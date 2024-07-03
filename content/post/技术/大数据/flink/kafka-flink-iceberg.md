---
categories:
- 技术
- 大数据
date: '2021-04-06 18:53:56+08:00'
tags:
- flink
thumbnailImage: //www.azheimage.top/markdown-img-paste-20210406193727690.png
title: kafka-flink-iceberg
---

kafka-flink-iceberg
模拟生成数据发送到kafka，读取kafka数据，通过flink写入iceberg
<!--more-->

### 1. kafka数据准备
1. 准备merge数据
`nohup  java -jar stream-mock-1.0-SNAPSHOT.jar -t test -e merge -r 5 -s 1 &`


### 2. SQL_client 
1. 启动flink
2. 启动sql_client
`sql-client.sh embedded -d $FLINK_HOME/conf/sql-client-hive.yaml -j flink_sql_client_conf/iceberg-flink-runtime-0.11.0.jar -j flink-1.11.1/lib/flink-sql-connector-hive-2.3.6_2.11-1.11.1.jar`
3. 建kafka源表表
```sql
use catalog myhive;

create database kafka_source;

CREATE TABLE kafka_source.merge_kafka_iceberg (
  carPlate STRING,
  plateColor INT,
  siteNo STRING,
  snapshotTime STRING,
  snapshotTimestamp BIGINT,
  snapshotDate STRING,
  direction INT,
  topic STRING,
  extractTime STRING,
  eventTime AS TO_TIMESTAMP(FROM_UNIXTIME(snapshotTimestamp / 1000,'yyyy-MM-dd HH:mm:ss')),
  WATERMARK FOR eventTime AS eventTime - INTERVAL '15' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'test',
  'properties.bootstrap.servers' = 'stream-server:9092',
  'properties.group.id' = 'sql_client_test_1',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'json',
  'json.fail-on-missing-field' = 'false',
  'json.ignore-parse-errors' = 'true'
);

select * from myhive.kafka_source.merge_kafka;
```

### 创建iceberg表
```sql
-- 创建iceberg&hive catalog
CREATE CATALOG iceberg_hive_catalog WITH (
  'type'='iceberg',
  'catalog-type'='hive',
  'uri'='thrift://hadoop-dev-1:9083',
  'clients'='5',
  'property-version'='1',
  'warehouse'='hdfs://stream-hdfs/user/hive/warehouse'
);
-- 切换catalog
use catalog iceberg_hive_catalog;

use iceberg_hive_db;
-- 创建iceberg表
-- CREATE TABLE merge_iceberg_partition_1 (
--   carPlate STRING,
--   plateColor INT,
--   siteNo STRING,
--   snapshotTime STRING,
--   snapshotTimestamp BIGINT,
--   snapshotDate STRING,
--   direction INT,
--   topic STRING,
--   extractTime STRING
-- ) PARTITIONED BY (snapshotDate);

-- 创建表如果是要跟hive打通，需要用javaAPI建表
  
INSERT into iceberg_hive_catalog.iceberg_hive_db.merge_iceberg_partition SELECT carPlate,plateColor,siteNo,snapshotTime,snapshotTimestamp,snapshotDate,direction,topic,extractTime from myhive.kafka_source.merge_kafka;

-- insert into merge_iceberg_partition values('晋B329SL',1,'G009233001000910020','2021-03-22 17:09:36',1616404176933,'20210322',1,'mock','2021-03-22 17:09:36');
```

### mock数据
```bash
usage: Kafka producer Application [-b <kafkaProp>] [-e <arg>] [-h] [-l]
       [-r <arg>] [-s <arg>] -t <arg>
 -b,--bootstrap.servers <kafkaProp>   kafka bootstrap servers.
                                      <string>
                                      eg:-b 1.1.1.1:9092,1.1.1.2:9092
 -e,--entity <arg>                    mock entity: speed/radar/default.
                                      <string>
                                      eg:-e speed
 -h,--help                            Print help
 -l,--logPrint                        Whether to print logs. eg:-l
 -r,--recordSize <arg>                record size.
                                      <int>
                                      eg:-r 1
 -s,--sleepSecond <arg>               sleep second.
                                      <double>
                                      eg:-s 0.01
 -t,--topic <arg>                     send records to kafka topic.
                                      <string>
                                      eg:-t test

<!-- 4天的数据量 60*60*24*4/0.2=1728000 -->

[admin@stream-server mock]$ nohup java -jar stream-mock-1.0-SNAPSHOT.jar -t test -e merge -r 1728000 -s 0.2 &
```



### 遇到问题
1. kafka数据已经写入了data目录，但是查不到结果
>没有开启checkpoint，`vim flink-conf.yaml`
```shell
# state.backend: filesystem
state.backend: filesystem

# state.checkpoints.dir: hdfs://namenode-host:port/flink-checkpoints
state.checkpoints.dir: hdfs://stream-hdfs/sql-client/flink-checkpoints

# state.savepoints.dir: hdfs://namenode-host:port/flink-checkpoints
state.savepoints.dir: hdfs://stream-hdfs/sql-client/flink-checkpoints

# state.backend.incremental: false
state.backend.incremental: false
execution.checkpointing.interval: 5s
```













