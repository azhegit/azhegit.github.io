---
categories:
- 技术
- 大数据
date: '2019-07-15 20:03:37+08:00'
tags:
- train
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725100954649.png
title: 5-快学presto
---
为数据中台新人进行培训，培训内容presto
<!--more-->

## 1. Presto是什么?
Presto是Facebook开发的数据查询引擎,是facebook的工程师对hive的查询速度忍无可忍后，下决心开发的一款高性能查询引擎，基于java8编写，其基于page的pipeline技术，使其具有高效的交互式查询性能，并可以高效的控制GC。
Presto通过使用分布式查询，可以快速高效的完成海量数据的查询。作为Hive和Pig的替代者，Presto不仅能访问HDFS，也能访问不同的数据源，包括：RDBMS和其他数据源（如Cassandra），而其和底层数据源解耦的特性，使其能够对接各类数据源，并具有跨源查询的特性。

## 2. Presto优点
1.Presto与hive对比，都能够处理PB级别的海量数据分析，但Presto是基于内存运算，减少没必要的硬盘IO，所以更快。
2.能够连接多个数据源，跨数据源连表查，如从hive查询大量网站访问记录，然后从mysql中匹配出设备信息。
3.部署也比hive简单。

## 3. Presto优点
1.虽然能够处理PB级别的海量数据分析，但不是代表Presto把PB级别都放在内存中计算的。而是根据场景，如count，avg等聚合运算，是边读数据边计算，再清内存，再读数据再计算，这种耗的内存并不高。但是连表查，就可能产生大量的临时数据，因此速度会变慢，反而hive此时会更擅长。 
2.为了达到实时查询，可能会想到用它直连MySql来操作查询，这效率并不会提升，瓶颈依然在MySql，此时还引入网络瓶颈，所以会比原本直接操作数据库要慢。

## 4.角色
Presto有两类服务器：coordinator和worker。
### 1. Coordinator
- Coordinator服务器是用来解析语句，执行计划分析和管理Presto的worker结点。Presto安装必须有一个Coordinator和多个worker。如果用于开发环境和测试，则一个Presto实例可以同时担任这两个角色。
- Coordinator跟踪每个work的活动情况并协调查询语句的执行。 Coordinator为每个查询建立模型，模型包含多个stage，每个stage再转为task分发到不同的worker上执行。
- Coordinator与Worker、client通信是通过REST API。
### 2. Worker
- Worker是负责执行任务和处理数据。Worker从connector获取数据。Worker之间会交换中间数据。Coordinator是负责从Worker获取结果并返回最终结果给client。
- 当Worker启动时，会广播自己去发现 Coordinator，并告知 Coordinator它是可用，随时可以接受task。
- Worker与Coordinator、Worker通信是通过REST API

## 5. Presto架构
![](https://www.azheimage.top/markdown-img-paste-20190715194305901.png)
prestodb主要由一个coordinator和多个worker组成，coordinaor节点负责和client对接，接收client发送过来的各类请求(DDL和DML)。coordinator在接收到client的请求后，就开始进行请求的处理，最后把查理结果返回给client。coordinator在进行请求处理时，对各类sql语句进行词法解析、语法分析、语义分析、优化、生成执行计划最后在调度模块进行任务的分发，把子任务分发到各个worker节点。worker节点是实际的执行节点，会执行包括聚合、排序、join以及去重等操作。

## 6. 相关文档
1. 部署：http://wiki.tongdun.me/pages/viewpage.action?pageId=29336053
2. 源码分析：http://wiki.tongdun.me/pages/viewpage.action?pageId=30101182