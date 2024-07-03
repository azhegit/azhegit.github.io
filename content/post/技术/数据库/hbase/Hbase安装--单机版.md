---
categories:
- 技术
- 数据库
date: 2018-07-13 16:18:38+08:00
tags:
- databases
- hbase
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716211711809.png
title: Hbase安装--单机版
---

HBase是列式数据库，HBase的历史由来 HBase是一个开源的非关系型分布式数据库（NoSQL）,基于谷歌的BigTable建模，是一个高可靠性、高性能、高伸缩的分布式存储系统，使用HBase技术可在廉价PC Server上搭建起大规模结构化存储集群
<!--more-->
## HBASE Logo：
![](https://www.azheimage.top/markdown-img-paste-20180713164554232.png)
# 本文讲述HBASE的单机版安装：
* ### 下载安装包
http://mirrors.tuna.tsinghua.edu.cn/apache/hbase/2.0.1/hbase-2.0.1-bin.tar.gz
* ### 解压安装包：
解压到/data01目录：`tar zxvf hbase-2.0.1-bin.tar.gz -C /data01`
* ### 修改HBASE环境文件：
`vim conf/hbase-env.sh`
>export JAVA_HOME=/usr/install/java
export HBASE_CLASSPATH=/data01/hbase-2.0.1/conf
>#告诉HBASE是否使用自己的zookeeper
>export HBASE_MANAGES_ZK=true

`vim conf/hbase-site.xml`
>\<configuration>
>    \<property>
>        \<name>hbase.rootdir\</name>
>        \<value>file:/data01/hbase-2.0.1\</value>
>    \</property>
>\</configuration>
>
* ### 执行启动：
启动：`bin/start-hbase`
shell命令行：`bin/hbase shell`
测试：
```
create 'graph' ,'janusgraph'
list
```
![](https://www.azheimage.top/markdown-img-paste-20180713170312805.png)

* ### 访问：http://localhost:16010/master-status
![](https://www.azheimage.top/markdown-img-paste-20180713170416277.png)

[0.98版本安装](http://archive.apache.org/dist/hbase/0.98.24/)
