---
categories:
- 技术
- 大数据
date: '2021-04-06 18:52:02+08:00'
tags:
- flink
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725101125909.png
title: flink sql写入iceberg
---
Flink SQL写入iceberg

<!--more-->
### SQL-Client 操作
1. 启动命令
`sql-client.sh embedded -d $FLINK_HOME/conf/sql-client-hive.yaml -j flink_sql_client_conf/iceberg-flink-runtime-0.11.0.jar -j flink-1.11.1/lib/flink-sql-connector-hive-2.3.6_2.11-1.11.1.jar`
```sql
-- 创建数据模拟实时表
CREATE TABLE  default_catalog.default_database.person_score_datagen (
	id INT, 
	name STRING, 
	age INT,
	score INT,
	ts AS LOCALTIMESTAMP, 
	WATERMARK FOR ts AS ts ) 
WITH (
	'connector' = 'datagen',
	'rows-per-second' = '2',
	'fields.id.kind' = 'sequence',
	'fields.id.start' = '1',
	'fields.id.end' = '20',
	'fields.name.length' = '6',
	'fields.age.min' = '20',
	'fields.age.max' = '30',
	'fields.score.min' = '60',
	'fields.score.max' = '100'
);

-- 创建hadoop catalog
CREATE CATALOG hadoop_catalog WITH (
  'type'='iceberg',
  'catalog-type'='hadoop',
  'warehouse'='hdfs://stream-hdfs/data/iceberg',
  'property-version'='1'
);

-- 创建hadoop iceberg表
CREATE TABLE hadoop_catalog.iceberg_hadoop_db.person_score_iceberg (
	id INT, 
	name STRING, 
	age INT,
	score INT
);

-- 数据写入iceberg
insert into hadoop_catalog.iceberg_hadoop_db.person_score_iceberg select id,name,age,score from default_catalog.default_database.person_score_datagen;

-- 查询结果
select * from hadoop_catalog.iceberg_hadoop_db.person_score_iceberg;

```
2. 查询结果
![](https://www.azheimage.top/markdown-img-paste-20210325143156204.png)

### 将hadoop iceberg表导入到hive表中
1. 启动hive
2. 创建外部表讲iceberg表目录加载到hive
```sql
-- 建库
create database if not exists iceberg_hadoop_db;
-- 切换库
use iceberg_hadoop_db; 
-- 创建外部表
CREATE EXTERNAL TABLE person_score_iceberg_hive
STORED BY 'org.apache.iceberg.mr.hive.HiveIcebergStorageHandler' 
LOCATION 'hdfs://stream-hdfs/data/iceberg/iceberg_hadoop_db/person_score_iceberg';
-- 查询结果
select * from person_score_iceberg_hive;
```
![](https://www.azheimage.top/markdown-img-paste-20210325145636416.png)
```sql
-- hive写iceberg表
insert into person_score_iceberg_hive values (21,'test hive insert',29,99);
```











