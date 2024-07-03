---
categories:
- 技术
- 数据库
date: '2021-10-27 20:19:27+08:00'
tags:
- Aerospike
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725101125909.png
title: 9-aerospike升级
---
特殊升级参考：https://docs.aerospike.com/server/operations/upgrade/special_upgrades

nohup asbackup -n large -l 172.16.20.79:3000 -z zstd -d large_79_zstd  > asbackup_large_0628.log 2>&1 &

<!--more-->


二级索引提升一倍

5000万索引构建之前2分钟

6.0 只需要1分钟





下载
wget https://github.com/aerospike/aerospike-server/releases/download/6.0.0.1/aerospike-server-community-6.0.0.1-1.el7.x86_64.rpm

rpm -ivh aerospike-server-community-6.0.0.1-1.el7.x86_64.rpm 


wget https://download.aerospike.com/artifacts/aerospike-tools/7.0.5/aerospike-tools-7.0.5-el7.tgz

tar zxvf aerospike-tools-7.0.5-el7.tgz 
cd aerospike-tools-7.0.5-el7
./asinstall

备份单节点数据
nohup asbackup -n large -l 172.16.20.79:3000 -z zstd -d large_79_zstd  > asbackup_large_0628.log 2>&1 &

修改配置
删除single-scan-threads 12

启动

nohup asrestore --host 172.16.20.19 -z zstd --directory large_79_zstd  -t 40 > restore_large_0630.log 2>&1 &


 nohup asrestore -z zstd --directory large_merge_zstd  -t 80 > restore_large_0707.log 2>&1 &



nohup asbackup -n large -s merge_v1_1_2_3  -M 900000000 -h 172.16.20.79  -z zstd -d large_9yi_zstd  > asbackup_large_0630.log 2>&1 &


![](https://www.azheimage.top/markdown-img-paste-20220707143816829.png)