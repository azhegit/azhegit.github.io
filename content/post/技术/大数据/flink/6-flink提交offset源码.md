---
categories:
- 技术
- 大数据
date: '2020-09-11 14:28:21+08:00'
tags:
- flink
thumbnailImage: //www.azheimage.top/markdown-img-paste-2018111316510833.png
title: 6-flink提交offset源码
---
Flink提交kafka offset源码

flink 消费 kafka 数据，提交消费组 offset方式 有三种类型
<!--more-->
- DISABLED 关闭offset自动提交
- ON_CHECKPOINTS 完成checkpoint时提交offset
- KAFKA_PERIODIC 使用内部Kafka客户机的自动提交功能，定期将偏移量提交回Kafka

四种情况
checkpoint|checkpoint提交|kafka client设置提交|是否提交offset
-|-|-|-
开启checkpoint</br>`env.enableCheckpointing(1000)`|默认开启checkpoint提交|是否开启不起作用|在 checkpoint 完成后提交✅
开启 checkpoint</br>`env.enableCheckpointing(1000)`|禁用 checkpoint 提交</br>`consumer.setCommitOffsetsOnCheckpoints(false)`|是否开启不起作用|不提交offset❌
默认不开启 checkpoint|是否开启不起作用|开启kafka client的自动提交</br> `prop.setProperty("enable.auto.commit", "true")`</br>`prop.setProperty("auto.commit.interval.ms", "100")`|kafka client周期性自动提交✅
默认不开启 checkpoint|是否开启不起作用|kafka client的自动提交</br> `prop.setProperty("enable.auto.commit", "true")`</br>`prop.setProperty("auto.commit.interval.ms", "100")`|不提交offset❌


核心判断代码：
```java
package org.apache.flink.streaming.connectors.kafka.config;

import org.apache.flink.annotation.Internal;

/**
 * Utilities for {@link OffsetCommitMode}.
 */
@Internal
public class OffsetCommitModes {

	/**
	 * Determine the offset commit mode using several configuration values.
	 *
	 * @param enableAutoCommit whether or not auto committing is enabled in the provided Kafka properties.
	 * @param enableCommitOnCheckpoint whether or not committing on checkpoints is enabled.
	 * @param enableCheckpointing whether or not checkpoint is enabled for the consumer.
	 *
	 * @return the offset commit mode to use, based on the configuration values.
	 */
	public static OffsetCommitMode fromConfiguration(
			boolean enableAutoCommit,
			boolean enableCommitOnCheckpoint,
			boolean enableCheckpointing) {

		if (enableCheckpointing) {
			// if checkpointing is enabled, the mode depends only on whether committing on checkpoints is enabled
			return (enableCommitOnCheckpoint) ? OffsetCommitMode.ON_CHECKPOINTS : OffsetCommitMode.DISABLED;
		} else {
			// else, the mode depends only on whether auto committing is enabled in the provided Kafka properties
			return (enableAutoCommit) ? OffsetCommitMode.KAFKA_PERIODIC : OffsetCommitMode.DISABLED;
		}
	}
}
```
