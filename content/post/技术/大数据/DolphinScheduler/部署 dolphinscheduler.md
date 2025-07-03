---
categories:
- 技术
- 大数据
date: '2024-09-23 14:18:51+08:00'
tags:
- DolphinScheduler
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716212442829.png
title: 部署 dolphinscheduler
---
Centos 部署 dolphinscheduler
<!--more-->

# Ubuntu安装 MySQL
```shell
apt-get upgrade
apt-get install mysql-server
service mysql start
service mysql status
```
## 配置 MySQL
mysql 8.0以后默认没有"root@%"远程连接账户，修改远程连接密码需要这样做：
```sql
# MySQL里查看用户信息
use mysql;
select host, user, authentication_string from user;

# 创建用户
create user 'xx'@'%' identified by 'xx@xxx';
# 授权（给创建的新用户授权）
GRANT ALL PRIVILEGES ON *.* TO 'xx'@'%' WITH GRANT OPTION;
# 刷新权限
FLUSH PRIVILEGES;

# 然后还要修改配置文件，先关闭服务再修改
sudo systemctl stop mysql
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
把bind-address  = 127.0.0.1注释掉，保存文件，重启mysql

# 重启mysql（方式1）
sudo service mysql start

# 重启mysql（方式2）
sudo systemctl start mysql.service

 # 开启自启动
sudo systemctl enable mysql.service
```

# 安装 datax
1. 下载
`wget https://datax-opensource.oss-cn-hangzhou.aliyuncs.com/xx303/datax.tar.gz`
2. 部署
解压到/opt

# 安装 zookeeper
1. 下载 zk
2. 配置zk
```shell
cd /opt/apache-zookeeper-3.8.3-bin
-- 修改配置文件
server.1=192.168.xx.35:2888:3888
server.2=192.168.xx.34:2888:3888
server.3=192.168.xx.33:2888:3888
server.4=192.168.xx.32:2888:3888
server.5=192.168.xx.31:2888:3888

# 启动 zk
bin/zkServer.sh start
```

