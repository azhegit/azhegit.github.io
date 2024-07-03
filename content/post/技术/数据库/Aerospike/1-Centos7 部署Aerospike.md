---
categories:
- 技术
- 数据库
date: '2021-09-22 11:20:55+08:00'
tags:
- Aerospike
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110144117219.png
title: 1-Centos7 部署Aerospike
---


### 准备工作
- 机器：newcdh-node5
- 操作系统版本查看:`uname -a`
<!--more-->
Linux newcdh-node5 3.10.0-1127.19.1.el7.x86_64 #1 SMP Tue Aug 25 17:23:54 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
- 操作系统详细版本查看：`cat /etc/redhat-release`
CentOS Linux release 7.8.2003 (Core)
- [官方下载最新版本5.6.0.13](https://download.aerospike.com/download/server/5.6.0.13/)
- 选择 Redhat7 rpm 包，服务器下载：
`wget https://download.aerospike.com/download/server/5.6.0.13/artifact/el7`
- 重命名安装包：
`mv el7 aerospike-server-community-5.6.0.13-el7.tgz`

### 安装
1. 要提取包的内容，请运行以下命令：
`tar zxvf aerospike-server-community-5.6.0.13-el7.tgz`
2. 安装服务器和工具包，进入解压目录执行
`cd aerospike-server-community-5.6.0.13-el7 ; ./asinstall`
![](https://www.azheimage.top/markdown-img-paste-20210922114049521.png)
3. 启动ASP
`systemctl start aerospike`
或
`service aerospike start`
或
`/etc/init.d/aerospike start`
4. 查看日志
`journalctl -u aerospike -a -o cat -f`
5. 查看状态
`systemctl status aerospike`
6. 支持命令：start、status、restart、stop
7. 日志截取
`journalctl -u aerospike -a -o cat --since "2016-03-17" --until "2016-03-18" | grep GMT > /tmp/aerospike.20160317.log`

### 目录

asp安装在/opt/aerospike
#### 工具目录结构
- lib - 管理工具使用的简单 Aerospike python 客户端。
- bin- [工具] 二进制文件，例如 aql、asadm、asbackup/asrestore等。
- doc - 工具文档和许可证。
- examples-aql示例文件，以及将 C 与 Lua 结合使用的示例。
该examples目录已在 Aerospike Tools 3.15.0.3 中删除。

#### 运行时目录
- data
这个目录是由安装包创建的，用于放置 Aerospike 数据文件——这些文件持久存在于内存中。在标准操作配置中，不推荐使用文件系统，而是将数据存储在原始设备上。但是，对于开发人员安装，文件系统通常是首选。
- smd
System MetaData 目录包含以分布式、持久方式保存的数据目录。为了便于阅读，这些文件的格式为 JSON - 不建议手动编辑这些文件。有关集群索引、册的用户定义函数 (UDF) 和其他集群范围的信息的信息存储在此处。
  - 驱逐.smd
这个模块是在4.5.1.5中添加的。它存储每个命名空间的驱逐实时时钟。
  - 名册.smd
此模块仅适用于企业 strong-consistency 用户，并在4.0.0.1中添加 。它存储每个强一致性命名空间的名册配置。
  - 安全.smd
本模块仅适用于企业用户。存储 用户权限 定义。
  - sindex.smd
该模块存储二级索引 定义。
  - truncate.smd
该模块存储每个集合或命名空间 LUT（上次更新时间）截止时间。
  - UDF文件
该模块存储用户定义函数 (UDF) 定义，实际 UDF 存储在opt/aerospike/usr目录中
- sys
此目录包含 UDF（以及可能的其他静态内容），它们是服务器包的一部分。它们由包管理器维护，并使用已安装的服务器版本进行测试。
不要修改这个目录；它不会在重新启动时重新创建。
- usr
该目录包含管理员通过集群管理工具（例如aql）注册的 UDF（以及可能的其他动态内容） 。
不建议在生产中直接修改这些文件。但是在开发者环境中，为了加快开发周期，可以禁用Lua缓存 ，usr/udf/lua直接修改文件。

#### 单机版，内存+磁盘方式配置
```yaml
service {
        paxos-single-replica-limit 1 # Number of nodes where the replica count is automatically reduced to 1.
        proto-fd-max 15000
}

logging {
        console {
                context any info
        }
}

network {
        service {
                address any
                port 3000
        }

        heartbeat {
                mode multicast
                multicast-group 239.1.99.222
                port 9918

                # To use unicast-mesh heartbeats, remove the 3 lines above, and see
                # aerospike_mesh.conf for alternative.

                interval 150
                timeout 10
        }

        fabric {
                port 3001
                channel-rw-recv-pools 8
        }

        info {
                port 3003
        }
}


namespace test {
        replication-factor 2
        memory-size 20G
        default-ttl 7D
        allow-ttl-without-nsup true
        storage-engine device {         # Configure the storage-engine to use
                                        # persistence. Maximum size is 2 TiB
                 file /data/disk01/aerospike/aerospike.dat  # Location of data file on server.
                 file /data/disk02/aerospike/aerospike.dat  # Location of data file on server.
                 file /data/disk03/aerospike/aerospike.dat  # Location of data file on server.
                 file /data/disk04/aerospike/aerospike.dat  # Location of data file on server.
                 file /data/disk05/aerospike/aerospike.dat  # Location of data file on server.
                 file /data/disk06/aerospike/aerospike.dat  # Location of data file on server.
                 file /data/disk07/aerospike/aerospike.dat  # Location of data file on server.
               # file /opt/aerospike/<another> # (optional) Location of data file on server.
                 filesize 20G                # Max size of each file in GiB.
                 data-in-memory false             # Indicates that all data should also be
                                                 # in memory.
        }

}

namespace bar {
        replication-factor 2
        memory-size 4G

        storage-engine memory

        # To use file storage backing, comment out the line above and use the
        # following lines instead.
#       storage-engine device {
#               file /opt/aerospike/data/bar.dat
#               filesize 16G
#               data-in-memory true # Store data in memory in addition to file.
#       }
}
```

## hot key 问题解决方案
在namespace 里配置 transaction-pending-limit 0  
asinfo -v "set-config:context=namespace;id=large;transaction-pending-limit=0"

## CentOS部署AMC
wget https://download.aerospike.com/artifacts/aerospike-amc-community/4.0.27/aerospike-amc-community-4.0.27-linux.tar.gz
tar zxvf aerospike-amc-community-4.0.27-linux.tar.gz -C /
启动
/etc/init.d/amc start

## 集群配置
```yaml
# Aerospike database configuration file for use with systemd.

service {
        paxos-single-replica-limit 1 # Number of nodes where the replica count is automatically reduced to 1.
        proto-fd-max 15000
}

logging {
        console {
                context any info
        }
}

network {
        service {
                address any
                port 3000
                # add current node address here
                access-address 172.16.11.113
        }

        heartbeat {
                mode mesh
                # add current node address here
                #address 172.16.11.113
                port 3002
                # add all cluster node address here
                mesh-seed-address-port 172.16.11.110 3002
                mesh-seed-address-port 172.16.11.111 3002
                mesh-seed-address-port 172.16.11.113 3002

                interval 150
                timeout 10
        }

        fabric {
                port 3001
                channel-rw-recv-pools 8
        }

        info {
                port 3003
        }
}


namespace test {
        replication-factor 2
        memory-size 20G
        default-ttl 7D
        allow-ttl-without-nsup true
        storage-engine device {         # Configure the storage-engine to use
                                        # persistence. Maximum size is 2 TiB
                 file /data/disk01/aerospike/aerospike.dat  # Location of data file on server.
                 file /data/disk02/aerospike/aerospike.dat  # Location of data file on server.
                 file /data/disk03/aerospike/aerospike.dat  # Location of data file on server.
                 file /data/disk04/aerospike/aerospike.dat  # Location of data file on server.
                 file /data/disk05/aerospike/aerospike.dat  # Location of data file on server.
                 file /data/disk06/aerospike/aerospike.dat  # Location of data file on server.
                 file /data/disk07/aerospike/aerospike.dat  # Location of data file on server.
               # file /opt/aerospike/<another> # (optional) Location of data file on server.
                 filesize 20G                # Max size of each file in GiB.
                 data-in-memory false             # Indicates that all data should also be
                                                 # in memory.
        }

}

namespace bar {
        replication-factor 2
        memory-size 4G

        storage-engine memory

        # To use file storage backing, comment out the line above and use the
        # following lines instead.
#       storage-engine device {
#               file /opt/aerospike/data/bar.dat
#               filesize 16G
#               data-in-memory true # Store data in memory in addition to file.
#       }
}
```


