---
categories:
- 技术
- 大数据
date: '2020-07-26 14:25:31+08:00'
tags:
- flink
thumbnailImage: //www.azheimage.top/markdown-img-paste-20181113165255716.png
title: 5-flinkSQL参数
---
FlinkSQL 参数理解
<!--more-->
- 'sink.partition-commit.trigger'='partition-time'

- 'sink.partition-commit.policy.kind'='metastore,success-file'
分区提交策略，可以理解为使分区对下游可见的附加操作。metastore表示更新Hive Metastore中的表元数据，success-file则表示在分区内创建_SUCCESS标记文件。

- 'sink.partition-commit.delay'='1 min'
触发分区提交的时间特征。默认为processing-time，即处理时间，很显然在有延迟的情况下，可能会造成数据分区错乱。所以这里使用partition-time，即按照分区时间戳（即分区内数据对应的事件时间）来提交

- 'partition.time-extractor.timestamp-pattern'='$dt $h:$m:00'
触发分区提交的延迟。在时间特征设为partition-time的情况下，当水印时间戳大于分区创建时间加上此延迟时，分区才会真正提交。此值最好与分区粒度相同，例如若Hive表按1小时分区，此参数可设为1 h，若按10分钟分区，可设为10 min。

- 'sink.rolling-policy.file-size'='100M'
滚动策略200M,分区文件的最大值，超过这个大小，将会启动一个新文件。

- 'sink.rolling-policy.check-interval'='1min'
滚动文件的时间间隔:参考TimeUtils，分区文件滚动的最大时间间隔，超过这个时间，将会新启动一个文件

- 'partition.time-extractor.kind'='default'
多久检查一次非活跃的bucket

### 滚动策略

key|default|type|description
-|-|-|-
sink.rolling-policy.file-size|128MB|MemorySize|分区文件的最大值，超过这个大小，将会启动一个新文件。
sink.rolling-policy.rollover-interval|30 m|Duration|分区文件滚动的最大时间间隔，超过这个时间，将会新启动一个文件
sink.rolling-policy.check-interval|1 m|Duration|一个时间间隔，定期去检查上面那个配置指定的策略下，文件是否应该滚动生成新文件.

- 在写入列格式（比如parquet、orc）的时候，上述的配置和checkpoint的间隔一起来控制滚动策略，也就是说sink.rolling-policy.file-size、sink.rolling-policy.rollover-interval、checkpoint间隔，这三个选项，只要有一个条件达到了，然后就会触发分区文件的滚动，结束上一个文件的写入，生成新文件。
- 对于写入行格式的数据，比如json、csv，主要是靠sink.rolling-policy.file-size、sink.rolling-policy.rollover-interval，也就是文件的大小和时间来控制写入数据的滚动策略.

### 分区提交
在往一个分区写完了数据之后，我们希望做一些工作来通知下游。比如在分区目录写一个SUCCESS文件，或者是对于hive来说，去更新metastore的数据，自动刷新一下分区等等。
分区的提交主要依赖于触发器和提交的策略：

- 触发器：即什么时候触发分区的提交
- 提交策略：也就是分区写完之后我们做什么，目前系统提供了两种内置策略：
  1. 往分区目录写一个空SUCCESS文件；
  2. 更新元数据.

### 分区提交触发器
key|default|type|解释
-|-|-|-
sink.partition-commit.trigger|process-time| String |触发器的类型，目前系统提供了两种：process-time 和 partition-time，如果选择了process-time，则当系统时间大于processtime的时候触发提交，如果选择了partition-time，则需要先从分区字段里面抽取分区时间的开始时间，然后当水印大于这个分区时间的时候触发分区的提交.
sink.partition-commit.delay|0 s|Duration|提交分区的延迟时间

1. process-time.  这种提交方式依赖于系统的时间，一旦遇到数据延迟等情况，会造成分区和分区的数据不一致。
2. partition-time ：这种情况需要从分区字段里抽取出来相应的pattern，具体可参考下一个段落分区的抽取。
3. sink.partition-commit.delay：一旦这个数值设置不为0，则在process-time情况下，当系统时间大于分区创建时间加上delay延迟，会触发分区提交； 如果是在partition-time 情况下，则需要水印大于分区创建时间加上delay时间，会触发分区提交.


第一个参数process-time、partition-time，我们不用做过多的解释，就类似于flink中的processtime和eventtime。
第二个参数sink.partition-commit.delay我们用实际案例解释下：
比如我们配置的是分区是/yyyy-MM-dd/HH/,写入的是ORC列格式，checkpoint配置的间隔是一分钟，也就是默认情况下会每分钟生成一个orc文件，最终会在每个分区(/yyyy-MM-dd/HH/)下面生成60个orc文件。
比如当前系统正在写入/day=2020-07-06/h=10/分区的数据，那么这个分区的创建时间是2020-07-06 10:00:00，如果这个delay配置采用的是默认值，也就是0s，这个时候当写完了一个ORC文件，也就是2020-07-06 10:01:00分钟的时候，就会触发分区提交，比如更新hive的元数据，这个时候我们去查询hive就能查到刚刚写入的文件；如果我们想/day=2020-07-06/h=10/这个分区的60个文件都写完了再更新分区，那么我们可以将这个delay设置成 1h，也就是等到2020-07-06 11:00:00的时候才会触发分区提交，我们才会看到/2020-07-06/10/分区下面的所有数据

### 分区时间的抽取
从分区值里抽取分区时间，我们可以理解为上面触发器参数配置为partition-time的时候，分区的创建时间，当水印大于这个时间+delay的时候触发分区的提交.

Key|Default|Type|解释
-|-|-|-
partition.time-extractor.kind| default | String |抽取分区的方式，目前有default和custom两种，如果是default，需要配置partition.time-extractor.timestamp-pattern，如果是custom，需要配置自定义class
partition.time-extractor.class|null|String|自定义class
partition.time-extractor.timestamp-pattern|null|String|从分区值中抽取时间戳的模式，需要组织成yyyy-MM-dd HH:mm:ss格式，比如 对于上面我们提到的分区/yyyy-MM-dd/HH/，其中两个分区字段对应的字段名分为是dt和hour，那么我们这个timestamp-pattern 可以配置成'hour:00:00'

自定义抽取分区时间的话，需要实现PartitionTimeExtractor接口：
```java
public interface PartitionTimeExtractor extends Serializable {

 String DEFAULT = "default";
 String CUSTOM = "custom";

 /**
  * Extract time from partition keys and values.
  */
 LocalDateTime extract(List<String> partitionKeys, List<String> partitionValues);
    ...................
}
```

### 分区提交策略
定义了分区提交的策略，也就是写完分区数据之后做什么事情，目前系统提供了以下行为：
metastore，只支持hive table，也就是写完数据之后，更新hive的元数据.success file:  写完数据，往分区文件写一个success file.自定义

key|Default|Type|描述
-|-|-|-
sink.partition-commit.policy.kind|null|string|可选：metastore,success-file,custom，这个可以写一个或者多个，比如可以这样，'metastore,success-file'
sink.partition-commit.policy.class|null|string|如果上述选择custom的话，这里指定相应的class
sink.partition-commit.success-file.name|null|string|如果上述选择的是success-file，这里可以指定写入的文件名，默认是 _SUCCESS。checkpoint 是用来切分文件的时间间隔。_SUCCESS delay+watermark>分区时间就生成
'sink.partition-commit.success-file.name' | null|string|成功文件名称。默认_success。

