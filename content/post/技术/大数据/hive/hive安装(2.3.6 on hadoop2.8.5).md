---
categories:
- 技术
- 大数据
date: '2020-08-27 18:20:35+08:00'
tags:
- hive
thumbnailImage: //www.azheimage.top/markdown-img-paste-2018111316554474.png
title: hive安装(2.3.6 on hadoop2.8.5)
---
对接hadoop2.8.5，选择Apache开源版本，下载[hive-2.3.6](http://archive.apache.org/dist/hive/hive-2.3.6/apache-hive-2.3.6-bin.tar.gz)
<!--more-->

## 安装hive


### 环境依赖
- hadoop:2.8.5
- java:1.8.0_252
- mysql:5.7.22

### 安装环境
- 安装用户:root
- 安装机器:hadoop-3
- hive版本：2.3.6
- 安装路径:/root/dist/apache-hive-2.3.6-bin
- 环境变量:~/.bashrc

### 安装步骤
1. 解压文件
`tar zxvf apache-hive-2.3.6-bin.tar.gz -C ~/dist/`
2. 修改配置文件
`cp hive-default.xml.template hive-site.xml`
3. 替换内容
```xml
<property>
  <name>javax.jdo.option.ConnectionURL</name>
  <value>jdbc:mysql://10.10.13.91:3306/hive?createDatabaseIfNotExist=true</value>
  <description>JDBC connect string for a JDBC metastore</description>
</property>
<property>
  <name>javax.jdo.option.ConnectionDriverName</name>
  <value>com.mysql.jdbc.Driver</value>
  <description>Driver class name for a JDBC metastore</description>
</property>
<property>
  <name>javax.jdo.option.ConnectionUserName</name>
  <value>root</value>
  <description>username to use against metastore database</description>
</property>
<property>
  <name>javax.jdo.option.ConnectionPassword</name>
  <value>tongdun@123</value>
  <description>password to use against metastore database</description>
</property>
<property>
  <name>hive.metastore.uris</name>
  <value>thrift://10.10.13.87:9083</value>
  <description>Thrift URI for the remote metastore. Used by metastore client to connect to remote
    metastore.
  </description>
</property>
```
4. 将mysql驱动包放到hive的lib目录
cp mysql-connector-java-5.1.36.jar $HIVE_HOME/lib/
5. 配置环境变量
```bash
export HIVE_HOME=/root/dist/apache-hive-2.3.6-bin
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HIVE_HOME/bin
```
6. 初始化MySQL中的hive库
`schematool -dbType mysql -initSchema`
7. 初始化成功
```bash
Metastore connection URL:	 jdbc:mysql://10.10.13.91:3306/hive?createDatabaseIfNotExist=true
Metastore Connection Driver :	 com.mysql.jdbc.Driver
Metastore connection User:	 root
Starting metastore schema initialization to 2.3.0
Initialization script hive-schema-2.3.0.mysql.sql
Initialization script completed
schemaTool completed
```
8. 启动hive
`hive`
9. 启动报错
>Exception in thread "main" java.lang.RuntimeException: java.lang.IllegalArgumentException: java.net.URISyntaxException: Relative path in absolute URI: ${system:java.io.tmpdir%7D/$%7Bsystem:user.name%7D
10. Hive里面配置的相对路径没有找到，我们可以直接在文件里面修改为绝对路径，修改hive-site.xml，将`${system:java.io.tmpdir}`替换成`/root/dist/apache-hive-2.3.6-bin/tmp`,
将`${system:user.name}`替换成`root`
    ```bash
    sed -i 's/${system:java.io.tmpdir}/\/root\/dist\/apache-hive-2.3.6-bin\/tmp/g' $HIVE_HOME/conf/hive-site.xml
    sed -i 's/${system:user.name}/root/g' $HIVE_HOME/conf/hive-site.xml
    ```
11. 启动hivemetastore
    ```bash
    mkdir $HIVE_HOME/logs
    nohup hive --service metastore >$HIVE_HOME/logs/hivemetastore.log 2>&1 &
    ```
12. 重新启动hive

