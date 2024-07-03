---
categories:
- 技术
- 数据库
date: 2018-07-14 09:18:38+08:00
tags:
- janusgraph
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716211900993.png
title: Janusgraph学习--1(Janusgraph安装)
---


JanusGraph是一个可扩展的图形数据库，专门用于存储和查询包含分布在多机群集中的数千亿个顶点和边缘的图形。JanusGraph是一个事务数据库，可以支持数千个并发用户实时执行复杂的图遍历。

<!--more-->
<!--toc-->
# 本文讲述JanusgraphE的单机版安装：
*初次接触￣□￣｜｜，学习记录一下*
## Janusgraph Logo：
![](https://www.azheimage.top/markdown-img-paste-20180713173354102.png)
* ### JanusGraph架构：
![](https://www.azheimage.top/markdown-img-paste-20180713175121946.png)
* ### 下载安装包
https://github.com/JanusGraph/janusgraph/releases/download/v0.2.0/janusgraph-0.2.0-hadoop2.zip
* ### 解压安装包：
解压到/data01目录：`unzip janusgraph-0.2.0-hadoop2.zip`
* ### 执行启动：
启动：`bin/gremlin.sh`
如果可以执行如下gremlin命令，则说明JanusGraph安装成功。
```sql
gremlin> 100-10
==>90
gremlin> "JanusGraph:" + " The Rise of Big Graph Data"
==>JanusGraph: The Rise of Big Graph Data
gremlin> [name:'aurelius', vocation:['philosopher', 'emperor']]
==>name=aurelius
==>vocation=[philosopher, emperor]
```
* ### Gods图

![](https://www.azheimage.top/markdown-img-paste-20180713182054834.png)
#### 将Gods的图表加载到janusgraph中，跟HBASE结合
```sql
gremlin> graph = JanusGraphFactory.open('conf/janusgraph-hbase.properties')
==>standardjanusgraph[hbase:[127.0.0.1]]
gremlin> GraphOfTheGodsFactory.loadWithoutMixedIndex(graph, true)
==>null
gremlin> g = graph.traversal() #构建图
==>graphtraversalsource[standardjanusgraph[hbase:[127.0.0.1]], standard]
```
#### 全局图索引
```sql
gremlin> saturn = g.V().has('name', 'saturn').next() #查询节点名称为‘saturn’的节点
==>v[4216]
gremlin> g.V(saturn).valueMap() #查询某个节点数据
==>[name:[saturn],age:[10000]]
gremlin> g.V(saturn).in('father').in('father').values('name') #查询某节点父节点的父节点的‘name’值
==>hercules
gremlin> g.E().has('place', geoWithin(Geoshape.circle(37.97, 23.72, 50))) #查询坐标在50公里以内的节点
18:17:28 WARN  org.janusgraph.graphdb.transaction.StandardJanusGraphTx  - Query requires iterating over all vertices [(place geoWithin BUFFER (POINT (23.72 37.97), 0.44966))]. For better performance, use indexes
==>e[4d8-3c0-7x1-6gw][4320-battled->8384]
==>e[3z0-3c0-7x1-6hs][4320-battled->8416]
gremlin> g.E().has('place', geoWithin(Geoshape.circle(37.97, 23.72, 50))).as('source').inV().as('god2').select('source').outV().as('god1').select('god1', 'god2').by('name') #查询出的节点，把入节点命名为‘god2’，出节点命名为‘god1’，查询god1，god2的名称
18:17:57 WARN  org.janusgraph.graphdb.transaction.StandardJanusGraphTx  - Query requires iterating over all vertices [(place geoWithin BUFFER (POINT (23.72 37.97), 0.44966))]. For better performance, use indexes
==>[god1:hercules,god2:hydra]
==>[god1:hercules,god2:nemean]
```
#### 图的遍历示例：
```sql
gremlin> hercules = g.V(saturn).repeat(__.in('father')).times(2).next() #同in('father').in('father')
==>v[4224]
gremlin> g.V(hercules).out('father', 'mother') #出去节点关系为father，mother
==>v[4152]
==>v[8320]
gremlin> g.V(hercules).out('father', 'mother').values('name') #出去节点关系为father，mother的名字
==>jupiter
==>alcmene
gremlin> g.V(hercules).out('father', 'mother').label() #出去节点关系为father，mother的type
==>god
==>human
gremlin> hercules.label() #Hercules的type值
==>demigod

gremlin> g.V(hercules).out('battled')
==>v[8248]
==>v[12416]
==>v[16512]
gremlin> g.V(hercules).out('battled').valueMap()
==>[name:[nemean]]
==>[name:[hydra]]
==>[name:[cerberus]]
gremlin> g.V(hercules).outE('battled').has('time', gt(1)).inV().values('name')
==>cerberus
==>hydra

gremlin> g.V(hercules).outE('battled').has('time', gt(1)).inV().values('name').toString()
==>[GraphStep(vertex,[v[4224]]), VertexStep(OUT,[battled],edge), HasStep([time.gt(1)]), EdgeVertexStep(IN), PropertiesStep([name],value)]
```

#### 更复杂的图的遍历示例：
```sql
gremlin> pluto = g.V().has('name', 'pluto').next()
==>v[4232]
gremlin> g.V(pluto).out('lives').in('lives').values('name')
==>pluto
==>cerberus
gremlin> g.V(pluto).out('lives').in('lives').where(is(neq(pluto))).values('name')
==>cerberus
gremlin> g.V(pluto).as('x').out('lives').in('lives').where(neq('x')).values('name')
==>cerberus

gremlin> g.V(pluto).out('brother').out('lives').values('name')
==>sea
==>sky
gremlin> g.V(pluto).out('brother').as('god').out('lives').as('place').select('god', 'place')
==>[god:v[4104],place:v[4336]]
==>[god:v[4240],place:v[4168]]
gremlin> g.V(pluto).out('brother').as('god').out('lives').as('place').select('god', 'place').by('name')
==>[god:neptune,place:sea]
==>[god:jupiter,place:sky]

gremlin> g.V(pluto).outE('lives').values('reason')
==>no fear of death
gremlin> g.E().has('reason', textContains('loves'))
20:05:02 WARN  org.janusgraph.graphdb.transaction.StandardJanusGraphTx  - Query requires iterating over all vertices [(reason textContains loves)]. For better performance, use indexes
==>e[35t-360-9hx-3cg][4104-lives->4336]
==>e[2du-39s-9hx-37s][4240-lives->4168]
gremlin> g.E().has('reason', textContains('loves')).as('source').values('reason').as('reason').select('source').outV().values('name').as('god').select('source').inV().values('name').as('thing').select('god', 'reason', 'thing')
20:05:33 WARN  org.janusgraph.graphdb.transaction.StandardJanusGraphTx  - Query requires iterating over all vertices [(reason textContains loves)]. For better performance, use indexes
==>[god:neptune,reason:loves waves,thing:sea]
==>[god:jupiter,reason:loves fresh breezes,thing:sky]
```
