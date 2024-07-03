---
categories:
- 技术
- 大数据
date: '2020-06-01 14:51:29+08:00'
tags:
- kafka
thumbnailImage: //www.azheimage.top/markdown-img-paste-2019011014402315.png
title: 1-kafka权限调研
---
调研kafka权限相关，并验证，生产级别
<!--more-->
[toc]
## 一、机器准备：
ip|机器|用户|jdk版本|zk版本|kafka版本|安装路径|
-|-|-|-|-|-|-
10.57.26.110|kafka-1|admin|jdk1.8.0_191|zookeeper-3.4.6|kafka_2.11-1.1.1|opt
10.57.26.111|kafka-1|admin|jdk1.8.0_191|zookeeper-3.4.6|kafka_2.11-1.1.1|opt
10.57.26.112|kafka-1|admin|jdk1.8.0_191|zookeeper-3.4.6|kafka_2.11-1.1.1|opt

## 二、安装zookeeper
[下载zookeeper3.4.6](http://archive.apache.org/dist/zookeeper/zookeeper-3.4.6/zookeeper-3.4.6.tar.gz)
1. 解压zookeeper
tar zxvf resources/zookeeper-3.4.6.tar.gz -C opt/
2. 修改配置文件zoo.cfg，myid
cd opt/zookeeper-3.4.6/conf
cp zoo_sample.cfg zoo.cfg
vim zoo.cfg
```bash
tickTime=2000
initLimit=10
syncLimit=5
#修改数据目录
dataDir=/home/admin/data/zookeeper
clientPort=2181
#添加主机配置
server.1=kafka-1:2888:3888
server.2=kafka-2:2888:3888
server.3=kafka-3:2888:3888
```
mkdir ~/data/zookeeper
到之前配置的zookeeper数据文件所在的目录下生成一个文件叫myid，其中写上一个数字表明当前机器是哪一个编号的机器。
echo 1 > ~/data/zookeeper/myid
3. 拷贝到另外2台服务器
cd ~/opt
scp -r zookeeper-3.4.6 admin@kafka-2:`pwd`
scp -r zookeeper-3.4.6 admin@kafka-3:`pwd`
4. 修改myid
echo 2 > ~/data/zookeeper/myid
echo 3 > ~/data/zookeeper/myid
5. 配置环境变量：vim /etc/profile
```bash
echo '
export JAVA_HOME=/home/admin/opt/jdk1.8.0_191
export KAFKA_HOME=/home/admin/opt/kafka_2.11-1.1.1
export ZOOKEEPER_HOME=/home/admin/opt/zookeeper-3.4.6
export PATH=$PATH:$JAVA_HOME/bin:$KAFKA_HOME/bin:$ZOOKEEPER_HOME/bin
' >> ~/.bashrc
source ~/.bashrc
java -version
```
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

1. [下载kafka1.1.1](http://archive.apache.org/dist/kafka/1.1.1/kafka_2.11-1.1.1.tgz)
2. 解压
`tar zxvf resources/kafka_2.11-1.1.1.tgz -C opt/`
3. 进入config目录,修改配置文件
`cd opt/kafka_2.11-1.1.1/config/`
`vim server.properties`
```bash
# （其他机器为 1/2）
broker.id =0
# zookeeper地址
zookeeper.connect= 10.57.26.110:2181,10.57.26.111:2181,10.57.26.112:2181
log.dirs =/home/admin/data/kafka-logs
# 本机地址
listeners=PLAINTEXT://10.57.26.110:9092
```
4. 发送到其他机器并修改对应配置broker .id，listeners
5. 添加环境变量
6. 挨个启动kafka
`nohup kafka-server-start.sh $KAFKA_HOME/config/server.properties > ~/kafka.out 2>&1 &`
7. 通过zookeeper命令行方式查看kafka集群节点数
`zkCli.sh`
>[zk: localhost:2181(CONNECTED) 0] ls /brokers/ids
[0, 1, 2]
8. 创建topic
```shell
kafka-topics.sh \
--create \
--zookeeper localhost:2181 \
--replication-factor 1 \
--partitions 1 \
--topic test-topic
```
9. 列出所有topic
```shell
kafka-topics.sh \
--list \
--zookeeper 10.57.26.110:2181
```
10. 查看列表及具体信息
```shell
kafka-topics.sh \
--zookeeper localhost \
--describe
>Topic:test-topic	PartitionCount:1	ReplicationFactor:3	Configs:
Topic: test-topic	Partition: 0	Leader: 2	Replicas: 1,2,0	Isr: 2,1,0
```

11. 查看topic集群情况：
```shell
kafka-topics.sh \
--describe \
--zookeeper localhost \
--topic test-topic
```
12. 生产消息
```shell
kafka-console-producer.sh \
--broker-list 10.57.26.110:9092 \
--topic test-topic
```
13. 消费消息
```shell
kafka-console-consumer.sh \
--zookeeper 10.57.26.110:2181 \
--from-beginning \
--topic test-topic
```
14. 删除topic
server.properties中配置了delete.topic.enable=true 通过kafka删除 效果显示的只是mark for deletion 并没有删除
```shell
kafka-topics.sh \
--delete \
--zookeeper 10.57.26.110:2181 \
--topic test-topic
```
15. 彻底删除topic
```bash
zkCli.sh -server 10.57.26.110
rmr /brokers/topic/test-topic
rmr /admin/delete_topics/test-topic
rmr /config/topics/test-topic
```
16. 重启kafka
```bash
kill -9 `ps -ef | grep kafka | grep -v grep| awk '{print $2}'`
nohup kafka-server-start.sh $KAFKA_HOME/config/server.properties > ~/kafka.out 2>&1 &
```

## 三、安装iptables
1. 安装
sudo yum -y install iptables-services
2. 启动
sudo service iptables start
3. 查看状态
service iptables status
4. 设置iptables的开机自启动
sudo systemctl enable iptables
5. 添加白名单规则及开放指定端口
sudo vim /etc/sysconfig/iptables
```sh
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
增加白名单
-N whitelist
-A whitelist -s 10.57.26.110 -j ACCEPT
-A whitelist -s 10.57.26.111 -j ACCEPT
-A whitelist -s 10.57.26.112 -j ACCEPT

-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
所有端口对白名单开放
-A INPUT -m state --state NEW -m tcp -p tcp --dport 1:65535 -j whitelist
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
开放kafka端口
-A INPUT -p tcp -m state --state NEW -m tcp --dport 9092 -j ACCEPT
开放kafka jmx端口
-A INPUT -p tcp -m state --state NEW -m tcp --dport 9999 -j ACCEPT
-A INPUT -j REJECT --reject-with icmp-host-prohibited
-A FORWARD -j REJECT --reject-with icmp-host-prohibited
COMMIT
```
6. 重启
sudo service iptables restart
7. 查看配置规则
sudo iptables -L -n

## 四、测试flink消费
1. 创建topic
```shell
kafka-topics.sh \
--create \
--zookeeper 10.57.26.110:2181 \
--replication-factor 1 \
--partitions 1 \
--topic test
```
2. 消费
```shell
kafka-console-consumer.sh \
--zookeeper 10.57.26.110:2181 \
--from-beginning \
--topic test
```
3. 启动生产者发送消息
4. 启动flink程序消费

## 五、开启SASL_SCRAM认证
### 1. 创建SCRAM证书
Kafka的SCRAM实现使用Zookeeper作为证书存储。通过使用kafka-configs.sh来创建证书。 对于启用的每个SCRAM机制，必须通过使用机制名称添加配置来创建证书。 必须在kafka broker启动之前创建broker之间通信的证书。客户端证书可以动态创建和更新，并且将使用更新后的证书来验证新的连接。

1. 为用户**td-kafka**创建SCRAM凭证（密码为*tongdun123*），该用户作为kafka各broker之间通信的用户：
```
kafka-configs.sh \
--zookeeper localhost:2181 \
--alter \
--add-config 'SCRAM-SHA-256=[iterations=8192,password=tongdun123],SCRAM-SHA-512=[password=tongdun123]' \
--entity-type users \
--entity-name td-kafka
```
>如果未指定迭代数，则使用默认迭代数为4096。 创建一个随机salt，由salt，迭代，StoredKey和ServerKey组成的SCRAM标识，都存储在Zookeeper中。
2. 可以使用--describe列出现有的证书：
```shell
kafka-configs.sh \
--zookeeper localhost:2181 \
--describe \
--entity-type users \
--entity-name td-kafka
```
3. 可以使用--delete为一个或多个SCRAM机制删除证书：
```bash
#添加一个admin用户
kafka-configs.sh \
--zookeeper localhost:2181 \
--alter \
--add-config 'SCRAM-SHA-256=[iterations=8192,password=tongdun123],SCRAM-SHA-512=[password=tongdun123]' \
--entity-type users \
--entity-name admin
#删除admin用户
kafka-configs.sh \
--zookeeper localhost:2181 \
--alter \
--delete-config 'SCRAM-SHA-512,SCRAM-SHA-256' \
--entity-type users \
--entity-name admin
```
4. SCRAM加密信息在zk里面，所以zk需要加固，才能保证密钥不被泄露
### 2. 配置Broker
1. 配置Kafka Broker
在每个Kafka broker的config目录下添加一个类似于下面的JAAS文件，我们姑且将其称为kafka_server_jaas.conf：
cd $KAFKA_HOME/config
vim kafka_server_jaas.conf
```bash
KafkaServer {
 org.apache.kafka.common.security.scram.ScramLoginModule required
 username="td-kafka"
 password="tongdun123";
};
```
2. 复制到其他broker节点
```bash
scp kafka_server_jaas.conf kafka-2:`pwd`
scp kafka_server_jaas.conf kafka-3:`pwd`
```
其中，broker使用KafkaServer中的用户名和密码来和其他broker进行连接。 在这个例子中，td-kafka是broker之间通信的用户。
3. 修改kafka启动脚本，讲JAAS配置文件的位置作为JVM参数：
```bash
cd $KAFKA_HOME/bin
vim kafka-server-start.sh
#添加一下内容
if [ "x$KAFKA_OPTS"  ]; then
    export KAFKA_OPTS="-Djava.security.auth.login.config=$KAFKA_HOME/config/kafka_server_jaas.conf"
fi
```
4. 复制到其他broker节点
scp kafka-server-start.sh kafka-2:`pwd`
scp kafka-server-start.sh kafka-3:`pwd`

5. 修改server.properties中配置SASL端口和SASL机制。 增加一下三行：
```bash
cd $KAFKA_HOME/config
vim server.properties
#修改
listeners=SASL_PLAINTEXT://10.57.26.110:9092
#添加下面内容
security.inter.broker.protocol=SASL_PLAINTEXT
sasl.mechanism.inter.broker.protocol=SCRAM-SHA-256
sasl.enabled.mechanisms=SCRAM-SHA-256
#默认禁止一切操作，必须显式授权
#allow.everyone.if.no.acl.found=false
#管理员用户允许做一切操作
super.users=User:td-kafka;
authorizer.class.name=kafka.security.auth.SimpleAclAuthorizer
```
### 3. 配置kafka客户端
1. 在config目录添加kafka_client_jaas.conf
```bash
cd $KAFKA_HOME/config
vim kafka_client_jaas.conf
#添加内容
KafkaClient {
 org.apache.kafka.common.security.scram.ScramLoginModule required
 username="td-kafka"
 password="tongdun123";
};
```
2. 复制到其他broker节点
```bash
scp kafka_client_jaas.conf kafka-2:`pwd`
scp kafka_client_jaas.conf kafka-3:`pwd`
```
3. 修改producer.properties,consumer.properties 中配置以下参数,并同步到所有节点
```bash
echo '
security.protocol=SASL_PLAINTEXT
sasl.mechanism=SCRAM-SHA-256
' >> producer.properties

echo '
security.protocol=SASL_PLAINTEXT
sasl.mechanism=SCRAM-SHA-256
' >> consumer.properties

scp producer.properties consumer.properties kafka-2:`pwd`
scp producer.properties consumer.properties kafka-3:`pwd`
```

4. 修改`kafka-console-producer.sh` 和 `kafka-console-consumer.sh` 文件
```bash
cd $KAFKA_HOME/bin
vim kafka-console-producer.sh
#添加一下内容
if [ "x$KAFKA_OPTS"  ]; then
    export KAFKA_OPTS="-Djava.security.auth.login.config=$KAFKA_HOME/config/kafka_client_jaas.conf"
fi
vim kafka-console-consumer.sh
#添加一下内容
if [ "x$KAFKA_OPTS"  ]; then
    export KAFKA_OPTS="-Djava.security.auth.login.config=$KAFKA_HOME/config/kafka_client_jaas.conf"
fi
```
4. 复制到其他broker节点
```bash
scp kafka-console-producer.sh kafka-console-consumer.sh kafka-2:`pwd`
scp kafka-console-producer.sh kafka-console-consumer.sh kafka-3:`pwd`
```
5. 重启kafka集群
6. 创建topic
```shell
kafka-topics.sh \
--zookeeper 10.57.26.110:2181 \
--create \
--topic test \
--partitions 1 \
--replication-factor 1;
```
7. 命令行启动消费者
```shell
kafka-console-consumer.sh  \
--bootstrap-server 10.57.26.110:9092 \
--consumer.config $KAFKA_HOME/config/consumer.properties \
--topic test
```
8. 命令行启动生产者
```shell
kafka-console-producer.sh \
--broker-list 10.57.26.110:9092  \
--producer.config $KAFKA_HOME/config/producer.properties \
--topic test
```
9. 正常消费

### 4.权限管理
#### 4.1 用户管理
1. 用户创建
```bash
kafka-configs.sh \
--zookeeper 10.57.26.110:2181 \
--alter \
--add-config 'SCRAM-SHA-256=[password=test123]' \
--entity-type users \
--entity-name test
```
2. v查看用户
ls /config/users
3. 查看用户信息
```bash
kafka-configs.sh \
--zookeeper 10.57.26.110:2181 \
--describe \
--entity-type users \
# 可以不指定用户
--entity-name test
```
4. 修改用户密码
```bash
kafka-configs.sh \
--zookeeper 10.57.26.110:2181 \
--alter \
--add-config 'SCRAM-SHA-256=[password=test1234]' \
--entity-type users \
--entity-name test
```
4. 删除用户
```bash
kafka-configs.sh \
--zookeeper 10.57.26.110:2181 \
--alter \
--delete-config 'SCRAM-SHA-256' \
--entity-type users \
--entity-name test
```
#### 4.2 Topic授权管理
1. 授予test用户对test topic 写权限, 只允许 10.57.241.* 网段
```bash
kafka-acls.sh \
--authorizer kafka.security.auth.SimpleAclAuthorizer \
--authorizer-properties zookeeper.connect=10.57.26.110:2181 \
--add \
--allow-principal User:test \
--operation Write \
--topic test \
--allow-host 10.57.241.161
```
2. 删除topic权限
```bash
kafka-acls.sh \
--authorizer kafka.security.auth.SimpleAclAuthorizer \
--authorizer-properties zookeeper.connect=localhost:2181 \
--remove \
--allow-principal User:test \
--operation Write \
--topic test \
--allow-host 10.57.241.*
```
3. 查看topic权限
```bash
kafka-acls.sh \
--authorizer kafka.security.auth.SimpleAclAuthorizer \
--authorizer-properties zookeeper.connect=localhost:2181 \
--list \
--topic test
```

## 六、Scala/Java 原生权限验证
1. 消费及生产程序改造
kafka的properties需要添加
```java
props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG,SecurityProtocol.SASL_PLAINTEXT.name)
props.put(SaslConfigs.SASL_JAAS_CONFIG,"org.apache.kafka.common.security.scram.ScramLoginModule required username=\"dev\" password=\"dev123\";")
props.put(SaslConfigs.SASL_MECHANISM,"SCRAM-SHA-256")
```
2. 创建topic
```shell
kafka-topics.sh \
--zookeeper 10.57.26.110:2181 \
--create \
--topic dev-topic \
--partitions 3  \
--replication-factor 2
```
3. 启动消费程序跟生产程序都报错
>failed authentication due to: Authentication failed due to invalid credentials with SASL mechanism SCRAM-SHA-256
4. 查询权限
```shell
kafka-acls.sh \
--authorizer-properties zookeeper.connect=10.57.26.110:2181 \
--list \
--topic dev-topic
```
>Current ACLs for resource `Topic:dev-topic`:
5. 创建dev用户
```shell
kafka-configs.sh \
--zookeeper localhost:2181 \
--alter \
--add-config 'SCRAM-SHA-256=[password=dev123]' \
--entity-type users \
--entity-name dev
```
6. 添加写权限
```bash
kafka-acls.sh \
--authorizer-properties  zookeeper.connect=10.57.26.110:2181 \
--add \
--allow-principal User:dev \
--producer \
--topic dev-topic
```
--producer实际上在Topic域上创建了(Write/Describe/Create)3个子权限，用户也可以单独创建者三个子权限。

7. 再次启动生产程序不报错了
8. 添加读权限
```bash
kafka-acls.sh \
--authorizer-properties  zookeeper.connect=10.57.26.110:2181 \
--add \
--allow-principal User:dev \
--consumer \
--topic dev-topic \
--group '*'
```
和producer相比，consumer还有一个额外的参数--group，如果没有限制，则置成'*'即可；这个--consumer的选择实际上在Topic域上创建了(Read/Describe)2个子权限，然后在Group域创建了(Read)1个子权限：

9. dev用户可以正常消费
10. 查看dev-topic权限
```shell
kafka-acls.sh \
--authorizer-properties zookeeper.connect=10.57.26.110:2181 \
--list \
--topic dev-topic

>Current ACLs for resource `Topic:dev-topic`:
 	User:dev has Allow permission for operations: Describe from hosts: *
	User:dev has Allow permission for operations: Write from hosts: *
	User:dev has Allow permission for operations: Read from hosts: *
```

## 七、Flink、Spark Streaming、Spring boot权限验证
## 八、Kafka-manager部署
1. 下载最新[kafka-manager-1.3.3.23](https://yusure.cn/usr/uploads/kafka-manager-1.3.3.23.zip)版本
2. 解压安装
unzip kafka-manager-1.3.3.23.zip -d ~/opt/
3. 修改配置文件
```bash
> vim ~/opt/kafka-manager-1.3.3.23/conf
#修改zk ip
kafka-manager.zkhosts="stream-server:2181"
```
4. 启动
nohup kafka-manager &
5. 页面添加kafka集群
填写zk地址，选择kafka版本，开启Poll consumer information
6. 添加加密集群
填写zk地址，选择kafka版本，开启Poll consumer information，填写Security Protocol，SASL Mechanism，SASL JAAS Config 

## 八、Kafka-manager故障解决
1. 收集JMX端口打开
```log
java.lang.IllegalArgumentException: requirement failed: No jmx port but jmx polling enabled!
```
解决办法：
>在`kafka-server-start.sh`添加export JMX_PORT=9999
2. no route to host
```log
k.m.j.KafkaJMX$ - Failed to connect to service:jmx:rmi:///jndi/rmi://10.57.26.111:9999/jmxrmi
java.io.IOException: Failed to retrieve RMIServer stub: javax.naming.CommunicationException [Root exception is java.rmi.ConnectIOException: Exception creating connection to: 10.57.26.111; nested exception is:
        java.net.NoRouteToHostException: No route to host (Host unreachable)]
```
解决办法：添加-Djava.rmi.server.hostname=kafka当前主机ip
KAFKA_JMX_OPTS="-Djava.rmi.server.hostname=10.57.26.110 -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false  -Dcom.sun.management.jmxremote.ssl=false "
修改防火墙规则
3. Caused by: java.lang.IllegalArgumentException: JAAS config entry not termina
解决办法：
kafka配置jaas密码的末尾少一个分号

## 九、Kafka MirrorMaker使用
1. 修改consumer.properties
```bash
# 源kafka集群地址
bootstrap.servers=10.57.26.136:9092
# consumer group id 自定义
group.id=dp-MirrorMaker
```
2. 复制出一个供mirror使用的producer.properties
```bash
>cp producer.properties mirror-producer.properties
>vim mirror-producer.properties
#修改需要同步的目标集群地址
bootstrap.servers=10.57.26.110:9092,10.57.26.111:9092,10.57.26.112:9092
# 添加SASL配置
security.protocol=SASL_PLAINTEXT
sasl.mechanism=SCRAM-SHA-256
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required username=** password=”**“;
```
3. 启动脚本
```bash
kafka-run-class.sh kafka.tools.MirrorMaker --consumer.config $KAFKA_HOME/config/consumer.properties --producer.config $KAFKA_HOME/config/mirror-producer.properties --num.streams 1 —-num.producers 1 --whitelist=mirror1
```

## 十、Kafka 源码阅读及修改
1. 下载kafka1.1.1源码
2. 下载[gradle-4.10.3](https://services.gradle.org/distributions/gradle-4.10.3-bin.zip)并安装
3. idea导入项目
![](https://www.azheimage.top/markdown-img-paste-20200610175846832.png)
4. 下载gradle依赖及编译
./gradlew jar
5. 为了提高gradle下载依赖速度
```bash
>vim ~/.gradle/init.gradle
```
```bsh
#添加一下内容到文件
allprojects{
    repositories {
        def REPOSITORY_URL = 'http://maven.aliyun.com/nexus/content/groups/public/'
        all { ArtifactRepository repo ->
            if(repo instanceof MavenArtifactRepository){
                def url = repo.url.toString()
                if (url.startsWith('https://repo1.maven.org/maven2') || url.startsWith('https://jcenter.bintray.com/')) {
                    project.logger.lifecycle "Repository ${repo.url} replaced by $REPOSITORY_URL."
                    remove repo
                }
            }
        }
        maven {
            url REPOSITORY_URL
        }
    }
}
```
6. 修改后的包替换kafka_2.11-1.1.1.jar
7. 启动脚本
```bash
kafka-run-class.sh kafka.tools.MirrorMaker \
--consumer.config $KAFKA_HOME/config/consumer.properties \
--producer.config $KAFKA_HOME/config/mirror-producer.properties \
--num.streams 1 \
--message.handler kafka.tools.CustomMirrorMakerMessageHandler \
--whitelist="mirror1|mirror2"  \
--message.handler.args "mirror1->mirror1,mirror2|mirror2->mirror2"
```

![](https://www.azheimage.top/markdown-img-paste-20200610115259114.png)

### 错误
##### 1. kafka源码日志未打印
出现：SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
具体做法：
1.下载相应的jar包，libs/slf4j-log4j12-1.7.25.jar libs/log4j-1.2.17.jar
2.导入jar包
具体的IDEA操作如下：
（1）File -> Project Structure -> Modules
（2）找到 core，main，打开 dependencies，点击 +，添加 libs目录
##### 2. 缺少log4j.properties
log4j:WARN No appenders could be found for logger (kafka.utils.Log4jControllerRegistration$).
解决办法：
在core-main添加resources目录，新建log4j.properties,并添加以下内容
```properties
log4j.rootCategory=info, console
log4j.appender.console=org.apache.log4j.ConsoleAppender
log4j.appender.console.target=System.out
log4j.appender.console.layout=org.apache.log4j.PatternLayout
log4j.appender.console.layout.ConversionPattern=[%d] %p %m (%c)%n
```

## 十一、kafka压测脚本
- topic:test-perf
- 分区数:1
- 副本数:1
- 测试机器：4C16G,kafka单节点
### 1. kafka生产数据写入压力测试
<table>
  <tr>
    <th>测试场景</th><th>生产消息总条数</th><th>每秒写入最大消息数</th><th>记录大小(单位:字节)</th>
  </tr>
	<tr>
		<td rowspan="3">Kafka消息写入测试</td>
    <td>10W</td><td>2000条</td><td>1000</td>
	</tr>
  <tr>
    <td>100W</td><td>5000条</td><td>2000</td>
	</tr>
  <tr>
    <td>1000W</td><td>10000条</td><td>2000</td>
  </tr>
</table>

### 2. kafka消费数据压力测试

<table>
  <tr>
    <th>测试场景</th><th>消费消息数</th>
  </tr>
	<tr>
		<td rowspan="3">Kafka消息写入测试</td>
    <td>10W</td>
	</tr>
  <tr>
    <td>100W</td>
	</tr>
  <tr>
    <td>1000W</td>
  </tr>
</table>

### 3. 写入压测命令
<table>
  <tr>
    <th>测试场景</th><th>压测消息数（单位：W）</th><th>测试命令</th><th>执行结果</th><th/>磁盘空间大小
  </tr>
	<tr>
		<td rowspan="3">Kafka消息写入测试</td>
    <td>10</td>
    <td>kafka-producer-perf-test.sh --topic test-perf --num-records 100000 --record-size 1000 --throughput 2000 --producer-props bootstrap.servers=10.57.26.136:9092</td>
    <td/>100000 records sent, 1999.680051 records/sec (1.91 MB/sec), 0.91 ms avg latency, 206.00 ms max latency, 1 ms 50th, 1 ms 95th, 3 ms 99th, 58 ms 99.9th.
    <td/>约100M
	</tr>
  <tr>
    <td>100</td>
    <td>kafka-producer-perf-test.sh --topic test-perf --num-records 1000000 --record-size 2000 --throughput 5000 --producer-props bootstrap.servers=10.57.26.136:9092</td>
    <td/>1000000 records sent, 4999.675021 records/sec (9.54 MB/sec), 0.74 ms avg latency, 173.00 ms max latency, 1 ms 50th, 1 ms 95th, 2 ms 99th, 51 ms 99.9th.
    <td/>约2G
	</tr>
  <tr>
    <td>1000</td>
    <td>kafka-producer-perf-test.sh --topic test-perf --num-records 10000000 --record-size 2000 --throughput 10000 --producer-props bootstrap.servers=10.57.26.136:9092</td>
    <td/>10000000 records sent, 9999.870002 records/sec (19.07 MB/sec), 0.92 ms avg latency, 179.00 ms max latency, 1 ms 50th, 2 ms 95th, 2 ms 99th, 16 ms 99.9th.
    <td/>约20G
  </tr>
</table>

### 4. 消费压测命令
<table>
  <tr>
    <th>测试场景</th><th>压测消息数（单位：W）</th><th>测试命令</th><th>接收数据量(MB)</th><th/>数据量(MB/s)<th/>数据量(条/s)<th/>时间(s)
  </tr>
	<tr>
		<td rowspan="3">Kafka消息消费测试</td>
    <td>10</td>
    <td/>kafka-consumer-perf-test.sh --zookeeper localhost:2181 --topic test-perf --fetch-size 1048576 --messages 100000 --threads 1
    <td/>95.3674<td/>61.8867<td/>59527.3528<td/>1.5
	</tr>
  <tr>
    <td>100</td>
    <td/>kafka-consumer-perf-test.sh --zookeeper localhost:2181 --topic test-perf --fetch-size 1048576 --messages 1000000 --threads 1
    <td/>1811.9812<td/>107.8624<td/>59527.3528<td/>17
	</tr>
  <tr>
    <td>1000</td>
    <td/>kafka-consumer-perf-test.sh --zookeeper localhost:2181 --topic test-perf --fetch-size 2097152 --messages 10000000 --threads 1
    <td/>18978.1189<td/>124.9498<td/>65838.8528<td/>152
  </tr>
</table>

## 十二、kafka数据同步
1. 创建topic
cd sasl_kafka_tools/
./kafka_topic_create.sh teset-copy 2 1
2. 配置mirror-maker环境变量
3. 启动mirror-maker
./pstart.sh mk
4. 通过脚本发送数据
```bash
kafka-producer-perf-test.sh \
--topic teset-copy \
--num-records 1000000 \
--record-size 2000 \
--throughput 5000 \
--producer-props bootstrap.servers=10.57.26.136:9092
```
5. 源topic数据量2G左右。同步10个副本到二级kafka，数据量10倍，占二级kafka集群磁盘空间20G

## 十三、机器评估
生产环境kafka，36h数据量top3
- dsp-wave-radar-original 总内存约为 361 G
- etl-merge-vehicle-data 总内存约为 31 G
- etl-siteregion-speed 总内存约为 24 G

二级kafka3台机器，磁盘空间单台1T，可支持扩展

