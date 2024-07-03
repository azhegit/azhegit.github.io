---
categories:
- 技术
- 虚拟化&云计算
date: '2019-06-11 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725103847120.png
title: 7-kolla离线仓库制作
---
准备OpenStack的docker镜像，以便新环境无网络环境移植
<!--more-->
## kolla离线仓库制作

|制作镜像主机|加载离线镜像主机|
|-|-|
|10.57.30.15|10.57.245.43|

### 1. 制作OpenStack本地镜像仓库
1. 下载镜像仓库
docker pull registry:2
2. 启动镜像仓库
docker run  -d -v /opt/registry:/var/lib/registry -p 4000:5000 --restart=always --name registry registry:2
3. 配置阿里云的Docker加速器，加快pull registry镜像，配置docker代理
mkdir -p /etc/docker
```bash
tee /etc/docker/daemon.json << 'EOF'
{
"registry-mirrors": ["https://a5aghnme.mirror.aliyuncs.com"]
}
EOF
mkdir -p /etc/systemd/system/docker.service.d
tee /etc/systemd/system/docker.service.d/http-proxy.conf << 'EOF'
[Service]
Environment="HTTP_PROXY=http://10.57.22.8:3128/"
EOF

```
重启docker：
systemctl daemon-reload && systemctl restart docker

4. 测试本地仓库
docker pull busybox
docker tag busybox 10.57.30.15:4000/busybox:1.0
docker push 10.57.30.15:4000/busybox:1.0
docker pull 10.57.30.15:4000/busybox:1.0
curl -XGET http://10.57.30.16:4000/v2/_catalog
5. 下载kolla镜像
down_load_openstack_queens.sh
6. 缺少镜像
Error: image kolla/centos-binary-freezer-api:queens not found
Error: image kolla/centos-binary-freezer-base:queens not found
Error: image kolla/centos-binary-bifrost-base:queens not found
Error: image kolla/centos-binary-bifrost-deploy:queens not found
Error: image kolla/centos-binary-blazar-api:queens not found
Error: image kolla/centos-binary-blazar-base:queens not found
Error: image kolla/centos-binary-blazar-manager:queens not found
Error: image kolla/centos-binary-karbor-api:queens not found
Error: image kolla/centos-binary-karbor-base:queens not found
Error: image kolla/centos-binary-karbor-operationengine:queens not found
Error: image kolla/centos-binary-karbor-protection:queens not found
Error: image kolla/centos-binary-congress-databinary:queens not found
Error: image kolla/centos-binary-dragonflow-base:queens not found
Error: image kolla/centos-binary-dragonflow-controller:queens not found
Error: image kolla/centos-binary-dragonflow-metadata:queens not found
Error: image kolla/centos-binary-dragonflow-publisher-service:queens not found
7. 修改docker配置
```bash
tee /etc/docker/daemon.json << 'EOF'
{
  "insecure-registries":["10.57.30.16:4000"]
}
EOF
```
systemctl daemon-reload && systemctl restart docker

8. 修改镜像tag
for i in `docker images|grep kolla|grep -v R|awk '{print $1}'`;do docker tag $i:queens 10.57.30.15:4000/$i:queens;done
9. 上传镜像到私有镜像仓库
for i in `docker images|grep 10.57.30.15|awk '{print $1}'`;do docker push $i:queens;done
10. 查看镜像是否上传成功
curl -XGET http://10.57.30.15:4000/v2/_catalog
11. 备份镜像文件
tar -zcvf kolla-openstack-queens-registry.tar.gz registry
12. 导出registy
docker save -o registry.tar registry

### 2. 启动制作好的镜像仓库
1. 安装docker并启动 
2. 指定docker仓库到本机ip
```bash
tee /etc/docker/daemon.json << 'EOF'
{
  "insecure-registries":["10.57.245.43:4000"]
}
EOF
systemctl daemon-reload
systemctl restart docker
```
3. 上传kolla-openstack-queens-registry.tar.gz，registry.tar.gz
4. 加载仓库镜像并启动
docker load < registry.tar.gz
docker run  -d -v /opt/registry:/var/lib/registry -p 4000:5000 --restart=always --name registry registry:2
5. 解压离线仓库
tar -zxvf kolla-openstack-queens-registry.tar.gz -C /opt/
6. 查看镜像是否上传成功
curl -XGET http://localhost:4000/v2/_catalog


