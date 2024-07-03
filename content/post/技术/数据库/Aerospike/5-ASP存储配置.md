---
categories:
- 技术
- 数据库
date: '2021-10-12 10:06:12+08:00'
tags:
- Aerospike
thumbnailImage: //www.azheimage.top/markdown-img-paste-20181113164859849.png
title: 5-ASP存储配置
---
#### SSD 存储引擎的秘诀
<!--more-->
```bash
namespace test {
        replication-factor 2
        memory-size 4G

#       storage-engine memory

        storage-engine device {     # Configure the storage-engine to use persistence
                device /dev/vdc1    # raw device. Maximum size is 2 TiB
                # device /dev/<device>  # (optional) another raw device.
                write-block-size 128K   # adjust block size to make it efficient for SSDs.
        }
}
```

这个配置SSD会有可能导致SSD盘出现64Z，磁盘占用100%

#### 具有内存数据的 HDD 存储引擎的配方
数据放在内存，同时持久化到磁盘
```bash
namespace test {
        replication-factor 2
        memory-size 50G
        default-ttl 7D
        allow-ttl-without-nsup true
        storage-engine device {         # Configure the storage-engine to use
                                        # persistence. Maximum size is 2 TiB
                 file /data/disk01/aerospike/aerospike.dat  # Location of data file on server.
               # file /opt/aerospike/<another> # (optional) Location of data file on server.
                 filesize 100G                # Max size of each file in GiB.
                 data-in-memory true             # Indicates that all data should also be
                                                 # in memory.
        }

}
```
#### 没有持久性的内存中数据的配方(默认配置，生产不建议)
没有持久性的命名空间的最小配置是将storage-engine设置 为memory. 如果您的命名空间需要为内存中的主索引和数据分配超过默认的 4 GiB内存大小，则还需要相应地进行调整memory-size。
```bash
namespace <namespace-name> {
    memory-size <SIZE>G   # Maximum memory allocation for data and primary and
                          # secondary indexes.
    storage-engine memory # Configure the storage-engine to not use persistence.
}
```


#### 使用索引引擎中的数据的 HDD 存储引擎的配方(未验证配置)
适合做指标，单bin处理。
数据是单 bin并且适合 8 个字节，并且您需要内存中命名空间的性能，但又不想失去 Aerospike 企业版中提供的快速重启功能，那么 data-in-index 就是它。
```bash
namespace <namespace-name> {
    memory-size <N>G                # Maximum memory allocation for data and
                                    # primary and secondary indexes.
    single-bin true                 # Required true by data-in-index.
    data-in-index true              # Enables in index integer store.
    storage-engine device {         # Configure the storage-engine to use
                                    # persistence.
    file /opt/aerospike/<filename>  # Location of data file on server.
    # file /opt/aerospike/<another> # (optimal) Location of data file on server.
    # device /dev/<device>          # Optional alternative to using files.

    filesize <SIZE>G               # Max size of each file in GiB. Maximum size is 2TiB
    data-in-memory true            # Required true by data-in-index.
    }
}
```

#### 持久内存存储引擎的秘诀(未验证配置)
将内存数据持久化，仅限于企业版
```bash
namespace test {
        replication-factor 2
        memory-size 50G
#       default-ttl 7D
#       allow-ttl-without-nsup true
        storage-engine pmem {         # Configure the storage-engine to use
                                        # persistence. Maximum size is 2 TiB
                 file /data/disk01/aerospike/aerospike.dat  # Location of data file on server.
               # file /opt/aerospike/<another> # (optional) Location of data file on server.
                 filesize 100G                # Max size of each file in GiB.
#                 data-in-memory true             # Indicates that all data should also be
                                                 # in memory.
        }

}
```

从数据留存的角度看，就是这3种，纯内存；内存+文件；索引内存+SSD数据

纯内存一般不用，毕竟生产环境，万一宕掉数据就没了，也挺危险的

数据在内存+文件的方式拆开又有三种：
1. pmem-file，内存并持久化，数据在内存，持久化到文件中，只限于企业版
2. device-file，内存并持久化，数据在内存，持久化到文件中
3. device-file，single-bin方式，可以提供快速重启



10亿级别key存储，主索引需要60G，单个二级索引需要11.5G左右
