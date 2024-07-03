---
categories:
- 技术
- 大数据
date: 2018-06-08 13:30:51+08:00
tags:
- cdh
thumbnailImage: //www.azheimage.top/markdown-img-paste-2019011014402315.png
title: cloudera-scm-agent启动报错
---
CDH报错信息处理
<!--more-->
<!-- toc -->
# CDH 报错信息cloudera-scm-agent dead but pid file exists


### 1. 通过报错信息得知cloudera-scm-agent挂掉了，但是pid还是存在
```shell
$ service cloudera-scm-agent status
cloudera-scm-agent dead but pid file exists
$ ls /var/run/cloudera-scm-agent
cgroups  cloudera-scm-agent.pid  events  flood  process  supervisor
# 删除cloudera-scm-agent.pid
$ rm -f cloudera-scm-agent.pid
# 重启agent
$ service cloudera-scm-agent start
# 查看状态
$ service cloudera-scm-agent status
cloudera-scm-agent dead but pid file exists
```

### 2. 删除pid还是不能重启成功，查看日志
```shell
$ tail -f /var/log/cloudera-scm-agent/cloudera-scm-agent.log
# 查看到报错信息，9000端口已经被占用
ChannelFailures: IOError("Port 9000 not free on 'vm3'",)
$ netstat -tunlp|grep 9000
tcp        0      0 10.171.133.79:9000          0.0.0.0:*                   LISTEN      4411/python2.6
# 删除pid，杀死端口占用的进程，然后重启
$ rm -rf cloudera-scm-agent.pid
$ kill -9 4411
$ service cloudera-scm-agent start
Starting cloudera-scm-agent:                               [  OK  ]
$ netstat -tunlp|grep 9000
tcp        0      0 10.171.133.79:9000          0.0.0.0:*                   LISTEN      6562/python2.6
$ service cloudera-scm-agent status
cloudera-scm-agent (pid  6562) is running...
```
## 启动成功！
