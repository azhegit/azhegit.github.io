---
categories:
  - 技术
  - 大数据
date: "2023-08-15 19:59:56+08:00"
tags:
  - aws
thumbnailImage: //www.azheimage.top/markdown-img-paste-20181113164516536.png
title: airflow_etl_demo
---

## 步骤一：准备数据目录及数据文件，建表及加载数据

gavin_demo_database

<!--more-->

1. 下载 hdfs 文件
2. S3 创建 tmp 目录：database/external/temp/temp_app_trace_log_new/
3. 上传已下载的文件到 tmp 目录
4. 创建目录`s3://gavin-data-demo/database/external/temp/temp_app_trace_log_new/ds=2023-07-19/hh=00/`
5. 复制 tmp 文件到表分区目录下
6. Athena 建表及相关查询语句

```sql
DROP TABLE IF EXISTS  `temp_app_trace_log_new`;

create external table IF NOT EXISTS gavin_demo_database.temp_app_trace_log_new(
  log_data string
  )PARTITIONED BY (ds string, hh string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
location 's3://gavin-data-demo/database/external/temp/temp_app_trace_log_new/'
TBLPROPERTIES ('has_encrypted_data'='false')
;

msck repair table temp_app_trace_log_new ;

select count(1) from gavin_demo_database.temp_app_trace_log_new;
```

## 步骤二：insert into

1. 创建表

```sql
create external table IF NOT EXISTS gavin_demo_database.temp_app_trace_log_new_10(
  log_data string
  )PARTITIONED BY (ds string, hh string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
location 's3://gavin-data-demo/database/temp_app_trace_log_new_10'
TBLPROPERTIES ('has_encrypted_data'='false')
;
```

方案一： 2. insert into 临时分区

```sql
insert into   temp_app_trace_log_new_10
select log_data,'2023-07-19' as ds,'00_tmp' as hh from temp_app_trace_log_new limit 10;
```

3. 删除分区

```sql
ALTER TABLE temp_app_trace_log_new_10
PARTITION (ds='2023-07-19',  hh='00_tmp') RENAME TO PARTITION (ds='2023-07-19', hh='00');
```

4. 手动删除 S3 原分区数据及分区

```sql
ALTER TABLE temp_app_trace_log_new_10
DROP if EXISTS  PARTITION (ds='2023-07-19', hh='00');
```

5. 重命名分区

```sql
ALTER TABLE temp_app_trace_log_new_10
PARTITION (ds='2023-07-19',  hh='00_tmp') RENAME TO PARTITION (ds='2023-07-19', hh='00');
```

方案二：

1. 使用 unload 将数据文件写入某个目录
2. 删除原来表中数据
3. 移动新数据到原表中目录

方案三：

1. 手动删除 S3 要插入的分区目录下文件
2. 再执行插入

下面的命令将创建一张名为 tmp_for_update 的表，表中内容是 testdb.testtable 表中内容的子集(根据条件过滤了部分记录)

CREATE TABLE testdb.tmp_for_update

WITH (

      external_location = 's3://xxx/yyy/tmp_for_update',

      parquet_compression = 'lzo')

AS select \* from testdb.testtable where [Filter conditions];

3. 将原表对应的数据文件删除；再拷入临时表中的数据文件

aws s3 rm s3://xxx/yyy/testtable/ --recursive

aws s3 mv s3://xxx/yyy/tmp_for_update s3://xxx/yyy/testtable/ --recursive

此时原表中再查看，满足指定条件的记录已经不存在了

4.使用 aws athena 命令对临时表进行清理

drop table dw_rec_db.tmp_for_update;

aws s3 rm s3://rec-collect/db/tmp_for_update/ --recursive
