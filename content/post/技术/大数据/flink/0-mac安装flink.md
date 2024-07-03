---
categories:
- 技术
- 大数据
date: '2020-07-16 11:52:07+08:00'
tags:
- flink
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725103847120.png
title: 0-mac安装flink
---
Mac环境部署flink
<!--more-->
### 1. 环境准备
- MacOS
- flink1.11.1
1. 下载[flink1.11.0安装包](https://flink.apache.org/downloads.html)
```xml
<plugin>  
    <groupId>org.apache.maven.plugins</groupId>  
    <artifactId>maven-surefire-plugin</artifactId>  
    <version>2.5</version>  
    <configuration>  
        <skipTests>true</skipTests>  
    </configuration>  
</plugin> 
```


### 安装
1. 解压到安装目录
`tar zxvf flink-1.11.0-bin-scala_2.11.tgz -C /usr/local/`
2. 配置环境变量
`vim ~/.bash_profile`,添加export FLINK_HOME=/usr/local/flink-1.11.0，并且在PATH后追加:$FLINK_HOME/bin,保存后`source ~/.bash_profile`
3. 启动flink
`start-cluster.sh`
4. 访问webUI
http://localhost:8081/#/overview
![](https://www.azheimage.top/markdown-img-paste-20200716120716220.png)

5. 运行SQL_Client
`sql-client.sh embedded`
![](https://www.azheimage.top/markdown-img-paste-20200716121416108.png)


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
flink-shaded-hadoop-2-uber-2.6.5-10.0.jar
hive-exec-1.1.1.jar
hive-metastore-1.1.0.jar
libfb303-0.9.2.jar
flink-connector-hive_2.11-1.10.1.jar
5. 启动flink
start-cluster.sh
6. 启动sql-client
sql-client.sh embedded -d $FLINK_HOME/conf/sql-client-hive.yaml -l $FLINK_HOME/lib
7. 查询结果
![](https://www.azheimage.top/markdown-img-paste-20200723100918109.png)
![](https://www.azheimage.top/markdown-img-paste-20200723101437653.png)









