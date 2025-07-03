---
categories:
- 技术
- 图计算
date: '2019-07-04 13:16:16+08:00'
tags:
- spark
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716211900993.png
title: Graphx源码学习
---


一、什么是 GraphX？

Graphx 利用了 Spark 这样了一个并行处理框架来实现了图上的一些可并行化执行的算法。
<!--more-->

mapReduceTriplets
joinVertices

aggregateMessagesWithActiveSet

aggregateMessages

mapVertices

Spark 图处理 GraphX 学习笔记！

算法是否能够并行化与 Spark 本身无关

算法并行化与否的本身，需要通过数学来证明

已经证明的可并行化算法，利用 Spark 来实现会是一个错的选择，因为 Graphx 支持 pregel 的图计算模型

二、Graphx 包含哪些组件和基本框架？

1、成员变量
graph 中重要的成员变量分别为

vertices

edges

triplets

为什么要引入 triplets 呢，主要是和 Pregel 这个计算模型相关，在 triplets 中，同时记录着 edge 和 vertex. 具体代码就不罗列了。

2、成员函数
函数分成几大类

对所有顶点或边的操作，但不改变图结构本身，如 mapEdges, mapVertices

子图,类似于集合操作中的 filter subGraph

图的分割，即 paritition 操作，这个对于 Spark 计算来说，很关键，正是因为有了不同的 Partition,才有了并行处理的可能, 不同的 PartitionStrategy,其收益不同。最容易想到的就是利用 Hash 来将整个图分成多个区域。

outerJoinVertices 顶点的外连接操作

三、图的运算和操作 GraphOps
图的常用算法是集中抽象到 GraphOps 这个类中，在 Graph 里作了隐式转换，将 Graph 转换为 GraphOps，具体有下列 12 个算子：

collectNeighborIds

collectNeighbors

collectEdges

joinVertices

filter

pickRandomVertex

pregel

pageRank

staticPageRank

connectedComponents

triangleCount

stronglyConnectedComponents

RDD
RDD 是 Spark 体系的核心，那么 Graphx 中引入了哪些新的 RDD 呢，有俩，分别为

VertexRDD

EdgeRDD

较之 EdgeRdd，VertexRDD 更为重要，其上的操作也很多，主要集中于 Vertex 之上属性的合并，说到合并就不得不扯到关系代数和集合论，所以在 VertexRdd 中能看到许多类似于 sql 中的术语，如

leftJoin

innerJoin

### joinVertices 与 outerJoinVertices

在许多情况下，有必要将外部数据（RDD）与图形关联起来。

> 1 class Graph[VD, ED] {
> 2 def joinVertices[U](table: RDD[(VertexId, U)])(map: (VertexId, VD, U) => VD)
> 3 : Graph[VD, ED]
> 4 def outerJoinVertices[U, VD2](table: RDD[(VertexId, U)])(map: (VertexId, VD, Option[U]) => VD2)
> 5 : Graph[VD2, ED]
> 6 }

内连接（joinVertices）运算符连接输入 RDD 并返回通过用户定义关系关联的新图形。RDD 中没有匹配的顶点保留原始值。

外连接（outerJoinVertices）运算符：因为并非所有的顶点在输入 RDD 中都具有匹配值，所以在不确定的时候可以采用该类型。

outerJoinVertices 的作用：通过 join 将两个图的顶点属性进行汇总，因为是 outjoin，可能左边的图的点，没有 join 上右边对应的点，这时候，这个函数给你了一个选择的判断。

定义：

```scala
def outerJoinVertices[U, VD2](other: RDD[(VertexID, U)])
      (mapFunc: (VertexID, VD, Option[U]) => VD2)
    : Graph[VD2, ED]

mapFunc的几种写法：

1）val inputGraph: Graph[Int, String] =
  graph.outerJoinVertices(graph.outDegrees)((vid, _, degOpt) => degOpt.getOrElse(0))

2）val degreeGraph = graph.outerJoinVertices(outDegrees) { (id, oldAttr, outDegOpt) =>
  outDegOpt match {
    case Some(outDeg) => outDeg
    case None => 0 // No outDegree means zero outDegree
  }
}

3）val rank_cc = cc.outerJoinVertices(pagerankGraph.vertices) {
  case (vid, cc, Some(pr)) => (pr, cc)
  case (vid, cc, None) => (0.0, cc)
}
```
