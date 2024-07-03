---
categories:
- 技术
- 数据库
date: 2018-06-06 18:53:27+08:00
tags:
- cassandra
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110144117219.png
title: cassandra笔记
---
Cassandra学习笔记
<!--more-->
<!-- toc -->
# cassandra笔记
---------

## 横向比较nosql数据库

### nosql数据库（not only sql），分布式
### 使用nosql的改变需求点
- 高并发读写请求
- 高容量和高效的存储需求
- 高扩展性和高可用性需求

##### 传统关系型数据库量大瓶颈，第一数据横向扩展能力低下，第二数据的高效路存储和访问的需求满足能力低

### nosql数据库特点：
- 易扩展
- 灵活的数据模型
- 高可用
- 大数据量高性能

### nosql根据数据模型4类：
- 键值存储（key-value) redis
- 面向表(table-oriented) hbase cassandra
- 面向文本(document-oriented) mongodb
- 面向图(graph-oriented) neo4j

### nosql趋势
![nosql趋势](https://www.azheimage.top/8fbd6f21cfde00c12a5ab3b787e449bd.png)
### nosql用户量
![nosql用户](https://www.azheimage.top/9792cbb72dc2c9d33500e406a4267cd0.png)
### 2018年最新的所有数据库排名前20
![top20](https://www.azheimage.top/3b5fbab314e54aa17d8f07ac2b0fd957.png)

## Cassandra快速入门

- 发展简史
两位从Amazon跳槽到Facebook的dynamo工程师完成的，Java语言编写。2009年1月成为Apache孵化项目
- Cassandra优点：
  1. 高度可扩展性
  2. 高度可用性，无单点故障，p2p去中心化处理
  3. nosql列簇实现
  4. 非常高的写入吞吐量和良好的读取吞吐量
  5. cql查询语言（0.8版本开始支持）
  6. 范围查询（键的范围）
  7. 可调节的一致性
  8. 灵活的模式
- Cassandra的应用场景（目前Apple，Facebook，ebay，360，饿了么,taobao）：
  1. 待处理的数据量很大
  2. 数据量超过关系型数据库的承载能力
  3. 大量集群

## Cassandra安装与运行

Cassandra目录结构
- bin 可执行脚本
- conf 配置
  Cassandra.yml 常用的配置参数：
    - cluster_name 集群的名字，默认Test Cluster
    - listen_address 监听的IP或主机，默认localhost
    - commitlog_directory commitlog的保存路径，压缩包方式保存
    - data_file_directories 数据文件的存放目录
    - save_caches_directory 缓存存放目录
    - commit_failure_policy(stop,stop_commit,ignore) 提交失败是的策略
    - disk_failure_policy(stop,stop_paranoid,best_offert,ignore) 磁盘故障
    - endpoint_snitch 定位节点喝路由请求
    - rpc_address 监听客户端链接的地址
    - seed_provider 需要联系的节点地址
    - compaction_throughput_mb_per_sec 限定特定吞吐量下的压缩速率，推荐16-32
    - memtable_total_space_in_mb 最大使用内存空间数量
    - concurrent_reads 并发读取数量
    - concurrent_writes 并发写数量
    - incremental_backuos 是否增量备份
    - snapshot_before_compaction 压缩前执行快照
- interface 接口
- Javadoc 帮助文档
- lib 依赖的jar包

## Cassandra数据模型与CQL查询语言
### Cassandra数据模型

- 列(Column)
	![column](https://www.azheimage.top/6f537d0eb1b0e7340613136d919ae3a2.png)
  ![column2](https://www.azheimage.top/cdffe51ce2a178214238bc0aefb7d19a.png)
- 超级列(Super Column)
  ![superColumn1](https://www.azheimage.top/290c5c344f0ccdf753260f4dd0f6b0c5.png)
  ![superColumn2](https://www.azheimage.top/752662de706a80558209b886e9b5001a.png)
- 列族(Column Familes)
  ![columnFamilies](https://www.azheimage.top/b0f0446c49ddea3b885d1fd8039c5527.png)
- 键空间(Keyspaces)
	![keyspaces](https://www.azheimage.top/03df71bc011d793cff9f83a6b7ce1cd2.png)
- 集群(Cluster)
  ![cluster](https://www.azheimage.top/75bab28b0ee0fd7c3ec2ee0d5a58110e.png)
- 复合键(Composite Keys)
  ![fuhejian](https://www.azheimage.top/ca2eb7e5591368e7d5126534329b7547.png)
- Cassandra与传统关系数据库差别
  ![chabie](https://www.azheimage.top/3f14721605f8e87d5f87520693f741d3.png)
- Cassandra的排序规则
- Cassandra数据设计实例
	![chabie](https://www.azheimage.top/acc8292fa808115138a5abbcf19d0b2f.png)

### CQL查询语言
  - CQL的概念
    - CQL基本含义
    ##### 概念：CQL是Cassandra Query Language的简称，CQL由类似SQL的语句组成，包括修改，查询，爆粗，变更数据的存储方式等等功能。每一行语句由（；）结束
    ```sql
    select * from mytable;
    update mytable set someColumn='Some Value' where columnName='Something Else';
    ```
    - 大小写不敏感
    ##### 忽略大小写：在CQL里，可以space，column和table的名称是忽略大小写的，除非用双引号”括起来，才是大小写敏感的。如果不用双引号括起来，即使CQL携程大小写，也会被保存位小写
    ##### CQL关键字是忽略大小写的，例如，关键字SELECT和select是等价的。用双引号引起来就变成大小写严格区分了
    ```sql
    CREATE TABLE test(
      Foo int PRIMARY KEY,
      "Bar" int
    )
    ```
    - 常用数据类型
		![leixing](https://www.azheimage.top/aa08ff827b620e1461730ea7d3c83663.png)
    - CQL命名规则
    ##### 需要字母或数字开头，满足正则表达式[a-zA-Z0-9_]*
    - CQL注释规则
    ##### 单行注释：使用--或者//注释内容
    ##### 多行注释：使用/\*\*注释内容\*\*/
    - CQL保留字
    ##### 正常不使用保留字，如果要使用，可以用“”括起来
    ![baoliuzi](https://www.azheimage.top/ae91ca547e4e53026d9ea6c897cbdf1e.png)
  - CQL数据定义语句
    ![ddl1](https://www.azheimage.top/453ba01ed1a4c1019da7a39174550381.png)
    - CREATE keyspace(创建keyspacce)
      语法：CREATE keyspace (if not exists)? <identifer> with <proteries>
      注意：ID恩替反而长度需要小鱼等于32，大小写敏感，可以使用双引号定义大小写敏感的名字
      ```sql
      create keyspace excelsior with replication={'class':'simplestrategy','replication_factor':3}
      create keyspace excalibur with replication={'class':'networktopoligystrategy','DC1':1,'DC2':3} and durable_writes=false;
      ```
      ![ddl2](https://www.azheimage.top/d559cfcfa9f77ce0396849d3568287fb.png)
    - use keyspace(切换键空间)
    - alter keyspace(修改键空间)
      `alter keyspace <identifer> with <proteries>`
      > alter keyspace excelsior with replication={'class':'simplestrategy','replication_factor':4}
    - drop keyspace(删除键空间)
      语法：`drop keyspace (if not exists)? <identifer>`
      > drop keyspace excelsior;
    - 触发器
		![chufaqi](https://www.azheimage.top/db4ee2491de5f400a0eedfeab66bff21.png)
		- 自定义类型使用
		```sql
		CREATE KEYSPACE complex
		WITH replication = {'class' : 'SimpleStrategy', 'replication_factor' :

		3};

		CREATE TYPE complex.phone (

		alias text,

		number text

		);

		CREATE TYPE complex.address (

		street text,

		city text,

		zip_code int,

		phones list<frozen<phone>>

		);

		CREATE TABLE complex.accounts (

		email text PRIMARY KEY,

		name text,

		addr frozen<address>

		);

		-- 自定义类型：phone和address。
		```
  - CQL数据操作语句
    ##### CQL数据操作语句主要是INSERT,UPDATE,DELETE,具体包括
    - INSTERT
      ![insert](https://www.azheimage.top/80cc933039cd2cb80d72f5648bb89214.png)
    - UPDATE
			![update](https://www.azheimage.top/b6bc65d554d34dbbaf47bc76da3fc0e0.png)
    - DELETE
      ![delete](https://www.azheimage.top/6318f5c5d7bb8e98b0a01169dc52f94c.png)
    - BATCH（原子性的操作，要么都执行成功，否则回滚）
      ![batch](https://www.azheimage.top/7ef5fcbf45da55c154e2e31986d2f818.png)
    - cql操作演示
			![cql](https://www.azheimage.top/f64471ed3d0cc46d42e78b7f1d5566e8.png)
  - CQL数据查询语句
      ![select](https://www.azheimage.top/f416ff49add26d070121ed50a174b6a5.png)
    - 语法：
    ```
    <select-stmt> ::= SELECT ( JSON )? <select-clause>
                      FROM <tablename>
                      ( WHERE <where-clause> )?
                      ( ORDER BY <order-by> )?
                      ( PER PARTITION LIMIT <integer> )?
                      ( LIMIT <integer> )?
                      ( ALLOW FILTERING )?

    <select-clause> ::= DISTINCT? <selection-list>

    <selection-list> ::= <selector> (AS <identifier>)? ( ',' <selector> (AS <identifier>)? )*
                       | '*'

    <selector> ::= <identifier>
                 | <term>
                 | WRITETIME '(' <identifier> ')'
                 | COUNT '(' '*' ')'
                 | TTL '(' <identifier> ')'
                 | CAST '(' <selector> AS <type> ')'
                 | <function> '(' (<selector> (',' <selector>)*)? ')'

    <where-clause> ::= <relation> ( AND <relation> )*

    <relation> ::= <identifier> <op> <term>
                 | '(' <identifier> (',' <identifier>)* ')' <op> <term-tuple>
                 | <identifier> IN '(' ( <term> ( ',' <term>)* )? ')'
                 | '(' <identifier> (',' <identifier>)* ')' IN '(' ( <term-tuple> ( ',' <term-tuple>)* )? ')'
                 | TOKEN '(' <identifier> ( ',' <identifer>)* ')' <op> <term>

    <op> ::= '=' | '<' | '>' | '<=' | '>=' | CONTAINS | CONTAINS KEY
    <order-by> ::= <ordering> ( ',' <odering> )*
    <ordering> ::= <identifer> ( ASC | DESC )?
    <term-tuple> ::= '(' <term> (',' <term>)* ')'
    ```
    - 例子：
    ```sql
    SELECT name, occupation FROM users WHERE userid IN (199, 200, 207);

    SELECT JSON name, occupation FROM users WHERE userid = 199;

    SELECT name AS user_name, occupation AS user_occupation FROM users;

    SELECT time, value
    FROM events
    WHERE event_type = 'myEvent'
      AND time > '2011-02-03'
      AND time <= '2012-01-01'

    SELECT COUNT(*) FROM users;

    SELECT COUNT(*) AS user_count FROM users;
    ```
    ##### 第一：索引查询
    cassandra是支持创建二级索引的，索引可以创建在除了第一个主键之外所有的列上，当然有些类型除外，例如集合类型。
    ```sql
    CREATE TABLE test(
  	a INT,
  	b INT,
  	c INT,
  	d INT,
  	e INT,
  	m INT,
  	PRIMARY KEY(a,b,c));

    CREATE INDEX ON test(c);
    CREATE INDEX ON test(e);
    ```
    在第一主键a上创建索引是不可以的：
    `CREATE INDEX ON test(a) //X`
    索引列只可以用=号查询，所以
    ```sql
    SELECT * FROM test WHERE e=1; //是可以
    SELECT * FROM test WHERE e>1; //就不行了。
    ```
    如果你的查询条件里，有一个是根据索引查询，那其它非索引非主键字段，可以通过加一个ALLOW FILTERING来过滤实现、
    例如：
    ```sql
    SELECT * FROM test WHERE e=1 AND m>2 ALLOW FILTERING;
    ```
    第二：排序
    cassandra也是支持排序的，order by。 当然它的排序也是有条件的，
      1. 必须有第一主键的=号查询。cassandra的第一主键是决定记录分布在哪台机器上，也就是说cassandra只支持单台机器上的记录排序。
      2. 那就是只能根据第二、三、四…主键进行有序的，相同的排序。
      3. 不能有索引查询
    ```sql
    SELECT * FROM test WHERE a=1 ORDER BY b DESC;
    SELECT * FROM test WHERE a=1 ORDER BY b DESC, c DESC;
    SELECT * FROM test WHERE a=1 ORDER BY b ASC;
    SELECT * FROM test WHERE a=1 ORDER BY b ASC, c ASC;
    ```
    以上都是可以的。
    ```sql
    SELECT * FROM test ORDER BY b DESC; //没有第一主键 不行
    SELECT * FROM test WHERE a=1 ORDER BY c DESC; //必须以第二主键开始排序
    SELECT * FROM test WHERE a=1 ORDER BY b DESC, c ASC; //不是相同的排序。
    SELECT * FROM test WHERE e=1 ORDER BY b DESC; //不能有索引。
    ```
    其实cassandra的任何查询，最后的结果都是有序的，默认的是b asc, c asc，因为它内部就是这样存储的。
    当然这个默认存储排序方式，是可以在建表的时候指定的。
    ```sql
    CREATE TABLE test(
    	a INT,
    	b INT,
    	c INT,
    	d INT,
    	e INT,
    	m INT,
    	PRIMARY KEY(a,b,c))
    WITH CLUSTERING ORDER BY (b DESC, c ASC);
