---
categories:
- 技术
- 大数据
date: '2020-06-18 14:47:05+08:00'
tags:
- kafka
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110143649189.png
title: 3-监控grafana+prometheus
---
配置kafka集群监控，及服务器相关信息监控
<!--more-->
## 监控
[grafana访问地址](http://10.57.26.136:3000/d/0kXIgLWGk/kafkaji-qun-jian-kong?orgId=1&refresh=10s)
用户名/密码:guest/guest

[toc]
## docker 镜像
docker pull prom/node-exporter
docker pull prom/prometheus
docker pull grafana/grafana

导出镜像
docker save prom/node-exporter > node-exporter.gz
docker save prom/prometheus > prometheus.gz
docker save grafana/grafana > grafana.gz

离线安装docker之后，将镜像导入
docker load < grafana.gz
docker load < prometheus.gz
docker load < node-exporter.gz

## node_exporter
### docker 启动
1. 启动node_export
```bash
docker run -d --restart=always \
  --name node_exporter \
  --net="host" \
  --pid="host" \
  -v "/:/host:ro,rslave" \
  prom/node-exporter \
  --path.rootfs=/host \
  --collector.filesystem.ignored-mount-points "^/(sys|proc|dev|host|etc)($|/)"
```
2. node_exporter启动脚本
```bash
cat > run-node-exporter.sh << 'EOF'
docker stop node_exporter
docker rm node_exporter
docker run -d --name node_exporter \
	--restart=always \
	--net="host" \
	--pid="host" \
	-v "/proc:/host/proc:ro" \
	-v "/sys:/host/sys:ro" \
	-v "/:/rootfs:ro" \
	prom/node-exporter \
	--path.procfs=/host/proc \
	--path.rootfs=/rootfs \
	--path.sysfs=/host/sys \
	--collector.filesystem.ignored-mount-points='^/(sys|proc|dev|host|etc)($$|/)'
EOF
```
3. 启动
chmod +x run-node-exporter.sh
sh run-node-exporter.sh
4. 当 Node Exporter 运行起来后，在浏览器中访问 http://IP:9100/metrics查看抓取metrics.
### 脚本启动
nohup ./node_exporter >> ~/node_exporter.out 2>&1 &

## prometheus
1. 创建配置文件及数据目录
```yml
global:
  scrape_interval:     5s
  evaluation_interval: 5s

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ['localhost:9090']
        labels:
          instance: prometheus

  - job_name: linux
    static_configs:
      - targets: ['10.57.26.136:9100']
```
mkdir -p /home/admin/data/prometheus/data
sudo chown -R 65534:65534 /home/admin/data/prometheus/data
2. 编写启动脚本
```bash
cat > run-prometheus.sh << 'EOF'
docker stop prometheus
docker rm prometheus
docker run -d --restart=always \
    --name=prometheus \
    -p 9090:9090 \
    -v /home/admin/opt/monitor/configs/prometheus.yml:/etc/prometheus/prometheus.yml \
    -v /home/admin/data/prometheus/data:/prometheus \
    prom/prometheus \
    --config.file=/etc/prometheus/prometheus.yml \
    --storage.tsdb.path=/prometheus \
    --web.console.libraries=/etc/prometheus/console_libraries \
    --web.console.templates=/etc/prometheus/consoles \
    --storage.tsdb.retention.time=168h \
    --web.enable-lifecycle
EOF
```
3. 启动脚本
chmod +x run-prometheus.sh
./run-prometheus.sh
4. 重载配置
从 2.0 开始，hot reload 功能是默认关闭的，如需开启，需要在启动 Prometheus的时候，添加 –web.enable-lifecycle 参数。
curl -X POST http://localhost:9090/-/reload


## grafana
1. 创建数据目录
mkdir -p /home/admin/data/grafana-storage
chmod 777 -R /home/admin/data/grafana-storage
2. 生成启动脚本
```bash
cat > run-grafana.sh << 'EOF'
docker stop grafana
docker rm grafana
docker run -d --restart always \
  -p 3000:3000 \
  --name=grafana \
  -e "GF_SERVER_ROOT_URL=http://192.168.92.25" \
  -e "GF_SECURITY_ADMIN_PASSWORD=admin" \
  -v ~/data/grafana-storage:/var/lib/grafana \
  grafana/grafana
EOF
```
3. 启动脚本
chmod +x run-grafana.sh
./run-grafana.sh

4. 登录并修改密码
5. 添加prometheus数据源
![](https://www.azheimage.top/markdown-img-paste-20200619112854182.png)
6. 导入prometheus图表
![](https://www.azheimage.top/markdown-img-paste-20200619113055693.png)
7. 就可以在主页查看
![](https://www.azheimage.top/markdown-img-paste-20200619113146117.png)
8. 查找想要的图表，[grafana dashboards](https://grafana.com/grafana/dashboards?orderBy=name&direction=asc),下载json文件
9. 导入node_exporter图表
![](https://www.azheimage.top/markdown-img-paste-20200619121215878.png)
9. 查看图表
![](https://www.azheimage.top/markdown-img-paste-20200619121406160.png)

## kafka_exporter
1. 下载[kafka_exporter](https://github.com/danielqsj/kafka_exporter/releases/download/v1.2.0/kafka_exporter-1.2.0.linux-amd64.tar.gz)
2. 启动kafka_exporter
nohup ./kafka_exporter-master --kafka.server=10.57.26.136:9092 >> ~/kafka_exporter.out 2>&1 &
3. 查看端口是否启动
ss -tunl | grep 9308
4. 修改prometheus.yml
```yml
global:
  scrape_interval:     5s
  evaluation_interval: 5s

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ['localhost:9090']
        labels:
          instance: prometheus

  - job_name: linux
    static_configs:
      - targets: ['10.57.26.136:9100']

  - job_name: kafka
    static_configs:
      - targets: ['10.57.26.136:9308']
        labels:
          instance: kafka@10.57.26.136
```
5. 更新prometheus配置
curl -X POST http://localhost:9090/-/reload
6. 启动成功
![](https://www.azheimage.top/markdown-img-paste-20200619142629418.png)
7. 下载grafana图表[json文件](https://grafana.com/api/dashboards/7589/revisions/5/download)
8. 导入图表
9. 查看图表
10. 添加另一个kafka集群启动
nohup ./kafka_exporter-master --kafka.server=10.57.26.110:9092 --sasl.enabled --sasl.username="td-kafka" --sasl.password="tongdun123" --sasl.mechanism='scram-sha256' >> ~/kafka_exporter.out 2>&1 &

## pushgateway
1. docker pull prom/pushgateway 
2. 编写脚本：
```bash
cat > run-pushgateway.sh << 'EOF'
docker stop pushgateway
docker rm pushgateway
docker run -d --restart always \
  -p 9091:9091 \
  --name=pushgateway \
  prom/pushgateway 
EOF
```
3. 执行启动脚本
4. 启动jmx_prometheus_httpserver
5. 修改prometheus配置

效果
![](https://www.azheimage.top/markdown-img-paste-20200628191122228.png)


