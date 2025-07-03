---
categories:
- 技术
- 大数据
date: 2018-10-11 15:18:38+08:00
tags:
- spark
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725100954649.png
title: 单机版spark搭建
---
快速搭建单机版spark
<!--more-->
### 单机版spark安装

1. 安装jdk
2. 安装Scala
3. 安装spark：
   1. 下载[spark2.3.1](https://archive.apache.org/dist/spark/spark-2.3.1/spark-2.3.1-bin-hadoop2.6.tgz)，解压spark
   2. cp conf/spark-env.sh.template conf/spark-env.sh
   3. 修改spark-env.sh
   ```
   export SCALA_HOME=/opt/scala-2.11.8
   export SPARK_MASTER_IP=poc3
   export JAVA_HOME=/usr/java/jdk1.8.0_171
   ```
   4. cp slaves.template slaves
   5. 修改slaves中localhost为poc3
   6. 启动master：`sbin/start-master.sh`
   7. 查看日志：`tail -f logs/spark-root-org.apache.spark.deploy.master.Master-1-poc3.out`
   日志内容：
   ```
   2018-09-13 23:27:31 INFO  MasterWebUI:54 - Bound   MasterWebUI to 0.0.0.0, and started at http://poc3:8080
   2018-09-13 23:27:31 INFO  Server:346 - jetty-9.3.z-SNAPSHOT
   2018-09-13 23:27:31 INFO  ContextHandler:781 - Started o.s.j.s.ServletContextHandler@180486e{/,null,AVAILABLE}
   2018-09-13 23:27:31 INFO  AbstractConnector:278 - Started ServerConnector@401e9bc4{HTTP/1.1,[http/1.1]}{poc3:6066}
   2018-09-13 23:27:31 INFO  Server:414 - Started @2818ms
   2018-09-13 23:27:31 INFO  Utils:54 - Successfully started service on port 6066.
   2018-09-13 23:27:31 INFO  StandaloneRestServer:54 - Started REST server for submitting applications on port 6066
   2018-09-13 23:27:32 INFO  ContextHandler:781 - Started o.s.j.s.ServletContextHandler@46eb7da5{/metrics/master/json,null,AVAILABLE,@Spark}
   2018-09-13 23:27:32 INFO  ContextHandler:781 - Started o.s.j.s.ServletContextHandler@28ca66a{/metrics/applications/json,null,AVAILABLE,@Spark}
   2018-09-13 23:27:32 INFO  Master:54 - I have been elected leader! New state: ALIVE
   ```
   8. 查看UI界面：http://poc3:8080
   ![](https://www.azheimage.top/markdown-img-paste-20180913233350912.png)
   9. 启动worker：sbin/start-slaves.sh
   ![](https://www.azheimage.top/markdown-img-paste-20180913233618709.png)
   10. 提交spark-submit测试：
   ```
   ./bin/spark-submit \
    --class org.apache.spark.examples.SparkPi \
    --master spark://poc3:7077 \
    --deploy-mode cluster \
    --num-executors 3 \
    --driver-memory 4g \
    --executor-memory 2g \
    --executor-cores 1 \
    --queue thequeue \
    ./examples/jars/spark-examples*.jar \
    10000
   ```
