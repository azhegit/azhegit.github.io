---
categories:
- 技术
- 大数据
date: '2022-07-04 13:06:59+08:00'
tags:
- flink
thumbnailImage: //www.azheimage.top/markdown-img-paste-20181113164516536.png
title: flink编译
---

flink 导入 idea

<!--more-->

1. 克隆代码仓库，导入 idea
   git clone https://github.com/apache/flink.git
2. 修改 pom 文件

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <version>2.5</version>
<!-- 添加测试跳过 -->
    <configuration>
        <skipTests>true</skipTests>
    </configuration>
</plugin>
```

3. 编译

- 使用阿里云镜像
- 最简单的构建 Flink 的方法是执行如下命令：
  `mvn clean install -DskipTests`
  上面的 Maven 指令（mvn）首先删除（clean）所有存在的构建，然后构建一个新的 Flink 运行包（install）。

- 为了加速构建，可以执行如下命令，以跳过测试，QA 的插件和 JavaDocs 的生成：
  mvn clean package -T 4 -Dfast -Dmaven.compile.fork=true -DskipTests -Dscala-2.11
