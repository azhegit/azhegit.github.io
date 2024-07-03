---
categories:
- 技术
- 大数据
date: '2020-06-16 15:50:46+08:00'
tags:
- kafka
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180831191423561.png
title: 2-kafka权限测试
---
测试kafka权限验证
<!--more-->
## 测试
1. 新建topic
```bash
cd sasl_kafka_tools
#topic:test-sasl 分区数:2 副本数:1
./kafka-topic-create.sh test-sasl 2 1
```
2. 生产数据脚本
```bash
cd sasl_kafka_tools
#topic:test-sasl 发送数据总量:100000 每秒发送数据量:1
./kafka-perf-test.sh test-sasl 100000 1
```
3. 二级kafka创建topic
./kafka-topic-create.sh test-sasl-1 2 2
4. 配置kafka-mirror-maker配置信息
```bash
vim ENV_KAFKA_HOST
# mirror_maker配置，添加白名单及映射关系
MIRROR_WHITE_LIST="teset-copy|test-sasl"
MIRROR_HANGER_ARGS="teset-copy->copy1,copy2,copy3,copy4,copy5,copy6,copy7,copy8,copy9,copy10|test-sasl->test-sasl-1"
```
5. 查看mirror-maker状态
./pstatus.sh mk
6. 重启mirror-maker
./prestart.sh mk
7. 在二级kafka执行消费脚本，查看到数据已经同步
./kafka-consumer.sh test-sasl-1
8. 添加新用户
./kafka-sasl-user-alter.sh sasl saslpwd
9. 添加读权限
./kafka-sasl-topic-add-token.sh sasl test-sasl-1 r
10. 添加写权限
./kafka-sasl-topic-add-token.sh sasl test-sasl-1 w
11. 程序验证
12. 删除写权限
./kafka-sasl-topic-remove-token.sh sasl test-sasl-1 w
13. 删除读权限
./kafka-sasl-topic-remove-token.sh sasl test-sasl-1 r

