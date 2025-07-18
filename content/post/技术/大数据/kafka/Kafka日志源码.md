---
categories:
- 技术
- 大数据
date: '2021-02-04 13:05:07+08:00'
tags:
- kafka
thumbnailImage: //www.azheimage.top/markdown-img-paste-2019011014402315.png
title: Kafka日志源码
---

Kafka 日志段部分源码解读

<!--more-->

kafka.log.LogSegment
LogSegment class；
LogSegment object；
LogFlushStats object。LogFlushStats 结尾有个 Stats，它是做统计用的，主要负责为日志落盘进行计时。

### 日志段

Kafka 日志在磁盘上的组织架构如下图所示：
![](https://www.azheimage.top/markdown-img-paste-20200702120455344.png)
append 方法接收 4 个参数，分别表示待写入消息批次中消息的最大位移值、最大时间戳、最大时间戳对应消息的位移以及真正要写入的消息集合。下面这张图展示了 append 方法的完整执行流程：
![](https://www.azheimage.top/markdown-img-paste-20200702120559695.png)
下图展示了 read 方法的完整执行逻辑：
![](https://www.azheimage.top/markdown-img-paste-20200702120641514.png)
recover 的处理逻辑：
![](https://www.azheimage.top/markdown-img-paste-20200702120713299.png)
今天，我们对 Kafka 日志段源码进行了重点的分析，包括日志段的 append 方法、read 方法和 recover 方法。

1. append 方法：我重点分析了源码是如何写入消息到日志段的。你要重点关注一下写操作过程中更新索引的时机是如何设定的。
2. read 方法：我重点分析了源码底层读取消息的完整流程。你要关注下 Kafka 计算待读取消息字节数的逻辑，也就是 maxSize、maxPosition 和 startOffset 是如何共同影响 read 方法的。
3. recover 方法：这个操作会读取日志段文件，然后重建索引文件。再强调一下，这个操作在执行过程中要读取日志段文件。因此，如果你的环境上有很多日志段文件，你又发现 Broker 重启很慢，那你现在就知道了，这是因为 Kafka 在执行 recover 的过程中需要读取大量的磁盘文件导致的。你看，这就是我们读取源码的收获。

![](https://www.azheimage.top/markdown-img-paste-20200702120342810.png)

### 日志

Log 源码位于 Kafka core 工程的 log 源码包下，文件名是 Log.scala。总体上，该文件定义了 10 个类和对象，如下图所示
![](https://www.azheimage.top/markdown-img-paste-20200702173824894.png)

Log Object 定义的所有常量。耳熟能详的.log、.index、.timeindex 和.txnindex 我就不解释了，我们来了解下其他几种文件类型。

- .snapshot 是 Kafka 为幂等型或事务型 Producer 所做的快照文件。鉴于我们现在还处于阅读源码的初级阶段，事务或幂等部分的源码我就不详细展开讲了。
- .deleted 是删除日志段操作创建的文件。目前删除日志段文件是异步操作，Broker 端把日志段文件从.log 后缀修改为.deleted 后缀。如果你看到一大堆.
- deleted 后缀的文件名，别慌，这是 Kafka 在执行日志段文件删除。.cleaned 和.swap 都是 Compaction 操作的产物，等我们讲到 Cleaner 的时候再说。
- -delete 则是应用于文件夹的。当你删除一个主题的时候，主题的分区文件夹会被加上这个后缀。
- -future 是用于变更主题分区文件夹地址的，属于比较高阶的用法。总之，记住这些常量吧。记住它们的主要作用是，以后不要被面试官唬住！开玩笑，其实这些常量最重要的地方就在于，它们能够让你了解 Kafka 定义的各种文件类型。

![](https://www.azheimage.top/markdown-img-paste-20200713113759826.png)
![](https://www.azheimage.top/markdown-img-paste-20200713113819807.png)

![](https://www.azheimage.top/markdown-img-paste-20200713140006799.png)

kafka 索引用的是改进版二分查找，社区提出了改进版的二分查找策略，也就是缓存友好的搜索算法。总体的思路是，代码将所有索引项分成两个部分：热区（Warm Area）和冷区（Cold Area），然后分别在这两个区域内执行二分查找算法，如下图所示：
![](https://www.azheimage.top/markdown-img-paste-20200713144044314.png)

![](https://www.azheimage.top/markdown-img-paste-20200713150305286.png)

![](https://www.azheimage.top/markdown-img-paste-2020071316240269.png)

nio 网络通信
![](https://www.azheimage.top/markdown-img-paste-20200713163144464.png)

socketserver
![](https://www.azheimage.top/markdown-img-paste-20200713163527834.png)

processors
![](https://www.azheimage.top/markdown-img-paste-20200713164501721.png)

![](https://www.azheimage.top/markdown-img-paste-20200713164802536.png)

![](https://www.azheimage.top/markdown-img-paste-20200713165300245.png)

![](https://www.azheimage.top/markdown-img-paste-20200713170032374.png)

监听器优先级
![](https://www.azheimage.top/markdown-img-paste-20200713174326106.png)
