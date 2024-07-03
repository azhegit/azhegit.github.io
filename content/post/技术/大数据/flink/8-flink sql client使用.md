---
categories:
- 技术
- 大数据
date: '2021-03-10 17:18:05+08:00'
tags:
- flink
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110143922992.png
title: 8-flink sql client使用
---
SQL 客户端

Flink 的 Table & SQL API 可以处理 SQL 语言编写的查询语句，但是这些查询需要嵌入用 Java 或 Scala 编写的表程序中。
<!--more-->

此外，这些程序在提交到集群前需要用构建工具打包。这或多或少限制了 Java/Scala 程序员对 Flink 的使用。

SQL 客户端 的目的是提供一种简单的方式来编写、调试和提交表程序到 Flink 集群上，而无需写一行 Java 或 Scala 代码。SQL 客户端命令行界面（CLI） 能够在命令行中检索和可视化分布式应用中实时产生的结果。

### 系统环境
- MAC OS
- flink1.12.0

### 运行环境
1. 启动集群
`start-cluster.sh`
![](https://www.azheimage.top/markdown-img-paste-20210310153154622.png)
2. 启动SQL-Client
`sql-client.sh embedded`
![](https://www.azheimage.top/markdown-img-paste-20210310153306484.png)

### DataGen连接器
- DataGen 连接器允许按数据生成规则进行读取。
- DataGen 连接器可以使用计算列语法。 这使您可以灵活地生成记录。
- DataGen 连接器是内置的。
>注意 不支持复杂类型: Array，Map，Row。 请用计算列构造这些类型。

#### SQL-Client DataGen建表语句
```sql
-- 删除表定义
drop table if exists person_score_datagen;
-- 创建表定义
CREATE TABLE if not exists person_score_datagen (
	id INT, 
	name STRING, 
	age INT,
	score INT,
	ts AS LOCALTIMESTAMP, 
	WATERMARK FOR ts AS ts ) 
WITH (
	'connector' = 'datagen',
-- 	每秒生成的行数：2
	'rows-per-second' = '2',
-- 	字段id选用序列生成器
	'fields.id.kind' = 'sequence',
	'fields.id.start' = '1',
	'fields.id.end' = '20',
-- 	随机生成器生成字符的长度：6
	'fields.name.length' = '6',
	'fields.age.min' = '20',
	'fields.age.max' = '30',
-- 	随机生成器的最小值：1
	'fields.score.min' = '60',
-- 	随机生成器的最大值：100
	'fields.score.max' = '100'
);
```

#### DataGen 连接器 参数
参数|是否必选|默认参数|数据类型|描述
-|-|-|-|-
connector|必须|(none)|String|指定要使用的连接器，这里是 'datagen'。
rows-per-second|可选|10000|Long|每秒生成的行数，用以控制数据发出速率。
fields.#.kind|可选|random|String|指定 '#' 字段的生成器。可以是 'sequence' 或 'random'。
fields.#.min|可选|(Minimum value of type)|(Type of field)|随机生成器的最小值，适用于数字类型。
fields.#.max|可选|(Maximum value of type)|(Type of field)|随机生成器的最大值，适用于数字类型。
fields.#.length|可选|100|Integer|随机生成器生成字符的长度，适用于 char、varchar、string。
fields.#.start|可选|(none)|(Type of field)|序列生成器的起始值。
fields.#.end|可选|(none)|(Type of field)|序列生成器的结束值。

#### 查询结果
```sql
select * from person_score_datagen;
```
![](https://www.azheimage.top/markdown-img-paste-20210310154832547.png)


### MySQL连接器
#### 依赖包
1. maven依赖
```xml
<dependency>
  <groupId>org.apache.flink</groupId>
  <artifactId>flink-connector-jdbc_2.11</artifactId>
  <version>1.12.0</version>
</dependency>
```
2. 启动Jar包依赖
- flink-connector-jdbc_2.11-1.12.0.jar
- mysql-connector-java-5.1.40.jar

#### MySQL建表语句
```sql
DROP TABLE IF EXISTS `person_score`;
CREATE TABLE `person_score` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `pid` bigint(20) NOT NULL COMMENT '一个批次内顺序id',
  `name` varchar(32) NOT NULL COMMENT '姓名',
  `age` int(3) NOT NULL COMMENT '年龄',
  `score` int(5) NOT NULL COMMENT '得分',
  `creator` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '创建者',
  `gmt_create` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modify` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='人员分数表';

INSERT INTO person_score( `pid`, `name`, `age`, `score`, `creator`) VALUES ( 1, 'test', 66, 100, 'Init');
```

#### SQL-Client JDBC建表语句
```sql
-- 删除定义表
drop table if exists person_score_mysql;

CREATE TABLE if not exists person_score_mysql (
	pid BIGINT,
  name STRING, 
	age INT,
	score INT,
	creator STRING
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://stream-dev:3306/dev',
    'table-name' = 'person_score',
    'driver' = 'com.mysql.jdbc.Driver',
    'username' = 'root',
    'password' = 'mysql@123',
    'lookup.cache.max-rows' = '5',
    'lookup.cache.ttl' = '10s'
);

select * from person_score_mysql;
```
![](https://www.azheimage.top/markdown-img-paste-20210310164118771.png)

![](https://www.azheimage.top/markdown-img-paste-2021031016413024.png)

#### JDBC 连接器 参数
参数|是否必选|默认参数|数据类型|描述
-|-|-|-|-|-
connector|必选的|(none)|String|指定要使用的连接器，此处应为'jdbc'。
url|必选的|(none)|String|JDBC数据库URL。
table-name|必选的|(none)|String|要连接的JDBC表的名称。
driver|可选的|(none)|String|用于连接到该URL的JDBC驱动程序的类名，如果未设置，它将自动从URL派生。
username|可选的|(none)|String|JDBC用户名。如果同时指定了两者'username'，则'password'必须同时指定两者。
password|可选的|(none)|String|JDBC密码。
scan.partition.column|可选的|(none)|String|用于对输入进行分区的列名。有关更多详细信息，请参见以下“分区扫描”部分。
scan.partition.num|可选的|(none)|Integer|分区数。
scan.partition.lower-bound|可选的|(none)|Integer|第一个分区的最小值。
scan.partition.upper-bound|可选的|(none)|Integer|最后一个分区的最大值。
scan.fetch-size|可选的|0|Integer|每次往返读取时应从数据库中获取的行数。如果指定的值为零，则忽略提示。
scan.auto-commit|可选的|true|Boolean|在JDBC驱动程序上设置自动提交标志，该标志确定是否在事务中自动提交每个语句。一些JDBC驱动程序，特别是 Postgres，可能要求将此设置为false以便流式传输结果。
lookup.cache.max-rows|可选的|(none)|Integer|查找缓存的最大行数（超过此值），最旧的行将过期。默认情况下，查找缓存处于禁用状态。有关更多详细信息，请参见下面的“查找缓存”部分。
lookup.cache.ttl|可选的|(none)|Duration|查找缓存中每一行的最长生存时间，在这段时间内，最旧的行将过期。默认情况下，查找缓存处于禁用状态。有关更多详细信息，请参见下面的“查找缓存”部分。
lookup.max-retries|可选的|3|Integer|查找数据库失败时的最大重试时间。
sink.buffer-flush.max-rows|可选的|100|Integer|刷新前缓冲记录的最大大小。可以设置为零以禁用它。
sink.buffer-flush.interval|可选的|1s|Duration|刷新间隔不断变化，在这段时间内，异步线程将刷新数据。可以设置'0'为禁用它。注意，'sink.buffer-flush.max-rows'可以将其设置为'0'刷新间隔设置，以允许对缓冲的动作进行完全异步处理。
sink.max-retries|可选的|3|Integer|如果将记录写入数据库失败，则最大重试时间。

### SQL-Client 插入数据到MySQL
```sql
insert into person_score_mysql
SELECT id as pid, name, age, score,'sql-client' FROM person_score_datagen;
```
![](https://www.azheimage.top/markdown-img-paste-20210310170606182.png)
执行结果
![](https://www.azheimage.top/markdown-img-paste-20210310170631719.png)
Flink UI
![](https://www.azheimage.top/markdown-img-paste-20210310170757115.png)



