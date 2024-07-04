---
categories:
- 技术
- 数据库
date: '2018-11-04 13:25:09+08:00'
tags:
- HugeGraph
thumbnailImage: //www.azheimage.top/markdown-img-paste-2018111316510833.png
title: FAQ
---

HugeGraph 使用过程中遇到的问题及解决方案

<!--more-->

#### 1.  在服务器上安装启动之后，本机访问不了 server（8080 端口），以及 studio（8088 端口）

    ① server端口访问修改rest-server.properties：

```properties
    #默认
    restserver.url=http://127.0.0.1:8080
    #修改成本机ip
    restserver.url=http://服务器ip:8080
```

    ② server端口访问修改rest-server.properties：

```properties
    #默认
    studio.server.host=localhost
    graph.server.host=localhost
    ###把默认配置修改成如下###
    studio.server.host=服务器ip
    graph.server.host=服务器ip
```

#### 2. vertex 定义联合主键，使用 hugegraph-loader 导入数据，报错

    已经提交issue，owner会尽快修复

#### 3. JavaAPI 定义顶点 label，使用 useCustomizeNumberId(),插入顶点的时候报错

    给HugeGraph开源项目提交issue，并且贡献修复bug的代码

#### 4. hugegraph-spark 目前没有开源

    后续大概率会开源出来

#### 5. hugegraph-loader 导入数据非常慢

    ① Cassandra优化：

```properties
    # Log WARN on any multiple-partition batch size exceeding this value. 5kb per batch by default.
    # Caution should be taken on increasing the size of this threshold as it can lead to node instability.
    #batch_size_warn_threshold_in_kb: 5
    batch_size_warn_threshold_in_kb: 1024

    # Fail any multiple-partition batch exceeding this value. 50kb (10x warn threshold) by default.
    #batch_size_fail_threshold_in_kb: 50
    batch_size_fail_threshold_in_kb: 1024
```

    ② HugeGraph调优，修改rest-server.properties,增加以下参数：

```properties
    #提高写的并行度
    batch.max_write_ratio=80
    #batch.max_write_threads=16
    #提高每批次处理条数
    batch.max_edges_per_batch=20000
    batch.max_vertices_per_batch=20000
```

    ③ HugeGraph调优，修改hugegraph.properties,增加以下参数：

```properties
    #事务中顶点（未提交）的最大大小（项）
    vertex.tx_capacity=50000
    edge.tx_capacity=80000
```

#### 6. 启动服务成功了，但是操作图时有类似于"无法连接到后端或连接未打开"的提示

    第一次启动服务前，需要先使用init-store初始化后端，后续版本会将提示得更清晰直接。

#### 7. 官方 rocksDB 性能测试能达到 8M/s(数据占内存大小),实际测试中只能达到 4.5M/s

    owner建议边，顶点数据存放不同的磁盘，以提高读写效率，性能可以提升一倍
    RocksDB配置：
    rocksdb.data_path=disk1/path
    rocksdb.wal_path=disk1/path
    rocksdb.data_disks=[graph/edge_out:disk2/path, graph/edge_in:disk3/path]
