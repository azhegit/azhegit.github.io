---
categories:
- 技术
- 数据库
date: 2018-07-16 19:18:38+08:00
tags:
- janusgraph
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716212442829.png
title: Janusgraph学习--3(Greemlin查询语言)
---

Gremlin是JanusGraph的查询语言，用于从图中检索数据和修改数据。Gremlin是一种面向路径的语言，它简洁地表达了复杂的图形遍历和变异操作。Gremlin是一种函数式语言，遍历运算符被链接在一起形成类似路径的表达式。

<!--more-->


Gremlin是Apache TinkerPop的一个组件。它独立于JanusGraph开发，并得到大多数图形数据库的支持。通过Gremlin查询语言在JanusGraph之上构建应用程序，用户可以避免供应商锁定，因为他们的应用程序可以迁移到支持Gremlin的其他图形数据库。

# 本文讲述Gremlin语言：
*初次接触￣□￣｜｜，学习记录一下*
## Greemlin Logo：
![](https://www.azheimage.top/markdown-img-paste-20180716174340261.png)
* ### Gods图

![](https://www.azheimage.top/markdown-img-paste-20180713182054834.png)

本节是Gremlin查询语言的简要概述。有关Gremlin的更多信息，请参阅以下资源：

[完整的Gremlin手册](http://tinkerpop.apache.org/docs/3.2.9/reference/)：所有Gremlin步骤的参考手册。

[Gremlin控制台教程](http://tinkerpop.apache.org/docs/3.2.9/tutorials/the-gremlin-console/)：了解如何有效地使用Gremlin控制台以交互方式遍历和分析图形。

[Gremlin Recipes](http://tinkerpop.apache.org/docs/3.2.9/recipes/)：Gremlin的最佳实践和常见遍历模式的集合。

[Gremlin语言驱动程序](http://tinkerpop.apache.org/index.html#language-drivers)：使用不同的编程语言连接到Gremlin服务器，包括Go，JavaScript，.NET / C＃，PHP，Python，Ruby，Scala和TypeScript。

[Gremlin语言变体](http://tinkerpop.apache.org/docs/3.2.9/tutorials/gremlin-language-variants/)：学习如何使用宿主编程语言嵌入Gremlin。

[面向SQL开发人员的 Gremlin](http://sql2gremlin.com/)：使用SQL查询数据时发现的典型模式学习Gremlin。

* ### 介绍性遍历
Gremlin查询是从左到右计算的一系列操作/函数。下面通过第3章“ [入门](https://docs.janusgraph.org/latest/getting-started.html)”中讨论的Gods数据集图表提供了一个简单的祖父查询。
```sql
graph = JanusGraphFactory.open('conf/janusgraph-hbase.properties')
==>standardjanusgraph[hbase:[127.0.0.1]]
gremlin>  GraphOfTheGodsFactory.loadWithoutMixedIndex(graph, true)
==>null
gremlin> g = graph.traversal()
==>graphtraversalsource[standardjanusgraph[hbase:[127.0.0.1]], standard]
gremlin>
gremlin> g.V().has('name', 'hercules').out('father').out('father').values('name')
==>saturn
```
>上面的查询可以读取：
g：对于当前的图遍历。
V：对于图中的所有顶点
has('name', 'hercules')：将顶点过滤到名称属性为“hercules”（只有一个）的顶点。
out('father')：从hercules遍历即将离任的父亲边缘。
out('father')：从hercules的父亲的顶点（即Jupiter）遍历外出的父亲边缘。
name：获取“hercules”顶点祖父的名称属性。

总之，这些步骤形成了类似路径的遍历查询。每个步骤都可以分解并显示其结果。在构建更大，更复杂的查询链时，这种构建遍历/查询的方式很有用。

```sql
gremlin> g
==>graphtraversalsource[standardjanusgraph[hbase:[127.0.0.1]], standard]
gremlin> g.V().has('name', 'hercules')
==>v[8408]
//hercules的父亲
gremlin> g.V().has('name', 'hercules').out('father')
==>v[4336]
gremlin> g.V().has('name', 'hercules').out('father').out('father')
==>v[4312]
gremlin> g.V().has('name', 'hercules').out('father').out('father').values('name')
==>saturn
```
为了更好的检查，通常会选择更好的返回方式，比如查看属性，而不是一个id
```sql
gremlin> g.V().has('name', 'hercules').values('name')
==>hercules
gremlin> g.V().has('name', 'hercules').out('father').values('name')
==>jupiter
gremlin> g.V().has('name', 'hercules').out('father').out('father').values('name')
==>saturn
```

对于查看整个父亲分支树，提供这种更复杂的遍历以展示语言的灵活性和表达性。对Gremlin的有效掌握为JanusGraph用户提供了流畅导航底层图形结构的能力。
```sql
gremlin> g.V().has('name','hercules').repeat(out('father')).emit().values('name')
==>jupiter
==>saturn
```

* ### 下面提供了一些遍历示例。
```sql
gremlin> hercules = g.V().has('name', 'hercules').next()
==>v[8408]
gremlin>  g.V(hercules).out('father', 'mother').label()
==>god
==>human
gremlin> g.V(hercules).out('battled').label()
==>monster
==>monster
==>monster
gremlin> g.V(hercules).out('battled').valueMap()
==>[name:[hydra]]
==>[name:[nemean]]
==>[name:[cerberus]]
```

鉴于当前图中只有一个战斗者（hercules）,另一个战斗者（为了举例）被添加到图形中，Gremlin展示了如何将顶点和边缘添加到图形中。

```sql
gremlin> theseus = graph.addVertex('human')
==>v[12328]
gremlin> theseus.property('name', 'theseus')
==>vp[name->theseus]
gremlin> cerberus = g.V().has('name', 'cerberus').next()
==>v[8416]
gremlin> battle = theseus.addEdge('battled', cerberus, 'time', 22)
==>e[3yd-9ig-7x1-6hs][12328-battled->8416]
gremlin> battle.values('time')
==>22
```
添加顶点时，可以提供可选的顶点标签。添加边时必须指定边标签。可以在顶点和边上设置作为键值对的属性。使用SET或LIST基数定义属性键addProperty时，必须在向顶点添加相应属性时使用。
```sql
gremlin> g.V(hercules).as('h').out('battled').in('battled').where(neq('h')).values('name')
==>theseus
```
上面的例子中有4个链功能：out，in，except，和values（即name是简写values('name')）。每个的函数签名在下面逐条列出，其中V是顶点并且U是任何对象，其中V是其子集U。

out: V -> V
in: V -> V
except: U -> U
values: V -> U
将函数链接在一起时，传入类型必须与传出类型U匹配，其中匹配任何内容。因此，上面的“共同战斗/盟友”遍历是正确的。


* ### 迭代遍历
Gremlin控制台的一个便利功能是它会自动迭代从gremlin>提示执行的查询中的所有结果。这在REPL环境中运行良好，因为它将结果显示为String。当您转向编写Gremlin应用程序时，了解如何显式迭代遍历非常重要，因为应用程序的遍历不会自动迭代。这些是迭代的一些常用方法Traversal：

iterate() - 预期或可忽略零结果。
next() - 获得一个结果。一定hasNext()要先检查一下。
next(int n)- 获得下一个n结果。一定hasNext()要先检查一下。
toList() - 将所有结果作为列表获取。如果没有结果，则返回空列表。
下面显示了一个Java代码示例来演示这些概念：


```java
Traversal t = g.V().has("name", "pluto"); // 定义遍历
//注意遍历未执行/迭代
Vertex pluto = null;
if (t.hasNext()) { //检查结果是否可用
    pluto = g.V().has("name", "pluto").next(); //得到一个结果
    g.V(pluto).drop().iterate(); //执行遍历以从图中删除pluto
}
//注意可以克隆遍历以便重用
Traversal tt = t.asAdmin().clone();
if (tt.hasNext()) {
    System.err.println("pluto was not dropped!");
}
List<Vertex> gods = g.V().hasLabel("god").toList(); //找到所有的神
```
