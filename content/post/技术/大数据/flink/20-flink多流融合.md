---
categories:
- 技术
- 大数据
date: '2023-07-04 13:06:59+08:00'
tags:
- flink
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716210809882.png
title: 20-flink多流融合
---

DataStream 和 DataSet 中都存在 CoGroup、Join 这两个 Operator，而 Connect 只适用于处理 DataStream

<!--more-->

## Flink CoGroup、Join 以及 Connect

### CoGroup

该操作是将两个数据流/集合按照 key 进行 group，然后将相同 key 的数据进行处理，但是它和 join 操作稍有区别，它在一个流/数据集中没有找到与另一个匹配的数据还是会输出。

- 语法是：coGroup where equalTo window apply ，用于 DataSet 时的语法是：coGroup where equalTo with
- 把 2 个实时窗口内或 2 个数据集合内 key 相同的数据分组同一个分区，key 不能匹配上的数据（只在一个窗口或集合内存在的数据）也分组到另一个分区上。

  1.在 DataStream 中

- 侧重与 group，对同一个 key 上的两组集合进行操作。
- 如果在一个流中没有找到与另一个流的 window 中匹配的数据，任何输出结果，即只输出一个流的数据。
- 仅能使用在 window 中。

  2.在 DataSet 中
  使用 cogroup 操作将两个集合中 key 相同数据合并

### join

join 操作很常见，与我们数据库中常见的 inner join 类似，它数据的数据侧重与 pair，它会按照一定的条件取出两个流或者数据集中匹配的数据返回给下游处理或者输出。

我们都知道 window 有三种 window 类型，因此 join 与其相对，也有三种，除此之外，还有 Interval join：

Tumbling Window Join
Sliding Window Join
Session Window Join
Interval Join
它的编程模型如下：

```scala
stream.join(otherStream)
    .where(<KeySelector>)
    .equalTo(<KeySelector>)
    .window(<WindowAssigner>)
    .apply(<JoinFunction>)
```

Interval Join 会将两个数据流按照相同的 key，并且在其中一个流的时间范围内的数据进行 join 处理。通常用于把一定时间范围内相关的分组数据拉成一个宽表。我们通常可以用类似下面的表达式来使用 interval Join 来处理两个数据流

### connect

该操作不同于上面两个操作，只适用操作 DataStream，它会将两个流中匹配的数据进行处理，不匹配不会进行处理，它会分别处理两个流，比上面的两个操作更加自由

- ConnectedStreams 只能连接两个流，而 union 可以连接多于两个流
- ConnectedStreams 连接的两个流类型可以不一致，而 union 连接的流的类型必须一致。
- ConnectedStreams 会对两个流的数据应用不同的处理方法，并且双流之间可以共享状态。这在第一个流的输入会影响第二个流时, 会非常有用。

### union

1 用于 DataStream 时,返回是 Datastream;用于 DataSet 时,返回是 DataSet;

2 可以多个流一起合并（stream1.union(stream2,stream3,stream4)），合并结果是一个新 Datastream；只能 2 个 DataSet 一起合并，合并结果是一个新 DataSet

3 无论是合并 Datastream 还是合并 DataSet，都不去重，2 个源的消息或记录都保存。

4 不可以 union 2 个类型不同的流或 union 2 个类型不同的数据集
