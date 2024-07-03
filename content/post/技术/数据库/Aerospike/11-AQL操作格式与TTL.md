---
categories:
- 技术
- 数据库
date: '2021-10-27 20:47:17+08:00'
tags:
- Aerospike
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110153448285.png
title: 11-AQL操作格式与TTL
---
- record_ttl   设置默认 TTL   time to live
- RECORD_PRINT_METADATA    显示元数据（TTL gen）  记录存活时间 记录更新次数
<!--more-->
- last-update-time （LUT） 上次更新时间，内部元数据，不会返回给客户端。
- key_send    是否发送保存key , 设置为true , 查询时会返回 pk

```bash
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
```
        
这些设置只在当前会话生效，退出重新登录后恢复默认设置


aql> get record_ttl
RECORD_TTL = 0

aql> set record_ttl 1000
RECORD_TTL = 1000
>设置 默认ttl 为 1000 s，会影响后续的操作

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
>默认不显示记录元数据信息

aql> set  RECORD_PRINT_METADATA true
RECORD_PRINT_METADATA = true
>设置显示记录元数据信息 (generate TTL)

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