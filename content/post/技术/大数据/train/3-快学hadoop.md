---
categories:
- 技术
- 大数据
date: '2019-07-15 19:56:53+08:00'
tags:
- train
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110143649189.png
title: 3-快学hadoop
---
为数据中台新人进行培训，培训内容hadoop
<!--more-->
## 1. Hadoop简介：
hadoop 是一个生态圈，由很多组件组成，是一个能够对大量数据进行分布式处理的软件框架。 Hadoop 以一种可靠、高效、可伸缩的方式进行数据处理。
![](https://www.azheimage.top/markdown-img-paste-20190715135558662.png)

其中最为核心的几个框架：
#### 1. 分布式存储系统HDFS
- 分布式存储系统
- 提供了高可靠性、高扩展性和高吞吐率的数据存储服务

##### 1. HDFS优点：
- 高容错性
- 适合批处理
- 适合大数据处理
- 可构建在廉价机器上
##### 2. HDFS的缺点：
- 低延迟数据访问
- 小文件存取
- 并发写入、文件随机修改

##### 3. HDFS架构：
- NameNode（NN元数据） 保存着 HDFS 的名字空间
  1. 接受客户端的读写服务
  2. 保存metadata信息包括
      1. 文件owership和permissions
      2. 文件包含那些快
      3. Block保存在datanode
  3. NameNode的metadata信息在启动后加载到内存
      1. Metadata存储到磁盘文件名为”fsImage”
      2. Block位置信息不会保存到fsImage
      3. Edits记录对metadata的操作日志
- SecondaryNameNode
  1. 不是NN的备份（但可以做备份），主要工作是帮助NN合并editslog,减少NN启动时间
  2. SNN执行合并时机
![](https://www.azheimage.top/markdown-img-paste-20190715135651582.png)
- DataNode(存放数据)
- Journal Node
  1. 两个NameNode为了数据同步，会通过一组称作JournalNodes的独立进程进行相互通信
  2. edits日志的改变必须写入大多数（一半以上）JNs，所以至少存在3个JournalNodes守护进程，这样系统能够容忍单个主机故障
![](https://www.azheimage.top/markdown-img-paste-20190715141519461.png)

##### 4.HDFS文件权限
1. 与Linux文件权限类似，rwx,权限x对于文件忽略，对文件夹表示允许访问
2. HDFS用户认证：
    1. Simple：只认证用户，不验证密码
    2. KerBeros:认证用户名跟密码：
      1.数据安全，但是速度比较慢
      2.每添加一台机器，需要重置用户密码，不利于维护

#### 2. 分布式计算框架MapReduce
i.分布式计算框架
ii.具有高容错性和高扩展性等优点
##### 1. MapReduceu优点
- 良好的扩展性
- 高容错性

##### 2. MapReduce的缺点
- 实时性差
- 处理流计算局限
- 不能处理DAG计算，性能底下

#### 3. 分布式调度框架YARN
YARN 是一个资源调度平台，负责为运算程序提供服务器运算资源，相当于一个分布式的操 作系统平台，而 MapReduce 等运算程序则相当于运行于操作系统之上的应用程序。

##### 1. YARN优点：
- 高扩展性
- 高可用性
- 高可靠性
- 向后兼容性
##### 3. YARN架构：
- ResourceManager（YARN 集群主控节点）
基于应用程序对集群资源的需求进行调度的 YARN 集群主控节点，负责 协调和管理整个集群（所有 NodeManager）的资源，响应用户提交的不同类型应用程序的 解析，调度，监控等工作。
它主要由两个组件构成：调度器（Scheduler）和应用程序管理器（ApplicationsManager）
  1. 处理客户端请求
  2. 启动或监控 MRAppMaster
  3. 监控 NodeManager
  4. 资源的分配与调度
- NodeManager
YARN 集群当中真正资源的提供者，是真正执行应用程序的容器的提供者
  1. 管理单个节点上的资源
  2. 处理来自 ResourceManager 的命令
  3. 处理来自 MRAppMaster 的命令
![](https://www.azheimage.top/markdown-img-paste-20190715145330688.png)

#### 4. hive
Hive是基于Hadoop的一个数据仓库工具，可以将结构化的数据文件映射为一张数据库表，并提供类SQL查询功能。

##### 1. 为什么使用Hive
###### 1. 直接使用hadoop所面临的问题
1. 人员学习成本太高
2. 项目周期要求太短
3. MapReduce实现复杂查询逻辑开发难度太大

###### 2. 操作接口采用类SQL语法，提供快速开发的能力。
1. 避免了去写MapReduce，减少开发人员的学习成本。
2. 扩展功能很方便。

##### 2. Hive的特点
- 可扩展
- 延展性
- 容错

##### 3. Hive组成
- 用户接口主要由三个：CLI、JDBC/ODBC和WebGUI。
  - CLI为shell命令行；
  - JDBC/ODBC是Hive的JAVA实现，与传统数据库JDBC类似；
  - WebGUI是通过浏览器访问Hive。
- 元数据存储：Hive 将元数据存储在数据库中。Hive 中的元数据包括表的名字，表的列和分区及其属性，表的属性（是否为外部表等），表的数据所在目录等。
- 解释器、编译器、优化器完成 HQL 查询语句从词法分析、语法分析、编译、优化以及查询计划的生成。生成的查询计划存储在 HDFS 中，并在随后有 MapReduce 调用执行。
![](https://www.azheimage.top/markdown-img-paste-20190715152440572.png)








