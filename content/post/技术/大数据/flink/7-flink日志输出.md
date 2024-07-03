---
categories:
- 技术
- 大数据
date: '2020-09-12 14:29:08+08:00'
tags:
- flink
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716211711809.png
title: 7-flink日志输出
---
flink日志输出冲突

解决flink项目中日志输出有冲突，或者是日志输出配置文件没有生效
<!--more-->
1. 通过jar包依赖查找maven依赖中，与log4j相关的包
dependency:tree
2. execution去除相关的log4j包
3. 添加日志相关依赖
```xml
<dependency>
  <groupId>org.slf4j</groupId>
  <artifactId>slf4j-api</artifactId>
</dependency>

<dependency>
  <groupId>org.slf4j</groupId>
  <artifactId>slf4j-log4j12</artifactId>
</dependency>
<dependency>
  <groupId>log4j</groupId>
  <artifactId>log4j</artifactId>
</dependency>
```
