---
categories:
- 技术
- 大数据
date: '2019-07-15 20:01:21+08:00'
tags:
- train
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725102054110.png
title: 4-快学spark
---
为数据中台新人进行培训，培训内容spark
<!--more-->

## 1. 什么是Spark？用来做什么？有什么特点？
Spark是专为大规模数据处理而设计的快速通用的计算引擎，是UC Berkeley AMP lab所开源的类Hadoop MapReduce的通用分布式并行计算框架。
## 2. Spark 和MapReduce对比：
Spark拥有Hadoop MapReduce所具有的优点，但和MapReduce 的最大不同之处在于：
1. Spark是基于内存的迭代式计算——Spark的Job处理的中间输出结果可以保存在内存中，从而不再需要读写HDFS，
对于迭代数据Spark效率更高。
2. 一个MapReduce 在计算过程中只有map 和reduce 两个阶段，处理之后就结束了，而在Spark的计算模型中，可以分为n阶段，因为它内存迭代式的，在处理完一个阶段以后，可以继续往下处理很多个阶段，而不只是两个阶段。
3. MapReduce总是消耗大量时间排序，而有些场景不需		要排序，Spark可以避免不必要的排序所带来的开销
4. Spark是一张有向无环图（从一个点出发最终无法回到		该点的一个拓扑），并对其进行优化
5. Spark能更好地适用于数据挖掘与机器学习等需要迭代的MapReduce的算法。其不仅实现了MapReduce的算子map 函数和reduce函数及计算模型，还提供更为丰富的算子，如filter、join、groupByKey等。
6. 是一个用来实现快速而通用的集群计算的平台

## 3. Spark 和Hadoop对比
1. 高可伸缩性
2. 高容错：每个RDD都会记录自己所依赖的父RDD，一旦出现某个RDD的某些partition丢失，可以通过并行计算迅速恢复
3. 基于内存计算：Spark的中间数据放到内存中，对于迭代运算效率更高
4. 更加通用： Spark提供的数据集操作类型更多

## 4. Spark的适用场景
1. Spark是基于内存的迭代计算框架，适用于需要多次操作特定数据集的应用场合。需要反复操作的次数越多，所需读取的数据量越大，受益越大，数据量小但是计算密集度较大的场合，受益就相对较小（大数据库架构中这是是否考虑使用Spark的重要因素）
2. 由于RDD的特性，Spark不适用那种异步细粒度更新状态的应用，例如web服务的存储或者是增量的web爬虫和索引。就是对于那种增量修改的应用模型不适合

## 5. RDD
RDD（Resilient Distributed Dataset）叫做分布式数据集，是Spark中最基本的数据抽象，它代表一个不可变、可分区、里面的元素可并行计算的集合。
RDD具有数据流模型的特点：自动容错、位置感知性调度和可伸缩性。
RDD允许用户在执行多个查询时显式地将工作集缓存在内存中，后续的查询能够重用工作集，这极大地提升了查询速度

源代码中对于RDD解释
- A list of partitions
即数据集的基本组成单位。对于RDD来说，每个分片都会被一个计算任务处理，并决定并行计算的粒度。
- A function for computing each split
每个函数作用于一个分区。
- A list of dependencies on other RDDs
RDD与RDD之间有依赖关系（宽依赖、窄依赖），在部分分区数据丢失时，Spark可以通过这个依赖关系重新计算丢失的分区数据，而不是对RDD的所有分区进行重新计算。
- Optionally, a Partitioner for key-value RDDs (e.g. to say that the RDD is hash-partitioned)
如果RDD是key-value形式的，会有一个分区器(Partioner)作用在这个RDD，分区器会决定该RDD的数据放在哪个子RDD的分区上
- Optionally, a list of preferred locations to compute each split on (e.g. block locations for an HDFS file)
一个列表，存储存取每个Partition的优先位置（preferred location）。对于一个HDFS文件来说，这个列表保存的就是每个Partition所在的块的位置。按照“移动数据不如移动计算”的理念，Spark在进行任务调度的时候，会尽可能地将计算任务分配到其所要处理数据块的存储位置。

## 5. spark组件
![](https://www.azheimage.top/markdown-img-paste-20190715153727996.png)
1. Spark Core 
实现Spark的基本功能，包括任务调度、内存管理、错误恢复、与存储系统交互等，以及RDD（Resilient Distributed Dataset）API的定义。 
2. Spark SQL 
用Spark来操作结构化数据的程序包。可以使用SQL或Hive的HQL来查询数据，并可以与RDD的操作相结合使用。 
3. Spark Streaming 
用来对实时数据进行流式计算的组件，Streaming中提供操作流式数据的API与RDD高度对应。Streaming与日志采集工具Flume、消息处理Kafka等可集成使用。 
4. MLib 
机器学习（ML）的功能库，提供多种学习算法，包括分类、回归、聚类、协同过滤等，还提供了模型评估、数据导入等功能。 
5. GraphX 
用来操作图的程序库，可以用于并行的图计算。扩展了RDD API功能，用来创建一个顶点和边都包含任意属性的有向图。支持针对图的各种操作，如图的分割subgraph、操作所有的顶点mapVertices、三角计算等。

## 6. Spark支持的API
Scala、Python、Java等
## 7. 运行模式
○ Local （用于测试、开发）
○ Standlone （独立集群模式）
○ Spark on Yarn （Spark在Yarn上）
○ Spark on Mesos （Spark在Mesos）

## 8. Demo
https://gitee.com/azhegit/ScalaDemo

## 9. 预期目标
1. 用python实现workCount
2. 实现对接kafka的实时Wordcount