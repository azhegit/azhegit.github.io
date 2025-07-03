---
categories:
- 技术
- 大数据
date: '2024-04-04 12:59:06+08:00'
tags:
- flink
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110143922992.png
title: Flink流批一体方案
---

实现批处理的技术许许多多，从各种关系型数据库的 sql 处理，到大数据领域的 MapReduce，Hive，Spark 等等。

### 离线数仓

<!--more-->

常见大数据离线批计算是由 Hive 加上 Spark 的方案，Hive 数仓有着成熟和稳定的存储能力，Spark 高性能计算能力，结合调度和上下游工具，构建一个完整的数据处理分析平台。

![](https://www.azheimage.top/markdown-img-paste-2021060816210003.png)

### 实时数仓

常见实时计算的架构一般来说包括消息队列、计算引擎和结果存储三部分。目前，我们常用的消息队列是 Kafka，计算引擎我们采用的是 Flink 作为我们统一的实时计算引擎。

离线数据源通过同步工具将数据同步到 kafka 集群，计算引擎用 flink 做数据 ETL、指标计算、特征提取、模型结果产出等，最终将实时计算结果 append 或者 update 到应用层。

![](https://www.azheimage.top/markdown-img-paste-20210608162108365.png)

### 指标计算-流批一体

Flink DataStream API 实现指标计算逻辑，适配离线数据源或者实时数据源，指标计算共用同一套计算逻辑。

目标： 实时数据处理和历史数据处理逻辑可以复用 指标计算支持流作业与批作业，减少维护成本 增量计算算子统一

![](https://www.azheimage.top/markdown-img-paste-20210608162151135.png)
