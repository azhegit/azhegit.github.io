---
categories:
- 技术
- 图计算
date: '2019-07-04 13:16:16+08:00'
tags:
- spark
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716211711809.png
title: pregel
---

## Pregel

###### Pregel 是 google 提出的用于大规模分布式图计算框架。主要用于图遍历（BFS）、最短路径（SSSP）、PageRank 计算等等计算。

<!--more-->

### 简介

在 Pregel 计算模式中，输入是一个有向图，该有向图的每一个顶点都有一个相应的独一无二的顶点 id (vertex identifier)。每一个顶点都有一些属性，这些属性可以被修改，其初始值由用户定义。每一条有向边都和其源顶点关联，并且也拥有一些用户定义的属性和值，并同时还记录了其目的顶点的 ID。
一个典型的 Pregel 计算过程如下：读取输入，初始化该图，当图被初始化好后，运行一系列的 supersteps，每一次 superstep 都在全局的角度上独立运行，直到整个计算结束，输出结果。
在 pregel 中顶点有两种状态：活跃状态（active）和不活跃状态（halt）。如果某一个顶点接收到了消息并且需要执行计算那么它就会将自己设置为活跃状态。如果没有接收到消息或者接收到消息，但是发现自己不需要进行计算，那么就会将自己设置为不活跃状态。这种机制的描述如下图：
![](https://img-blog.csdn.net/20160420124300354)

### 计算过程

#### [Google Pregel 论文](http://www.pitt.edu/~viz/classes/infsci3350/resources/pregel_sigmod10.pdf)

Pregel 中的计算分为一个个“superstep”，这些”superstep”中执行流程如下：

1. 首先输入图数据，并进行初始化。
2. 将每个节点均设置为活跃状态。每个节点根据预先定义好的 sendmessage 函数，以及方向（边的正向、反向或者双向）向周围的节点发送信息。
3. 每个节点接收信息如果发现需要计算则根据预先定义好的计算函数对接收到的信息进行处理，这个过程可能会更新自己的信息。如果接收到消息但是不需要计算则将自己状态设置为不活跃。
4. 每个活跃节点按照 sendmessage 函数向周围节点发送消息。
5. 下一个 superstep 开始，像步骤 3 一样继续计算，直到所有节点都变成不活跃状态，整个计算过程结束。

下面以一个具体例子来说明这个过程：假设一个图中有 4 个节点，从左到右依次为第 1/2/3/4 个节点。圈中的数字为节点的属性值，实线代表节点之间的边，虚线是不同超步之间的信息发送，带阴影的圈是不活跃的节点。我们的目的是让图中所有节点的属性值都变成最大的那个属性值。
![](https://img-blog.csdn.net/20160420124344434)

    superstep 0：首先所有节点设置为活跃，并且沿正向边向相邻节点发送自身的属性值。
    Superstep 1：所有节点接收到信息，节点1和节点4发现自己接受到的值比自己的大，所以更新自己的节点(这个过程可以看做是计算)，并保持活跃。节点2和3没有接收到比自己大的值，所以不计算、不更新。活跃节点继续向相邻节点发送当前自己的属性值。
    Superstep 2：节点3接受信息并计算，其它节点没接收到信息或者接收到但是不计算，所以接下来只有节点3活跃并发送消息。
    Superstep 3：节点2和4接受到消息但是不计算所以不活跃，所有节点均不活跃，所以计算结束。

在 pregel 计算框架中有两个核心的函数：sendmessage 函数和 F(Vertex)节点计算函数。

```scala
def pregel[A: ClassTag](
    initialMsg: A,
    maxIterations: Int = Int.MaxValue,
    activeDirection: EdgeDirection = EdgeDirection.Either)(
    vprog: (VertexId, VD, A) => VD,
    sendMsg: EdgeTriplet[VD, ED] => Iterator[(VertexId, A)],
    mergeMsg: (A, A) => A)
  : Graph[VD, ED] = {
  Pregel(graph, initialMsg, maxIterations, activeDirection)(vprog, sendMsg, mergeMsg)
}
```

### GraphX API 中的参数：

pregel 是 spark 图极限封装的一个基础 api，帮助简单实现基础的图计算功能，核心功能主要为三个自定义功能方法，如下图所示，每次 pregel 执行迭代生成一个新的图

- mergeMsg：自定义聚合消息的方式
- vprog：使用聚合消息更新当前顶点
- sendMsg：定义消息接收方，并且发送消息
  ![](http://www.zdingke.com/wp-content/uploads/2018/01/20180106180130_30007.png)
- initialMsg:第一次迭代默认给每个顶点发送一个初始化消息
- maxIterations：最多迭代次数
- activeDirection：决定当前顶点是否发送消息，一般构造 edge[srcid,dstid,attr]时，默认左边为 srcid，右边为 dstid:
  - EdgeDirection.Out，假设当前顶点为 srcId，收到来自上一轮迭代的消息时，就会调用 sendMsg。
  - EdgeDirection.In，假设当前顶点为 dstId，收到来自上一轮迭代的消息时，就会调用 sendMsg。
  - EdgeDirection.Either，只要 srcId 或 dstId 收到来自上一轮迭代的消息时，两个顶点都会调用 sendMsg。
  - EdgeDirection.Both，只有 srcId 和 dstId 都收到来自上一轮迭代的消息时，两个点的才会调用 sendMsg

#### 源码解读

```scala
//初始化消息，更新节点，完成一次迭代
var g = graph.mapVertices((vid, vdata) => vprog(vid, vdata, initialMsg)).cache()
//计算发给下一次迭代的消息并合并
var messages = g.mapReduceTriplets(sendMsg, mergeMsg)
var activeMessages = messages.count()
var prevG: Graph[TestVertice, Int] = null
var i = 0
//根据迭代次数或者消息数量进行循环
while (activeMessages > 0 && i < maxIterations) {
    //使用已经合并的消息，更新当前节点
    val newVerts = g.vertices.innerJoin(messages)(vprog).cache()
    prevG = g
    //生成新的图，完成一次迭代
    g = g.outerJoinVertices(newVerts) { (vid, old, newOpt) => newOpt.getOrElse(old) }
    g.cache()
    val oldMessages = messages
    //计算发给下一次迭代的消息并合并
  messages = g.mapReduceTriplets(sendMsg, mergeMsg, Some((newVerts,activeDirection))).cache()
  //计算发给下一次迭代的消息量，如果消息为0，则停止循环
    activeMessages = messages.count(）
      oldMessages.unpersist(blocking = false)
    newVerts.unpersist(blocking = false)
    prevG.unpersistVertices(blocking = false)
  prevG.edges.unpersist(blocking = false)
  i += 1
}
```

#### spark graphx 优化

由于关系链项目是需要求二度关系，甚至三度关系，从第二次迭代开始数据量会呈指数增长，导致 out of memory 或者 lost task 等错误，归根到底就是内存不够；所以 spark graphx 的优化主要从内存和减少 job 入手

- 增加机器内存
  暴力而且难以实现
- 数据序列化和压缩
  采用 spak kryo 进行序列化，并且设置压缩，能够减少 8-9 倍数据量，rdd 存储为 MEMORY_ONLY_SER 配置才生效
  set(“spark.rdd.compress”, “true”)
  set(“spark.serializer”, “org.apache.spark.serializer.KryoSerializer”)
- pregel api 修改
  由于项目需求最多是跑到三度关系，迭代的次数是固定的；
  因此 pregel api 的一些 job 操作，比如，messages.count()可以去掉；
  根据 pregel 的计算流程，每次迭代完成后，发送的消息是给下一次迭代计算用的，mapReduceTriplets 这个 job 操作是可以在最后一次迭代去掉的
