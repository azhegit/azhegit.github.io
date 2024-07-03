---
categories:
- 技术
- 大数据
date: '2021-08-03 14:37:41+08:00'
tags:
- flink
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110143649189.png
title: Flink监控搭建
---
<!-- # flink+prometheus+grafana监控配置 -->

[toc]
利用Apache Flink的内置指标系统以及如何使用Prometheus来高效地监控流式应用程序.
<!--more-->

基于PushGateway + prometheus的方式。Flink任务先将数据推到pushgateway。然后pushgateway将值推送到prometheus，最后grafana展示prometheus中的值,如下图
```mermaid
graph LR
Flink-->PushGateway
PushGateway-->Prometheus
Prometheus-->Grafana
```
## 环境准备
- Flink
- PushGateway
- Prometheus
- Grafana

因为环境都已经准备好，就不在此篇记录各环境安装。只记录基于现有环境新增的修改。

### Flink
需要修改配置文件`flink-conf.yaml`
```yaml
metrics.reporter.promgateway.class: org.apache.flink.metrics.prometheus.PrometheusPushGatewayReporter
# 这里写PushGateway的主机名与端口号
metrics.reporter.promgateway.host: xxx.com
metrics.reporter.promgateway.port: 9091
# Flink metric在前端展示的标签（前缀）与随机后缀
metrics.reporter.promgateway.jobName: flink-metrics-
metrics.reporter.promgateway.randomJobNameSuffix: true
# 关闭集群删除pushgateway数据
metrics.reporter.promgateway.deleteOnShutdown: true
metrics.reporter.promgateway.interval: 10 SECONDS
```
deleteOnShutdown有BUG，只会删除Jobmanager的信息数据，解决办法是写一个脚本，通过crontab定期执行过期的Taskmanager信息。
每分钟执行
`* * * * * sh /pushgateway-1.4.1.linux-amd64/cleanup.sh >> /pushgateway-1.4.1.linux-amd64/cleanup.out`
定期清理脚本：
```bash
#!/bin/bash

export MILLS=60
export ADD='xxx.com'

export PUSH_TIME_SECONDS=$(curl -X GET http://$ADD:9091/api/v1/metrics  | jq --raw-output '.data[].push_time_seconds')

export PUSH_TIME=($(echo $PUSH_TIME_SECONDS | jq --raw-output '.time_stamp'| sed 's/\"//g'))
export JOB=($(echo $PUSH_TIME_SECONDS | jq --raw-output '.metrics[0].labels.job'| sed 's/\"//g'))

export NUM=${#PUSH_TIME[@]}

#echo $PUSH_TIME_SECONDS | jq

CURRENT_TIME=$(date +%s)

#echo $PUSH_TIME

#echo $JOB

for ((i=0;i<NUM;i++))
do
 # echo -e "\033[1;32m[ `date -d ${PUSH_TIME[i]} +%s` ]\033[0m"
 # echo -e "\033[1;32m[${PUSH_TIME[i]}]\033[0m"
 # echo -e "\033[1;32m[${JOB[i]}]\033[0m"
  push_mill=`date -d ${PUSH_TIME[i]} +%s`
  let gaps=$CURRENT_TIME-$push_mill

  if [[ $gaps -ge $MILLS ]];then
    echo `date --date today +%Y%m%d_%H:%M:%S` gaps: $gaps '删除' ${JOB[i]}
    curl -X DELETE http://$ADD:9091/metrics/job/${JOB[i]}
  fi
done
```

### PushGateway
安装跳过，贴上[下载地址](https://prometheus.io/download/)
解压，创建启动pushgateway脚本：
```bash
ps -ef | grep pushgateway |grep -v simple | grep -v grep | awk '{print $2}' | xargs kill -9
nohup ./pushgateway  --web.enable-admin-api > pushgateway.out 2>&1 &
```

### Prometheus
安装跳过，启动脚本`./prometheus --config.file=./prometheus.yml --storage.tsdb.retention.time=15d --web.enable-lifecycle  > prometheus.out 2>&1 &`

修改配置文件,新增
```yaml
scrape_configs:
  - job_name: 'pushgateway'
    static_configs:
      - targets: ['xxx.com:9091']
```

### Grafana
跳过安装部署阶段，直接配置图表



