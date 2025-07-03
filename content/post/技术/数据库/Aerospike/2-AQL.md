---
categories:
- 技术
- 数据库
date: '2021-09-17 15:42:09+08:00'
tags:
- Aerospike
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725100954649.png
title: 2-AQL
---

AQL 是一个命令行工具，用于浏览数据并为 Aerospike 数据库开发用户定义函数。
<!--more-->
## AQL - [aerospike的语法](https://docs.aerospike.com/docs/tools/aql/record_operations.html)


### 数据插入
命令
`INSERT INTO <ns>[.<set>] (PK, <bins>) VALUES (<key>, <values>)`
- <ns> 是记录的命名空间。
- <set> 是记录的集合名称。
- <key> 是记录的主键。
- <bins> 是一个以逗号分隔的 bin 名称列表。
- <values>是逗号分隔的 bin 值列表，其中可能包括类型转换表达式。设置为 NULL（不区分大小写和无引号）以删除 bin。

aql> INSERT INTO test.testset (PK, a, b) VALUES ('xyz', 'abc', 123)



### 删除记录
以下是删除记录的命令：

DELETE FROM <ns>[.<set>] WHERE PK=<key>
在哪里

<ns> 是记录的命名空间。
<set> 是记录的集合名称。
<key> 是记录的主键。
例子：

aql> DELETE FROM test.testset WHERE PK='xyz'

### 操作记录
以下是插入记录的命令：

OPERATE <op(<bin>, params...)>[with_policy(<map policy>),] [<op(<bin>, params...)> with_policy (<map policy>) ...] ON <ns>[.<set>] where PK=<key>
在哪里

<op> 要执行的操作的名称。
<bin> 是 bin 的名称。
<params> 操作参数。
<map policy> 地图运营政策。
<ns> 是要查询的记录的命名空间。
<set> 是要查询的记录的集合名称。
<key> 是记录的主键。
例子：

aql> OPERATE LIST_APPEND(listbin, 1), LIST_APPEND(listbin2, 10) ON test.demo where PK = 'key1'
aql> OPERATE LIST_POP_RANGE(listbin, 1, 10) ON test.demo where PK = 'key1'

### 清空表
truncate test.testset

### 删除记录
delete from test.logistic where PK='a'

```
record_ttl   设置默认 TTL   time to live
RECORD_PRINT_METADATA    显示元数据（TTL gen）  记录存活时间 记录更新次数
 last-update-time （LUT） 上次更新时间，内部元数据，不会返回给客户端。
key_send    是否发送保存key , 设置为true , 查询时会返回 pk

SETTINGS
        ECHO                          (true | false, default false)
        VERBOSE                       (true | false, default false)
        OUTPUT                        (TABLE | JSON | MUTE | RAW, default TABLE)
        OUTPUT_TYPES                  (true | false, default true)
        TIMEOUT                       (time in ms, default: 1000)
        SOCKET_TIMEOUT                (time in ms, default: -1)
        LUA_USERPATH                  , default : /opt/aerospike/usr/udf/lua
        USE_SMD                       (true | false, default false)
        RECORD_TTL                    (time in sec, default: 0)
        RECORD_PRINT_METADATA         (true | false, default false, prints record metadata)
        REPLICA_ANY                   (true | false, default false)
        KEY_SEND                      (true | false, default false)
        DURABLE_DELETE                (true | false, default false)
        FAIL_ON_CLUSTER_CHANGE        (true | false, default true, policy applies to scans)
        SCAN_PRIORITY                 priority of scan (LOW, MEDIUM, HIGH, AUTO), default : AUTO
        NO_BINS                       (true | false, default false, No bins as part of scan and query result)
        LINEARIZE_READ                (true | false, default false, Make read linearizable, applicable only for namespace with strong_consistency enabled.)

        
这些设置只在当前会话生效，退出重新登录后恢复默认设置


aql> get record_ttl
RECORD_TTL = 0

aql> set record_ttl 1000
RECORD_TTL = 1000
# 设置 默认ttl 为 1000 s，会影响后续的操作

aql> select * from ns1.data_clean where pk='a'
+------+
| DATA |
+------+
| "a"  |
+------+
1 row in set (0.002 secs)

OK

aql> get RECORD_PRINT_METADATA
RECORD_PRINT_METADATA = false
# 默认不显示记录元数据信息

aql> set  RECORD_PRINT_METADATA true
RECORD_PRINT_METADATA = true
# 设置显示记录元数据信息 (generate TTL)

aql> select * from ns1.data_clean where pk='a'
+------+---------+-------+
| DATA | {ttl}   | {gen} |
+------+---------+-------+
| "a"  | 7775610 | 1     |
+------+---------+-------+
1 row in set (0.002 secs)

OK

aql> INSERT INTO ns1.data_clean (PK,DATA) VALUES ('a','a')
OK, 1 record affected.

# 执行 insert (新增或更新)

aql> select * from ns1.data_clean where pk='a'
+------+-------+-------+
| DATA | {ttl} | {gen} |
+------+-------+-------+
| "a"  | 952   | 2     |
+------+-------+-------+
1 row in set (0.002 secs)

# ttl 使用设置的默认 1000  ， 更新后 GEN 增加

aql> INSERT INTO ns1.data_clean (PK,DATA) VALUES ('a','new')
OK, 1 record affected.


aql> select * from ns1.data_clean where pk='a'
+-------+-------+-------+
| DATA  | {ttl} | {gen} |
+-------+-------+-------+
| "new" | 975   | 3     |
+-------+-------+-------+
1 row in set (0.001 secs)

aql> get key_send
KEY_SEND = false
# 默认不会保存 key 

aql> set key_send true
KEY_SEND = true
# 设置为发送保存key

aql> INSERT INTO ns1.data_clean (PK,DATA) VALUES ('a','new2')
OK, 1 record affected.

aql> select * from ns1.data_clean where pk='a'
+-----+--------+-------+-------+
| PK  | DATA   | {ttl} | {gen} |
+-----+--------+-------+-------+
| "a" | "new2" | 979   | 4     |
+-----+--------+-------+-------+
1 row in set (0.001 secs)

# 返回结果显示 PK


aql> get all
ECHO = false
VERBOSE = false
OUTPUT = TABLE
OUTPUT_TYPES = true
TIMEOUT = 1000
LUA_USERPATH = /opt/aerospike/usr/udf/lua
USE_SMD = false
RECORD_TTL = 0
RECORD_PRINT_METADATA = false
REPLICA_ANY = false
KEY_SEND = false
DURABLE_DELETE = false
FAIL_ON_CLUSTER_CHANGE = true
SCAN_PRIORITY = AUTO
NO_BINS = false
LINEARIZE_READ = false
```
