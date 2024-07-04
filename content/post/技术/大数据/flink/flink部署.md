---
categories:
- 技术
- 大数据
date: '2022-07-04 13:06:59+08:00'
tags:
- flink
thumbnailImage: //d1u9biwaxjngwg.cloudfront.net/welcome-to-tranquilpeak/city-750.jpg
title: flink部署
---

下载
wget https://archive.apache.org/dist/flink/flink-1.5.6/flink-1.5.6-bin-hadoop27-scala_2.11.tgz

<!--more-->

## 1. standalone 方式

1. 解压文件
   tar zxvf flink-1.5.6-bin-hadoop27-scala_2.11.tgz -C /opt/
2. 修改环境变量
3. 修改配置文件

```bash
vim $FLINK_HOME/conf/flink-conf.yaml
#修改
jobmanager.rpc.address: hadoop-01
taskmanager.numberOfTaskSlots: 4
--------
vim $FLINK_HOME/conf/masters
#修改
hadoop-01:8081
--------
vim $FLINK_HOME/conf/slaves
hadoop-01
hadoop-02
hadoop-03
--------
```

4. 把 flink-1.5.6 拷贝到其他机器
   scp -r flink-1.5.6 hadoop-02:`pwd`
   scp -r flink-1.5.6 hadoop-03:`pwd`
5. 执行启动命令
   [root@hadoop-01 ~]# start-cluster.sh
   Starting cluster.
   Starting standalonesession daemon on host hadoop-01.
   Starting taskexecutor daemon on host hadoop-01.
   Starting taskexecutor daemon on host hadoop-02.
   Starting taskexecutor daemon on host hadoop-03.
6. 登录页面查看
   ![](https://www.azheimage.top/markdown-img-paste-20191121170520656.png)
7. 编写 WordCount 实时程序

```scala
package io.github.wzq.offline
import org.apache.flink.api.java.utils.ParameterTool
import org.apache.flink.streaming.api.scala._
/**
  * Created by azhe on 2019-11-21 14:37
  */
object StreamWordCount {
  def main(args: Array[String]): Unit = {
    val arg: ParameterTool = ParameterTool.fromArgs(args)
    val host: String = arg.get("host")
    val port: Int = arg.getInt("port")
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    val socktStream: DataStream[String] = env.socketTextStream(host,port)
    val wordCount: DataStream[(String, Int)] = socktStream.flatMap(_.split(" "))
      .filter(_.nonEmpty)
      .map((_, 1))
      .keyBy(0)
      .sum(1)
    wordCount.print().setParallelism(2)

    env.execute("Stream word count")
  }
}
```

8. hadoop-02 启动 tcp 端口
   [root@hadoop-02 ~]# nc -lk 8888
9. 上传打包好的 jar，编辑提交参数，执行 submit
   ![](https://www.azheimage.top/markdown-img-paste-20191121171753565.png)
10. running 状态
    ![](https://www.azheimage.top/markdown-img-paste-20191121171902952.png)
11. 发送两条数据，查看 taskmanager 的 stdout
    [root@hadoop-02 ~]# nc -lk 8888
    hello flink
    hello scala
12. 页面查看结果
    ![](https://www.azheimage.top/markdown-img-paste-20191121172146531.png)
13. 停止任务可以页面点击 cancel 按钮，或者命令行操作

```bash
[root@hadoop-01 conf]# flink list
Waiting for response...
------------------ Running/Restarting Jobs -------------------
21.11.2019 04:17:57 : 7b6607a8a5cdecaa7e88bcfa3ec680cc : Stream word count (RUNNING)
--------------------------------------------------------------
No scheduled jobs.
[root@hadoop-01 conf]# flink cancel 7b6607a8a5cdecaa7e88bcfa3ec680cc
Cancelling job 7b6607a8a5cdecaa7e88bcfa3ec680cc.
Cancelled job 7b6607a8a5cdecaa7e88bcfa3ec680cc.
[root@hadoop-01 conf]# flink list
Waiting for response...
No running jobs.
No scheduled jobs.
```

yarn-session.sh -n 3 -tm 1024 -s 2

## 2. yarn 方式

wget https://archive.apache.org/dist/flink/flink-1.11.1/flink-1.11.1-bin-scala_2.12.tgz
hadoop2.8.5
flink1.11.1

1. 解压
2. 环境变量配置

```bash
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export YARN_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_CLASSPATH=`hadoop classpath`
```

3. 测试 yarn-pre 提交
   `./bin/flink run -m yarn-cluster ./examples/batch/WordCount.jar`
4. Application Mode
   `./bin/flink run-application -t yarn-application ./examples/batch/WordCount.jar`
5. 提交 application mode 任务

```shell
./bin/flink run-application -t yarn-application \
hdfs://stream-hdfs/user/flink/app/stream-sync-1.0-SNAPSHOT.jar
```

flink run-application -t yarn-application -Dyarn.application.name="flink-sync-kafka" hdfs://stream-hdfs/user/flink/AppJars/stream-sync-kafka-1.0-SNAPSHOT.jar --source.topic test --sink.topic test1 -n 2

flink run-application -t yarn-application ./wzq/stream-sync-hive-1.0-SNAPSHOT.jar
