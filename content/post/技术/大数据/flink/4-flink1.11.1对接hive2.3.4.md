---
categories:
- 技术
- 大数据
date: '2020-07-23 14:23:50+08:00'
tags:
- flink
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716210809882.png
title: 4-flink1.11.1对接hive2.3.4
---
flink对接hive

### 环境准备
- MacOS
- flink1.11.1
<!--more-->
### 集成hive
1. 配置sql-client-hive.yaml
`cp $FLINK_HOME/conf/sql-client-defaults.yaml $FLINK_HOME/conf/sql-client-hive.yaml`
2. 准备hive-site.xml文件
3. 修改配置文件
```yaml
catalogs: 
  - name: myhive
    type: hive
    hive-conf-dir: /usr/local/flink-1.11.0/hive_conf
    hive-version: 1.1.1
execution:
  type: batch
```
4. 拷贝jar包
wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-hive-2.3.6_2.11/1.11.1/flink-sql-connector-hive-2.3.6_2.11-1.11.1.jar
hive-exec-2.3.6.jar

5. 启动flink
start-cluster.sh
6. 启动sql-client
`sql-client.sh embedded -d $FLINK_HOME/conf/sql-client-hive.yaml -l $FLINK_HOME/lib`
7. 查询结果
![](https://www.azheimage.top/markdown-img-paste-20200723100918109.png)
![](https://www.azheimage.top/markdown-img-paste-20200723101437653.png)
```
use catalog myhive;
show databases;
use test;
describe records;

select * from test.records;
```










