---
categories:
- 技术
- 数据库
date: '2024-09-13 15:51:46+08:00'
tags:
- neo4j
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725103847120.png
title: 部署 Neo4j
---
在 Linux 服务器快速部署Neo4j
<!--more-->
# 部署 Neo4j

## 安装JDK17
1. 下载

[下载java17地址](https://www.oracle.com/java/technologies/downloads/?er=221886#java17)

[选择对应版本](https://download.oracle.com/java/17/latest/jdk-17_linux-x64_bin.rpm)

2. 安装
`yum localinstall jdk-17_linux-x64_bin.rpm`
## 安装Neo4J
[参考官网地址](https://neo4j.com/docs/operations-manual/current/installation/linux/rpm/#_openjdk_java_17)

### 添加源
```shell
rpm --import https://debian.neo4j.com/neotechnology.gpg.key
cat << EOF >  /etc/yum.repos.d/neo4j.repo
[neo4j]
name=Neo4j RPM Repository
baseurl=https://yum.neo4j.com/stable/5
enabled=1
gpgcheck=1
EOF
```
### 安装Neo4J最新社区版
`yum install neo4j-5.23.0`
### 安装完毕，设置服务自启动
`systemctl enable neo4j`
### 修改配置文件/etc/neo4j/neo4j.conf
```ini
## 修改数据目录
server.directories.data=/data/neo4j/data
## 数据导入文件目录
server.directories.import=/data/neo4j/import
## JVM堆初始化内存
server.memory.heap.initial_size=4g

## JVM堆最大内存
server.memory.heap.max_size=8g
## 页缓存大小set to 50% of RAM minus the Java heap size
server.memory.pagecache.size=64g

server.bolt.listen_address=0.0.0.0:7687
server.http.listen_address=0.0.0.0:7474
```
### 修改初始化密码
`neo4j-admin dbms set-initial-password xx@neo4j`
创建索引获取 http Basic 密码:  echo -n "neo4j:xx@neo4j" | openssl base64
>得到密码：bmVvNGo6aHNtYXBAbmVvNGo=

### 启动Neo4j
`systemctl start neo4j`

### 访问地址：
http://192.168.xx.12:7474/browser/

![部署 Neo4j-0](https://www.azheimage.top/2025-07-03-15-56-e11ce50f94f2a2b3d0d061609e6326514353de7f9f5ae63dc2883a873dfe1014.png)  