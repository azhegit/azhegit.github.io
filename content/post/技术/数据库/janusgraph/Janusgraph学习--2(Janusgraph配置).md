---
categories:
- 技术
- 数据库
date: 2018-07-16 09:18:38+08:00
tags:
- janusgraph
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716213938138.png
title: Janusgraph学习--2(Janusgraph配置)
---

JanusGraph是一个可扩展的图形数据库，专门用于存储和查询包含分布在多机群集中的数千亿个顶点和边缘的图形。JanusGraph是一个事务数据库，可以支持数千个并发用户实时执行复杂的图遍历。
<!--more-->
<!--toc-->
# 本文讲述JanusgraphE的配置信息：
*初次接触￣□￣｜｜，学习记录一下*
## Janusgraph Logo：
![](https://www.azheimage.top/markdown-img-paste-20180713173354102.png)
* ### JanusGraph配置：
JanusGraph图数据库集群由一个或多个JanusGraph实例组成。要打开JanusGraph实例，必须提供一个配置，指定如何设置JanusGraph。

JanusGraph分为本地和全局配置. 本地配置适用于单独的JanusGraph实例. 全局配置适用于集群中的全部实例. JanusGraph有以下5个范围的配置:
* LOCAL 只适用于单独的JanusGraph实例, 而且需要在实例初始化时提供
* MASKABLE 用本地配置文件启动的单独实例, MASKABLE参数可以被覆盖. 如果本地配置文件没有提供参数, 会读取全局集群的配置.
* GLOBAL 从全局集群配置中读取, 而且不能被覆盖
* GLOBAL_OFFLINE 与GLOBAL类似, 但修改这类参数, 需要启动集群, 确保集群中获得同一个值
* FIXED 与GLOBAL类似, 但这些值不能被修改
当集群中第一个实例启动, 全局配置便被从本地文件初始化了. 可以通过系统提供的API来修改全局配置参数. 调用实例g.getManagementSystem()方法,可以访问管理API.例如, 修改一个集群默认的缓存行为

```sql
gremlin> graph = JanusGraphFactory.open('conf/janusgraph-hbase.properties')
==>standardjanusgraph[hbase:[127.0.0.1]]
gremlin> mgmt = graph.openManagement()
==>org.janusgraph.graphdb.database.management.ManagementSystem@7ed3df3b
gremlin> mgmt.get('cache.db-cache')
==>false
gremlin> mgmt.set('cache.db-cache', true)
==>org.janusgraph.diskstorage.configuration.UserModifiableConfiguration@2cd4e16a
gremlin> mgmt.get('cache.db-cache')
==>true
gremlin> mgmt.commit()
==>null
```

* ### 修改离线参数
修改配置参数不会影响运行着的实例, 只会对新启动的实例有作用. 修改GLOBAL_OFFLINE级别的配置, 需要重启集群, 让全部实例生效. 如下步骤:
* 集群仅留一个实例
* 连接到该实例上
* 确保全部业务都关闭
* 确保没有新的业务被启动
* 打开管理API
* 修改配置参数
* 调用commit方法, commit方法会自动将实例停止
* 重启全部实例

* ### 边缘标签多样性
##### 多重性设置

* MULTI：允许任意一对顶点之间的同一标签的多个边。换句话说，该图是关于这种边缘标签的多图。边缘多样性没有约束。
* SIMPLE：在任何一对顶点之间最多允许此类标签的一个边缘。换句话说，该图是关于标签的简单图。确保边缘对于给定标签和顶点对是唯一的。
* MANY2ONE：在图形中的任何顶点上最多允许此标签的一个输出边缘，但不对输入边缘施加约束。边缘标签mother是MANY2ONE多样性的一个例子，因为每个人最多只有一个母亲，但母亲可以有多个孩子。
* ONE2MANY：在图形中的任何顶点上最多允许此标签的一个传入边缘，但不对输出边缘施加约束。边缘标签winnerOf是ONE2MANY多样性的一个例子，因为每个比赛最多只赢一个人，但一个人可以赢得多个比赛。
* ONE2ONE：在图表的任何顶点上最多允许此标签的一个输入边和一个输出边。边缘标签结婚是ONE2ONE多样性的一个例子，因为一个人与另一个人结婚。
默认的多重性是**MULTI**。通过调用make()构建器上的方法来完成边缘标签的定义，该构建器返回定义的边缘标签，如以下示例所示。
sql
```sql
gremlin> mgmt = graph.openManagement()
==>org.janusgraph.graphdb.database.management.ManagementSystem@76ececd
gremlin> follow = mgmt.makeEdgeLabel('follow').multiplicity(MULTI).make()
==>follow
gremlin> mother = mgmt.makeEdgeLabel('mother').multiplicity(MANY2ONE).make()
==>mother
gremlin> mgmt.commit()
==>null
```

* ### Property Key Cardinality
使用cardinality(Cardinality)定义与在任何给定的顶点的键关联的值允许的基数。
##### 基数设置
* SINGLE：对于此键，每个元素最多允许一个值。换句话说，键→值映射对于图中的所有元素都是唯一的。属性键birthDate是SINGLE基数的一个例子，因为每个人只有一个出生日期。
* LIST：允许每个元素的任意数量的值用于此类键。换句话说，密钥与允许重复值的值列表相关联。假设我们将传感器建模为图形中的顶点，则属性键sensorReading是具有LIST基数的示例，以允许记录大量（可能重复的）传感器读数。
* SET：允许多个值，但每个元素没有重复值用于此类键。换句话说，密钥与一组值相关联。name如果我们想要捕获个人的所有姓名（包括昵称，婚前姓名等），则属性键具有SET基数。
默认基数设置为SINGLE。请注意，边和属性上使用的属性键具有基数SINGLE。不支持为边或属性上的单个键附加多个值。

```sql
gremlin> mgmt = graph.openManagement()
==>org.janusgraph.graphdb.database.management.ManagementSystem@20ab76ee
gremlin> birthDate = mgmt.makePropertyKey('birthDate').dataType(Long.class).cardinality(Cardinality.SINGLE).make()
==>birthDate
gremlin> name = mgmt.makePropertyKey('name').dataType(String.class).cardinality(Cardinality.SET).make()
==>name
gremlin> sensorReading = mgmt.makePropertyKey('sensorReading').dataType(Double.class).cardinality(Cardinality.LIST).make()
==>sensorReading
gremlin> mgmt.commit()
==>null
```

* ### 关系类型
边标签和属性键共同称为关系类型。关系类型的名称在图形中必须是唯一的，这意味着属性键和边缘标签不能具有相同的名称。JanusGraph API中有一些方法可以查询是否存在或检索包含属性键和边缘标签的关系类型。

```sqlsql
gremlin> mgmt = graph.openManagement()
==>org.janusgraph.graphdb.database.management.ManagementSystem@294aba23
gremlin> if (mgmt.containsRelationType('name'))
......1>     name = mgmt.getPropertyKey('name')
==>name
gremlin> mgmt.getRelationTypes(EdgeLabel.class)
==>follow
==>mother
gremlin> mgmt.commit()
==>null
```

* ### 像边一样，顶点有标签。与边缘标签不同，顶点标签是可选的。顶点标签可用于区分不同类型的顶点，例如用户顶点和产品顶点。

虽然标签在概念和数据模型级别是可选的，但JanusGraph会为所有顶点分配标签作为内部实现细节。由addVertex方法创建的顶点使用JanusGraph的默认标签。

要创建标签，请调用makeVertexLabel(String).make()打开的图形或管理事务，并提供顶点标签的名称作为参数。顶点标签名称在图表中必须是唯一的。

```sql
gremlin> mgmt = graph.openManagement()
==>org.janusgraph.graphdb.database.management.ManagementSystem@6ec63f8
gremlin> person = mgmt.makeVertexLabel('person').make()
==>person
gremlin> mgmt.commit()
==>null
//创建一个标记的顶点
gremlin> person = graph.addVertex(label, 'person')
==>v[4136]
//创建一个未标记的顶点
gremlin> v = graph.addVertex()
==>v[4288]
gremlin> graph.tx().commit()
==>null
```