# 安装 DolphinScheduler
## 下载 ds
下载地址:[apache-dolphinscheduler-3.2.2-bin.tar.gz](https://www.apache.org/dyn/closer.lua/dolphinscheduler/3.2.2/apache-dolphinscheduler-3.2.2-bin.tar.gz)
解压到/opt

## 配置 ds
/opt/apache-dolphinscheduler-3.2.2-bin/bin/env/dolphinscheduler_env.sh
```shell
export JAVA_HOME=${JAVA_HOME:-/usr/lib/jvm/java-1.8.0-openjdk-amd64}

export DATABASE=mysql
export SPRING_PROFILES_ACTIVE=${DATABASE}
export SPRING_DATASOURCE_URL="jdbc:mysql://192.168.xx.xx/dolphinscheduler?useUnicode=true&characterEncoding=UTF-8&useSSL=false"
export SPRING_DATASOURCE_USERNAME=xx
export SPRING_DATASOURCE_PASSWORD=xx@xxx

# DolphinScheduler server related configuration
export SPRING_CACHE_TYPE=${SPRING_CACHE_TYPE:-none}
export SPRING_JACKSON_TIME_ZONE=${SPRING_JACKSON_TIME_ZONE:-UTC}

# Registry center configuration, determines the type and link of the registry center
export REGISTRY_TYPE=${REGISTRY_TYPE:-zookeeper}
export REGISTRY_ZOOKEEPER_CONNECT_STRING=${REGISTRY_ZOOKEEPER_CONNECT_STRING:-192.168.xx.31:2181,192.168.xx.32:2181,192.168.xx.33:2181,192.168.xx.34:2181,192.168.xx.35:2181}



export PATH=$HADOOP_HOME/bin:$SPARK_HOME/bin:$PYTHON_LAUNCHER:$JAVA_HOME/bin:$HIVE_HOME/bin:$FLINK_HOME/bin:$DATAX_LAUNCHER:$PATH
```

/opt/apache-dolphinscheduler-3.2.2-bin/bin/env/install_env.sh |grep -v "#"
```shell


ips=${ips:-"sjzz-sjyy-dw-cluster-3,sjzz-sjyy-dw-cluster-4,sjzz-sjyy-dw-cluster-5"}

sshPort=${sshPort:-"22"}

masters=${masters:-"sjzz-sjyy-dw-cluster-5"}

workers=${workers:-"sjzz-sjyy-dw-cluster-3:default,sjzz-sjyy-dw-cluster-4:default,sjzz-sjyy-dw-cluster-5:default"}

alertServer=${alertServer:-"sjzz-sjyy-dw-cluster-5"}

apiServers=${apiServers:-"sjzz-sjyy-dw-cluster-5"}

installPath=${installPath:-"/opt/apache-dolphinscheduler-3.2.2-bin"}

deployUser=${deployUser:-"root"}

zkRoot=${zkRoot:-"/dolphinscheduler"}
```
执行 install.sh
执行 start-all.sh

## MySQL数据库初始化
### 准备驱动包
找到 MySQL 驱动并移动到 DolphinScheduler 的每个模块的 libs 目录下，其中包括 `api-server/libs` 和 `alert-server/libs` 和 `master-server/libs` 和 `worker-server/libs` 和 `tools/libs`。
### 初始化数据库
```shell
mysql -uroot -p

mysql> CREATE DATABASE dolphinscheduler DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

# 以下已经创建了用户可忽略
mysql> CREATE USER 'xx'@'%' IDENTIFIED BY 'xx@xx';
mysql> GRANT ALL PRIVILEGES ON dolphinscheduler.* TO '{user}'@'%';
mysql> CREATE USER '{user}'@'localhost' IDENTIFIED BY '{password}';
mysql> GRANT ALL PRIVILEGES ON dolphinscheduler.* TO '{user}'@'localhost';
mysql> FLUSH PRIVILEGES;

# 执行bash 初始化脚本
bash tools/bin/upgrade-schema.sh
```
## 配置集群节点互相免密（步骤省略）
## 安装所有节点
```shell
cd /opt/apache-dolphinscheduler-3.2.2-bin
# 安装
./bin/install.sh
# 启动
./bin/start-all.sh
# 停止
./bin/stop-all.sh
```
## 启停服务
```shell
# 一键停止集群所有服务
bash ./bin/stop-all.sh

# 一键开启集群所有服务
bash ./bin/start-all.sh

# 启停 Master
bash ./bin/dolphinscheduler-daemon.sh stop master-server
bash ./bin/dolphinscheduler-daemon.sh start master-server

# 启停 Worker
bash ./bin/dolphinscheduler-daemon.sh start worker-server
bash ./bin/dolphinscheduler-daemon.sh stop worker-server

# 启停 Api
bash ./bin/dolphinscheduler-daemon.sh start api-server
bash ./bin/dolphinscheduler-daemon.sh stop api-server

# 启停 Alert
bash ./bin/dolphinscheduler-daemon.sh start alert-server
bash ./bin/dolphinscheduler-daemon.sh stop alert-server
```
## 资源放到 HDFS
1. 修改worker-server/conf/common.properties，api-server/conf/common.properties

```properties
resource.storage.type=HDFS
#hdfs目录
resource.storage.upload.base.path=/dolphinscheduler-192 
resource.hdfs.fs.defaultFS=hdfs://master:8020
```
2. 将 Hadoop 集群下的 `core-site.xml` 和 `hdfs-site.xml` 复制到 `worker-server/conf` 以及 `api-server/conf`
## Datax任务
需要把 datax 部署好并且在环境变量配置
export PYTHON_LAUNCHER=/usr/bin/python2
export DATAX_LAUNCHER=/opt/datax/bin/datax.py

## 动态修改参数
修改参考
 `curl -X POST http://192.168.xx.35:8040/api/update_config?streaming_load_json_max_mb=1024`

查看配置
`http://192.168.xx.31:8040/varz`
