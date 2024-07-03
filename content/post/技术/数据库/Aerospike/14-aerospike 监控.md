---
categories:
- 技术
- 数据库
date: '2022-04-18 16:18:39+08:00'
tags:
- Aerospike
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110143649189.png
title: 14-aerospike 监控
---
prometheus跟grafana已经安装好，此篇忽略，重点讲Aerospike监控安装及配置。
<!--more-->
1. 下载aerospike-prometheus-exporter
https://download.aerospike.com/artifacts/aerospike-prometheus-exporter/1.5.0/aerospike-prometheus-exporter-1.5.0-x86_64.rpm.tar.gz
2. 安装
rpm -ivh aerospike-prometheus-exporter-1.5.0-x86_64.rpm
3. 启动aerospike-prometheus-exporter
systemctl start aerospike-prometheus-exporter.service
4. 验证是否启动端口
telnet localhost 9145
5. 配置Prometheus
```yml
scrape_configs:
  - job_name: 'aerospike'
    static_configs:
      - targets: ['aerospike-1:9145']
      - targets: ['aerospike-2:9145']
      - targets: ['aerospike-3:9145']
      - targets: ['aerospike-4:9145']
```
4. 