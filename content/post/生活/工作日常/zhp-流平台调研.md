---
categories:
- 生活
date: '2024-01-03 13:02:49+08:00'
tags:
- 工作日常
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180831191033396.png
title: zhp-流平台调研
---

[flink-streaming-platform-web](https://github.com/zhp8341/flink-streaming-platform-web)系统是基于 flink 封装的一个可视化的 web 系统
[toc]

<!--more-->

## 一、简介

[flink-streaming-platform-web](https://github.com/zhp8341/flink-streaming-platform-web)系统是基于 flink 封装的一个可视化的 web 系统，用户只需在 web 界面进行 sql 配置就能完成流计算任务，
主要功能包含任务配置、启/停任务、告警、日志等功能。目的是减少开发，完全实现 flink-sql 流计算任务

flink 任务支持单流 双流 单流与维表等

<font color=red size=5>支持本地模式、yarn-per 模式、STANDALONE 模式 </font >

**支持 udf、自定义连接器等,完全兼容官方连接器**

## 二、部署

#### 1. 环境

- 操作系统：Centos7
- hadoop 版本 2.8.5
- flink 版本 1.12.0
- jdk 版本 1.8.0_171
- scala 版本 2.11
- kafka 版本 1.1.1
- mysql 版本 5.7.22

#### 2. 平台安装准备工作

**hadoop2.8.5 已经安装好了**
平台支持 3 种模式：YARN_PER、LOCAL、STANDALONE

1. flink 客户端安装
   下载对应版本 [flink-1.12.0-bin-scala_2.11.tgz](https://www.apache.org/dyn/closer.lua/flink/flink-1.12.0/flink-1.12.0-bin-scala_2.11.tgz) 然后解压

2. YARN_PER 模式，需要准备 hadoop 配置文件`core-site.xml`,`yarn-site.xml`,`hdfs-site.xml`放在 conf 目录下，LOCAL 模式，STANDALONE 模式不需要,因为机器已经有 hadoop 环境，直接添加软链
   ```
   ln -s /opt/hadoop/hadoop-2.8.5/etc/hadoop/core-site.xml core-site.xml
   ln -s /opt/hadoop/hadoop-2.8.5/etc/hadoop/yarn-site.xml yarn-site.xml
   ln -s /opt/hadoop/hadoop-2.8.5/etc/hadoop/hdfs-site.xml hdfs-site.xml
   ```
3. 修改`flink-conf.yaml`，三种模式都需要,开启 classloader.resolve-order 并且设置**classloader.resolve-order: parent-first**

4. 下载[flink-shaded-hadoop-2-uber-2.7.5-10.0.jar](https://repo.maven.apache.org/maven2/org/apache/flink/flink-shaded-hadoop-2-uber/2.7.5-10.0/flink-shaded-hadoop-2-uber-2.7.5-10.0.jar)到/flink-1.12.0/lib 集成 hadoop

5. 配置环境变量 HADOOP_CLASSPATH
   ```
   export HADOOP_CLASSPATH=`hadoop classpath`
   ```

#### 3. flink-streaming-platform-web 安装

1. 下载最新[release 版本](https://github.com/zhp8341/flink-streaming-platform-web/releases/) 并且解压
2. 创建数据库 数据库名：flink_web，执行建表语句，[脚本地址](https://github.com/zhp8341/flink-streaming-platform-web/blob/master/docs/sql/flink_web.sql)

3. 修改数据库连接配置/flink-streaming-platform-web/conf/application.properties

4. 启动，bin/deploy.sh start

#### 4. flink-streaming-platform-web 使用

1. 登录地址：http://hadoop-dev-5:9084，用户名/密码：admin/123456
   ![](https://www.azheimage.top/markdown-img-paste-20210108152926902.png)
2. 登录首页：
   ![](https://www.azheimage.top/markdown-img-paste-20210108153017133.png)
3. 系统设置，修改配置
   ![](https://www.azheimage.top/markdown-img-paste-20210108164203759.png)

#### 5. 准备 connector 相关 jar 包

1. demo 演示用 SQL，读取 kafka，写入 mysql
   mysql-connector-java-5.1.40.jar
   flink-connector-jdbc_2.11-1.12.0.jar
   flink-sql-connector-kafka_2.11-1.12.0.jar

#### 6. SQLdemo 演示

---

##### 1. Demo1 单流 kafka 写入 mysql 参考

1. [demo 内容地址](https://github.com/zhp8341/flink-streaming-platform-web/blob/master/docs/sql_demo/demo_1.md)
2. 创建 topic
   `kafka-topic-create.sh flink_test_4 1 1`
3. mysql 建表

```sql
CREATE TABLE sync_test_1 (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `day_time` varchar(64) DEFAULT NULL,
  `total_gmv` bigint(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uidx` (`day_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
```

4. 配置语句

```sql
create table flink_test_1 (
  id BIGINT,
  day_time VARCHAR,
  amnount BIGINT,
  proctime AS PROCTIME ()
)
 with (
 'connector.properties.zookeeper.connect'='hadoop-dev-1:2181,hadoop-dev-2:2181,hadoop-dev-3:2181',
  'connector.version'='universal',
  'connector.topic'='flink_test_4',
  'connector.startup-mode'='earliest-offset',
  'format.derive-schema'='true',
  'connector.type'='kafka',
  'update-mode'='append',
  'connector.properties.bootstrap.servers'='hadoop-dev-1:9092,hadoop-dev-2:9092,hadoop-dev-3:9092',
  'connector.properties.group.id'='flink_gp_test1',
  'format.type'='json'
 );

CREATE TABLE sync_test_1 (
                   day_time string,
                   total_gmv bigint
 ) WITH (
   'connector.type' = 'jdbc',
   'connector.url' = 'jdbc:mysql://stream-dev:3306/flink_web?characterEncoding=UTF-8',
   'connector.table' = 'sync_test_1',
   'connector.username' = 'root',
   'connector.password' = 'mysql@123'
 );

INSERT INTO sync_test_1
SELECT day_time,SUM(amnount) AS total_gmv
FROM flink_test_1
GROUP BY day_time;
```

5. 保存配置
   运行配置：`-yqu default   -yjm 1024m -ytm 2048m  -p 1  -ys 1`
   checkpoint 配置：`-checkpointInterval 5000 -checkpointDir   hdfs://stream-hdfs/flink/checkpoints/`
   ![](https://www.azheimage.top/markdown-img-paste-20210111103249178.png)
6. 开启配置，然后提交任务
   ![](https://www.azheimage.top/markdown-img-paste-20210108170215539.png)
   ![](https://www.azheimage.top/markdown-img-paste-20210108170234477.png)
7. 往 kafka 发送数据

```bash
[admin@hadoop-dev-1 ~]$ kafka-producer.sh flink_test_4
{"day_time": "20201009","id": 7,"amnount":20}
{"day_time": "20201010","id": 7,"amnount":20}
{"day_time": "20201011","id": 7,"amnount":20}
{"day_time": "20201010","id": 7,"amnount":20}
{"day_time": "20201011","id": 7,"amnount":20}
{"day_time": "20201011","id": 7,"amnount":20}
```

8. 去 MySQL 查看实时结果

---

##### 2. Demo2 双流 kafka 写入 mysql 参考

1. [demo 内容地址](https://github.com/zhp8341/flink-streaming-platform-web/tree/master/docs/sql_demo/demo_2.md)
2. 创建 topic

```
kafka-topic-create.sh flink_test_5_1 1 1
kafka-topic-create.sh flink_test_5_2 1 1
```

3. mysql 建表

```sql
CREATE TABLE `sync_test_2` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `day_time` varchar(64) DEFAULT NULL,
  `total_gmv` bigint(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uidx` (`day_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
```

4. 配置语句

```sql
create table flink_test_5_1 (
  id BIGINT,
  day_time VARCHAR,
  amnount BIGINT,
  proctime AS PROCTIME ()
)
 with (
  'connector.properties.zookeeper.connect'='hadoop-dev-1:2181,hadoop-dev-2:2181,hadoop-dev-3:2181',
   'connector.version'='universal',
   'connector.topic'='flink_test_5_1',
   'connector.startup-mode'='earliest-offset',
   'format.derive-schema'='true',
   'connector.type'='kafka',
   'update-mode'='append',
   'connector.properties.bootstrap.servers'='hadoop-dev-1:9092,hadoop-dev-2:9092,hadoop-dev-3:9092',
   'connector.properties.group.id'='flink_gp_test1',
   'format.type'='json'
 );


  create table flink_test_5_2 (
  id BIGINT,
  coupon_amnount BIGINT,
  proctime AS PROCTIME ()
)
 with (
  'connector.properties.zookeeper.connect'='hadoop-dev-1:2181,hadoop-dev-2:2181,hadoop-dev-3:2181',
   'connector.version'='universal',
   'connector.topic'='flink_test_5_2',
   'connector.startup-mode'='earliest-offset',
   'format.derive-schema'='true',
   'connector.type'='kafka',
   'update-mode'='append',
   'connector.properties.bootstrap.servers'='hadoop-dev-1:9092,hadoop-dev-2:9092,hadoop-dev-3:9092',
   'connector.properties.group.id'='flink_gp_test1',
   'format.type'='json'
 );


CREATE TABLE sync_test_2 (
                   day_time string,
                   total_gmv bigint
 ) WITH (
   'connector.type' = 'jdbc',
   'connector.url' = 'jdbc:mysql://stream-dev:3306/flink_web?characterEncoding=UTF-8',
   'connector.table' = 'sync_test_2',
   'connector.username' = 'root',
   'connector.password' = 'mysql@123'
 );

INSERT INTO sync_test_2
SELECT
  day_time,
  SUM(amnount - coupon_amnount) AS total_gmv
FROM
  (
    SELECT
      a.day_time as day_time,
      a.amnount as amnount,
      b.coupon_amnount as coupon_amnount
    FROM
      flink_test_5_1 as a
      LEFT JOIN flink_test_5_2 b on b.id = a.id
  )
GROUP BY
  day_time;
```

5. 保存配置
   运行配置：`-yqu default   -yjm 1024m -ytm 2048m  -p 1  -ys 1`
   checkpoint 配置：`-checkpointInterval 5000 -checkpointDir   hdfs://stream-hdfs/flink/checkpoints/`
   ![](https://www.azheimage.top/markdown-img-paste-20210112104835734.png)
6. 开启配置，然后提交任务
   ![](https://www.azheimage.top/markdown-img-paste-20210108170215539.png)
   ![](https://www.azheimage.top/markdown-img-paste-20210108170234477.png)
7. 往 kafka 发送数据

```bash
[admin@hadoop-dev-1 ~]$ kafka-producer.sh flink_test_5_1
{"day_time": "20201011","id": 8,"amnount":211}
{"day_time": "20201011","id": 8,"amnount":99}

[admin@hadoop-dev-1 ~]$ kafka-producer.sh flink_test_5_2
{"id": 8,"coupon_amnount":100}
{"id": 8,"coupon_amnount":10}
{"id": 8,"coupon_amnount":200}
```

8. 去 MySQL 查看实时结果

---

##### 3. Demo3 kafka 和 mysql 维表实时关联写入 mysql 参考

1. [demo 内容地址](https://github.com/zhp8341/flink-streaming-platform-web/tree/master/docs/sql_demo/demo_3.md)
2. 创建 topic

```
kafka-topic-create.sh flink_test_6 1 1
```

3. mysql 建表

```sql
CREATE TABLE `test_dim` (
  `id` bigint(11) NOT NULL,
  `coupon_amnount` bigint(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of test_dim
-- ----------------------------
BEGIN;
INSERT INTO `test_dim` VALUES (1, 1);
INSERT INTO `test_dim` VALUES (3, 1);
INSERT INTO `test_dim` VALUES (8, 1);
COMMIT;

CREATE TABLE `sync_test_3` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `day_time` varchar(64) DEFAULT NULL,
  `total_gmv` bigint(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uidx` (`day_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

```

4. 配置语句

```sql
create table flink_test_6 (
  id BIGINT,
  day_time VARCHAR,
  amnount BIGINT,
  proctime AS PROCTIME ()
)
 with (
  'connector.properties.zookeeper.connect'='hadoop-dev-1:2181,hadoop-dev-2:2181,hadoop-dev-3:2181',
   'connector.version'='universal',
   'connector.topic'='flink_test_6',
   'connector.startup-mode'='earliest-offset',
   'format.derive-schema'='true',
   'connector.type'='kafka',
   'update-mode'='append',
   'connector.properties.bootstrap.servers'='hadoop-dev-1:9092,hadoop-dev-2:9092,hadoop-dev-3:9092',
   'connector.properties.group.id'='flink_gp_test1',
   'format.type'='json'
 );


create table flink_test_6_dim (
  id BIGINT,
  coupon_amnount BIGINT
)
 with (
   'connector.type' = 'jdbc',
   'connector.url' = 'jdbc:mysql://stream-dev:3306/flink_web?characterEncoding=UTF-8',
   'connector.table' = 'test_dim',
   'connector.username' = 'root',
   'connector.password' = 'mysql@123',
   'connector.lookup.max-retries' = '3'
 );


CREATE TABLE sync_test_3 (
                   day_time string,
                   total_gmv bigint
 ) WITH (
   'connector.type' = 'jdbc',
   'connector.url' = 'jdbc:mysql://stream-dev:3306/flink_web?characterEncoding=UTF-8',
   'connector.table' = 'sync_test_3',
   'connector.username' = 'root',
   'connector.password' = 'mysql@123'
 );


INSERT INTO sync_test_3
SELECT
  day_time,
  SUM(amnount - coupon_amnount) AS total_gmv
FROM
  (
    SELECT
      a.day_time as day_time,
      a.amnount as amnount,
      b.coupon_amnount as coupon_amnount
    FROM
      flink_test_6 as a
      LEFT JOIN flink_test_6_dim  FOR SYSTEM_TIME AS OF  a.proctime  as b
     ON b.id = a.id
  )
GROUP BY day_time;
```

5. 保存配置
   运行配置：`-yqu default   -yjm 1024m -ytm 2048m  -p 1  -ys 1`
   checkpoint 配置：`-checkpointInterval 5000 -checkpointDir   hdfs://stream-hdfs/flink/checkpoints/`
6. 开启配置，然后提交任务
7. 往 kafka 发送数据

```bash
[admin@hadoop-dev-1 ~]$ kafka-producer.sh flink_test_6
{"day_time": "20201011","id": 8,"amnount":211}
{"day_time": "20201011","id": 8,"amnount":101}

```

8. 去 MySQL 查看实时结果

---

##### 4. Demo4 滚动窗口

1. [demo 内容地址](https://github.com/zhp8341/flink-streaming-platform-web/tree/master/docs/sql_demo/demo_4.md)
2. 创建 topic

```
kafka-topic-create.sh flink_test_9 1 1
```

3. mysql 建表

```sql
CREATE TABLE `sync_test_tumble_output` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `window_start` datetime DEFAULT NULL,
  `window_end` datetime DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `clicks` bigint(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_uk` (`window_start`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
```

4. 配置语句

```sql
-- -- 开启 mini-batch （相关配置说明 https://ci.apache.org/projects/flink/flink-docs-release-1.10/zh/dev/table/config.html）
SET table.exec.mini-batch.enabled=true;
-- -- mini-batch的时间间隔，即作业需要额外忍受的延迟
SET table.exec.mini-batch.allow-latency=36000s;
-- -- 一个 mini-batch 中允许最多缓存的数据
SET table.exec.mini-batch.size=1000;

create table user_clicks (
 username varchar,
 click_url varchar,
 ts BIGINT,
 ts2 AS TO_TIMESTAMP(FROM_UNIXTIME(ts / 1000, 'yyyy-MM-dd HH:mm:ss')),
 WATERMARK FOR ts2 AS ts2 - INTERVAL '5' SECOND

)
with (
 'connector.properties.zookeeper.connect'='hadoop-dev-1:2181,hadoop-dev-2:2181,hadoop-dev-3:2181',
 'connector.version'='universal',
 'connector.topic'='flink_test_9',
 'connector.startup-mode'='earliest-offset',
 'format.derive-schema'='true',
 'connector.type'='kafka',
 'update-mode'='append',
 'connector.properties.bootstrap.servers'='hadoop-dev-1:9092,hadoop-dev-2:9092,hadoop-dev-3:9092',
 'connector.properties.group.id'='flink_gp_test1',
 'format.type'='json'
);


CREATE TABLE sync_test_tumble_output (
        window_start TIMESTAMP(3),
         window_end TIMESTAMP(3),
         username VARCHAR,
         clicks BIGINT
) WITH (
  'connector.type' = 'jdbc',
  'connector.url' = 'jdbc:mysql://stream-dev:3306/flink_web?characterEncoding=UTF-8',
  'connector.table' = 'sync_test_tumble_output',
  'connector.username' = 'root',
  'connector.password' = 'mysql@123'
);


INSERT INTO sync_test_tumble_output
SELECT
TUMBLE_START(ts2, INTERVAL '60' SECOND) as window_start,
TUMBLE_END(ts2, INTERVAL '60' SECOND) as window_end,
username,
COUNT(click_url)
FROM user_clicks
GROUP BY TUMBLE(ts2, INTERVAL '60' SECOND), username;
```

5. 保存配置
   运行配置：`-yqu default   -yjm 1024m -ytm 2048m  -p 1  -ys 1`
   checkpoint 配置：`-checkpointInterval 5000 -checkpointDir   hdfs://stream-hdfs/flink/checkpoints/`
6. 开启配置，然后提交任务
7. 往 kafka 发送数据

```bash
[admin@hadoop-dev-1 ~]$ kafka-producer.sh flink_test_9
{"username":"zhp","click_url":"http://xxx/","ts":1602295200000}
{"username":"zhp","click_url":"http://xxx/","ts":1602295210000}
{"username":"zhp","click_url":"http://xxx/","ts":1602295270000}
{"username":"zhp","click_url":"http://xxx/","ts":1602295310000}

```

8. 去 MySQL 查看实时结果

---

##### 5. Demo5 滑动窗口

1. [demo 内容地址](https://github.com/zhp8341/flink-streaming-platform-web/tree/master/docs/sql_demo/demo_5.md)
2. 创建 topic

```
kafka-topic-create.sh flink_test_10 1 1
```

3. mysql 建表

```sql
CREATE TABLE `sync_test_hop_output` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `window_start` datetime DEFAULT NULL,
  `window_end` datetime DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `clicks` bigint(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_uk` (`window_start`) USING BTREE
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;
```

4. 配置语句

```sql
-- -- 开启 mini-batch （相关配置说明 https://ci.apache.org/projects/flink/flink-docs-release-1.10/zh/dev/table/config.html）
SET table.exec.mini-batch.enabled=true;
-- -- mini-batch的时间间隔，即作业需要额外忍受的延迟
SET table.exec.mini-batch.allow-latency=60s;
-- -- 一个 mini-batch 中允许最多缓存的数据
SET table.exec.mini-batch.size=1000;

create table user_clicks (
username varchar,
click_url varchar,
ts BIGINT,
ts2 AS TO_TIMESTAMP(FROM_UNIXTIME(ts / 1000, 'yyyy-MM-dd HH:mm:ss')),
WATERMARK FOR ts2 AS ts2 - INTERVAL '5' SECOND

)
with (
'connector.properties.zookeeper.connect'='hadoop-dev-1:2181,hadoop-dev-2:2181,hadoop-dev-3:2181',
'connector.version'='universal',
'connector.topic'='flink_test_10',
'connector.startup-mode'='earliest-offset',
'format.derive-schema'='true',
'connector.type'='kafka',
'update-mode'='append',
'connector.properties.bootstrap.servers'='hadoop-dev-1:9092,hadoop-dev-2:9092,hadoop-dev-3:9092',
'connector.properties.group.id'='flink_gp_test1',
'format.type'='json'
);


CREATE TABLE sync_test_hop_output (
     window_start TIMESTAMP(3),
     window_end TIMESTAMP(3),
     username VARCHAR,
     clicks BIGINT
) WITH (
'connector.type' = 'jdbc',
'connector.url' = 'jdbc:mysql://stream-dev:3306/flink_web?characterEncoding=UTF-8',
'connector.table' = 'sync_test_hop_output',
'connector.username' = 'root',
'connector.password' = 'mysql@123'
);


INSERT INTO sync_test_hop_output
SELECT
HOP_START (ts2, INTERVAL '30' SECOND, INTERVAL '1' MINUTE) as window_start,
HOP_END (ts2, INTERVAL '30' SECOND, INTERVAL '1' MINUTE) as window_end,
username,
COUNT(click_url)
FROM user_clicks
GROUP BY HOP (ts2, INTERVAL '30' SECOND, INTERVAL '1' MINUTE), username;
```

5. 保存配置
   运行配置：`-yqu default   -yjm 1024m -ytm 2048m  -p 1  -ys 1`
   checkpoint 配置：`-checkpointInterval 5000 -checkpointDir   hdfs://stream-hdfs/flink/checkpoints/`
6. 开启配置，然后提交任务
7. 往 kafka 发送数据

```bash
[admin@hadoop-dev-1 ~]$ kafka-producer.sh flink_test_6
{"username":"wzq","click_url":"http://xxx/","ts":1602295200000}
{"username":"wzq","click_url":"http://xxx/","ts":1602295210000}
{"username":"wzq","click_url":"http://xxx/","ts":1602295270000}
```

8. 去 MySQL 查看实时结果

---

##### 6. Demo6 SQL UDF

1. [demo 内容地址](https://github.com/zhp8341/flink-streaming-platform-web/tree/master/docs/sql_demo/demo_5.md)
2. 创建 topic

```
kafka-topic-create.sh flink_test_10 1 1
```

3. mysql 建表

```sql
CREATE TABLE `sync_test_hop_output` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `window_start` datetime DEFAULT NULL,
  `window_end` datetime DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `clicks` bigint(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_uk` (`window_start`) USING BTREE
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;
```

4. 配置语句

```sql
-- -- 开启 mini-batch （相关配置说明 https://ci.apache.org/projects/flink/flink-docs-release-1.10/zh/dev/table/config.html）
SET table.exec.mini-batch.enabled=true;
-- -- mini-batch的时间间隔，即作业需要额外忍受的延迟
SET table.exec.mini-batch.allow-latency=60s;
-- -- 一个 mini-batch 中允许最多缓存的数据
SET table.exec.mini-batch.size=1000;

create table user_clicks (
username varchar,
click_url varchar,
ts BIGINT,
ts2 AS TO_TIMESTAMP(FROM_UNIXTIME(ts / 1000, 'yyyy-MM-dd HH:mm:ss')),
WATERMARK FOR ts2 AS ts2 - INTERVAL '5' SECOND

)
with (
'connector.properties.zookeeper.connect'='hadoop-dev-1:2181,hadoop-dev-2:2181,hadoop-dev-3:2181',
'connector.version'='universal',
'connector.topic'='flink_test_10',
'connector.startup-mode'='earliest-offset',
'format.derive-schema'='true',
'connector.type'='kafka',
'update-mode'='append',
'connector.properties.bootstrap.servers'='hadoop-dev-1:9092,hadoop-dev-2:9092,hadoop-dev-3:9092',
'connector.properties.group.id'='flink_gp_test1',
'format.type'='json'
);


CREATE TABLE sync_test_hop_output (
     window_start TIMESTAMP(3),
     window_end TIMESTAMP(3),
     username VARCHAR,
     clicks BIGINT
) WITH (
'connector.type' = 'jdbc',
'connector.url' = 'jdbc:mysql://stream-dev:3306/flink_web?characterEncoding=UTF-8',
'connector.table' = 'sync_test_hop_output',
'connector.username' = 'root',
'connector.password' = 'mysql@123'
);


INSERT INTO sync_test_hop_output
SELECT
HOP_START (ts2, INTERVAL '30' SECOND, INTERVAL '1' MINUTE) as window_start,
HOP_END (ts2, INTERVAL '30' SECOND, INTERVAL '1' MINUTE) as window_end,
username,
COUNT(click_url)
FROM user_clicks
GROUP BY HOP (ts2, INTERVAL '30' SECOND, INTERVAL '1' MINUTE), username;
```

5. 保存配置
   运行配置：`-yqu default   -yjm 1024m -ytm 2048m  -p 1  -ys 1`
   checkpoint 配置：`-checkpointInterval 5000 -checkpointDir   hdfs://stream-hdfs/flink/checkpoints/`
6. 开启配置，然后提交任务
7. 往 kafka 发送数据

```bash
[admin@hadoop-dev-1 ~]$ kafka-producer.sh flink_test_6
>{"day_time": "20201011","id": 8,"amnount":211}
>{"day_time": "20201011","id": 8,"amnount":101}

```

8. 去 MySQL 查看实时结果
