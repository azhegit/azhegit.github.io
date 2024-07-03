---
categories:
- 技术
- 大数据
date: '2019-12-28 18:13:32+08:00'
tags:
- hadoop
thumbnailImage: //d1u9biwaxjngwg.cloudfront.net/welcome-to-tranquilpeak/city-750.jpg
title: 0-hadoop安装
---
Apache原生hadoop部署
<!--more-->
## 搭建hadoop2.7.7高可用HA

1. 下载hadoop2.7.7，zookeeper3.4.6
https://archive.apache.org/dist/hadoop/common/hadoop-2.7.7/hadoop-2.7.7.tar.gz
https://archive.apache.org/dist/zookeeper/zookeeper-3.4.6/zookeeper-3.4.6.tar.gz
2. 上传文件到hadoop-01
3. 解压hadoop并移动
tar zxvf hadoop-2.7.7.tar.gz -C /opt
4. 解压java
tar xvf jdk-8u171-linux-x64.tar -C /opt
5. 执行advance-cdh.sh

## 安装zookeeper
1. 解压zookeeper
tar zxvf zookeeper-3.4.6.tar.gz -C /opt
2. 修改配置文件zoo.cfg，myid
cd /opt/zookeeper-3.4.6/conf
cp zoo_sample.cfg zoo.cfg
vim zoo.cfg
```bash
tickTime=2000
initLimit=10
syncLimit=5
#修改数据目录
dataDir=/data/zookeeper
clientPort=2181
#添加主机配置
server.1=hadoop-01:2888:3888
server.2=hadoop-02:2888:3888
server.3=hadoop-03:2888:3888
```
mkdir /data/zookeeper
到之前配置的zookeeper数据文件所在的目录下生成一个文件叫myid，其中写上一个数字表明当前机器是哪一个编号的机器。
echo 1 > /data/zookeeper/myid
3. 拷贝到另外2台服务器
cd /opt
scp -r zookeeper-3.4.6 root@hadoop-02:`pwd`
scp -r zookeeper-3.4.6 root@hadoop-03:`pwd`
4. 修改myid
5. 配置环境变量：vim /etc/profile
```bash
export JAVA_HOME=/opt/jdk1.8.0_171
export HADOOP_HOME=/opt/hadoop-2.7.7
export ZOOKEEPER_HOME=/opt/zookeeper-3.4.6
export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$ZOOKEEPER_HOME/bin
```
source /etc/profile
6. 启动zookeeper
启动zookeeper的各种命令操作如下，可以使用绝对路径操作这些命令，也可使用相对路径操作这些命令，相对路径需要进到zookeeper服务的bin目录进行操作。
```bash
#启动ZK服务: 
zkServer.sh start
#停止ZK服务: 
zkServer.sh stop
#重启ZK服务: 
zkServer.sh restart
#查看ZK服务状态: 
zkServer.sh status
```
Zookeeper集群需要每台挨个启动。

## 安装hadoop2.7.7
1. 配置hadoop-env.sh、mapred-env.sh、yarn-env.sh
```bash
vim $HADOOP_HOME/etc/hadoop/hadoop-env.sh
vim $HADOOP_HOME/etc/hadoop/mapred-env.sh
vim $HADOOP_HOME/etc/hadoop/yarn-env.sh
#添加JAVA_HOME
export JAVA_HOME=/opt/jdk1.8.0_171
```
2. 修改core-site.xml
vim $HADOOP_HOME/etc/hadoop/core-site.xml
```xml
<configuration>
    <property>
        <!--集群服务的ID-->
        <name>fs.defaultFS</name>
        <value>hdfs://tdhdfs</value>
    </property>
    <property>
        <!--Zookeeper的节点-->
        <name>ha.zookeeper.quorum</name>
        <value>hadoop-01:2181,hadoop-02:2181,hadoop-03:2181</value>
    </property>
    <property>
        <!--Hadoop数据的目录-->
        <name>hadoop.tmp.dir</name>
        <value>/data/</value>
    </property>
</configuration>
```
3. 修改hdfs-site.xml
vim $HADOOP_HOME/etc/hadoop/hdfs-site.xml
```xml
<configuration>
    <property>
        <!--服务id-->
        <name>dfs.nameservices</name>
        <value>tdhdfs</value>
    </property>
    <property>
        <!--配置NameNode节点id-->
        <name>dfs.ha.namenodes.tdhdfs</name>
        <value>nn1,nn2</value>
    </property>
    <property>
        <!--配置NameNode1的节点-->
        <name>dfs.namenode.rpc-address.tdhdfs.nn1</name>
        <value>hadoop-01:8020</value>
    </property>
    <property>
        <!--配置NameNode2的节点-->
        <name>dfs.namenode.rpc-address.tdhdfs.nn2</name>
        <value>hadoop-02:8020</value>
    </property>
    <property>
        <!--配置NameNode1服务器地址-->
        <name>dfs.namenode.http-address.tdhdfs.nn1</name>
        <value>hadoop-01:50070</value>
    </property>
    <property>
        <!--配置NameNode2服务器地址-->
        <name>dfs.namenode.http-address.tdhdfs.nn2</name>
        <value>hadoop-02:50070</value>
    </property>
    <property>
        <!--此集群的JournalNode所在的算机-->
        <name>dfs.namenode.shared.edits.dir</name>
        <value>qjournal://hadoop-01:8485;hadoop-02:8485;hadoop-03:8485/tdhdfs</value>
    </property>
    <property>
        <!--ZKFC来监听哪个NameNode服务-->
        <name>dfs.client.failover.proxy.provider.tdhdfs</name>
        <value>org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider</value>
    </property>
    <property>
        <!--ssh远程私钥-->
        <name>dfs.ha.fencing.methods</name>
        <value>sshfence</value>
    </property>
    <property>
        <name>dfs.ha.fencing.ssh.private-key-files</name>
        <value>/root/.ssh/id_rsa</value>
    </property>
    <property>
        <!--journalnode的数据目录-->
        <name>dfs.journalnode.edits.dir</name>
        <value>/data/jn</value>
    </property>
    <property>
        <!--自动故障切换配置-->
        <name>dfs.ha.automatic-failover.enabled</name>
        <value>true</value>
    </property>
</configuration>
```
4. 修改slaves文件配置datanode节点
vim $HADOOP_HOME/etc/hadoop/slaves
5. 修改mapred-site.xml
cp $HADOOP_HOME/etc/hadoop/mapred-site.xml.template $HADOOP_HOME/etc/hadoop/mapred-site.xml
vim $HADOOP_HOME/etc/hadoop/mapred-site.xml
```xml
<configuration>
    <!-- 指定mr框架为yarn方式 -->
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
```
6. 修改yarn-site.xml
vim $HADOOP_HOME/etc/hadoop/yarn-site.xml
```xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.resourcemanager.ha.enabled</name>
        <value>true</value>
    </property>
    <!--该cluster-id不能与nameService相同-->
    <property>
        <name>yarn.resourcemanager.cluster-id</name>
        <value>tdyarn</value>
    </property>
    <!--指定2台Resource Manager (即Name Node )节点-->
    <property>
        <name>yarn.resourcemanager.ha.rm-ids</name>
        <value>rm1,rm2</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname.rm1</name>
        <value>hadoop-01</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname.rm2</name>
        <value>hadoop-02</value>
    </property>
    <!--指定zookeeper 节点-->
    <property>
        <name>yarn.resourcemanager.zk-address</name>
        <value>hadoop-01:2181,hadoop-02:2181,hadoop-03:2181</value>
    </property>
</configuration>
```
7. 配置文件拷贝到其他机器

## 启动hadoop
1. 确认zookeeper集群已经启动，如果没启动，挨个zkServer.sh start
2. 挨个启动journalnode
hadoop-daemon.sh start journalnode
3. 在其中一个NameNode上格式化hadoop.tmp.dir 并初始化
hadoop namenode -format
4. 把格式化后的元数据拷备到另一台NameNode节点上：
scp -r dfs hadoop-02:`pwd`
a)启动刚刚格式化的namenode :hadoop-daemon.sh start namenode
b)在没有格式化的namenode上执行：hdfs namenode -bootstrapStandby
c)启动第二个namenode:hadoop-daemon.sh start namenode
5. 初始化zookeeper，在任意一台NameNode中
hdfs zkfc -formatZK
6. 停止所有节点
stop-dfs.sh
7. 需要把zookeeper全部开启，然后全面启动节点:start-dfs.sh
8. 进行测试：在浏览器下输入hadoop-01:50070/hadoop-02:50070有一个节点处于active，一个节点处于standby，高可用成功
9. 如果hadoop-01突然挂掉了，那么hadoop-02备用的NameNode会自动的补上，替换为Active，	测试方法：Kill hadoop-01 的nameNode进程，然后再刷新hadoop-02
a)$ jps 			#ps是显示当前系统进程 ，jps就是显示当前系统的java 进程
b)$ kill -9 进程ID 	 #杀掉进程
c)在启动hadoop-01中的NameNode：hadoop-daemon.sh start namenode

## 启动yarn
1. 单独启动yarn使用命令：start-yarn.sh
2. 启动完成以后，另一台resourcemanager需要手动启动yarn：start-yarn.sh或者yarn-daemon.sh start resourcemanager
3. 启动所有Hadoop相关进程使用命令：start-all.sh


/home/admin/dist/hadoop/sbin/start-yarn.sh
/home/admin/dist/hadoop/sbin/yarn-daemon.sh start nodemanager
/home/admin/dist/hadoop/sbin/yarn-daemon.sh start historyserver
## hadoop双网卡路由
1. 配置允许路由转发
vim /etc/sysctl.conf
添加：net.ipv4.ip_forward = 1 # 默认值为0，修改为1，表示允许转发
sysctl -p
2. 关联包通过配置
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
3. 转发路由配置
4. iptables -t nat -A PREROUTING -d 10.10.13.28 -p tcp --dport 50070 -j DNAT --to-destination 10.93.124.2:50070
5. 查看配置
iptables -t nat  -L -n --line-numbers
6. 删除路由规则
iptables -t nat -D PREROUTING 1




