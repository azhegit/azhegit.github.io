---
categories:
- 技术
- 数据库
date: '2021-10-25 13:45:53+08:00'
tags:
- Aerospike
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180831191423561.png
title: 7-Aerospike集群安装
---

## 机器环境
<!--more-->
3台阿里云机器：
机型|实例规格|vCPU|内存|本地存储|处理器|内网宽带|内网收发包
-|-|-|-|-|-|-|-
本地SSD型 i2|ecs.i2gne.4xlarge|16 vCPU|64 GiB|1 * 1788 GiB|2.5 GHz/-|5 Gbps|150 万 PPS

## 存储规划
### 可用内存
机器存储,除去系统需要，能用62G，3台2副本策略，3*62/2=93G

### 混合存储规划
10亿级别key存储，
内存分配(50G+1.2T)*3
namespace：large

### 纯内存规划
单台机器8G*3
namespace：small


## linux 优化

### 1.min_free_kbytes优化
min_free_kbytes 该参数即强制Linux 系统最低保留多少空闲内存（Kbytes），如果系统可用内存低于该值，默认会启用oom killer 或者强制重启，当耗尽内存直至系统最低保存内存时会有两种现象，根据内核参数vm.panic_on_\oom 设置值的不同而有不同的行为。

vm.panic_on_oom=0 系统会提示oom ，并启动oom-killer杀掉占用最高内存的进程 vm.panic_on_oom =1. 系统关闭oom,不会启动oom-killer,而是会自动重启，AS建议设定为1.1～1.25GB。

```bash
echo 3 > /proc/sys/vm/drop_caches
echo 1048576 > /proc/sys/vm/min_free_kbytes
echo "vm.min_free_kbytes=1048576" >> /etc/sysctl.conf
# 查看
sysctl -a | grep min_free
```
### 关闭swap
```bash
echo 0 > /proc/sys/vm/swappiness
echo "vm.swappiness=0" >> /etc/sysctl.conf
# 查看
sysctl -a | grep swappiness
```

### 2. 关闭THP
transparent huge pages 对于AS这种大量并发的小内存分配来说，这个默认启用的THP会导致系统较快的耗尽内存或者产生类似内存泄漏相关的症状。所以建议关闭。
```bash
# 临时生效
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag
# 重启生效
cat <<EOF > /etc/systemd/system/disable-transparent-huge-pages.service
[Unit]
Description=Disable Transparent Huge Pages
[Service]
Type=oneshot
ExecStart=/bin/bash /etc/init.d/disable-transparent-hugepages start
[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable disable-transparent-huge-pages.service

```

### 3. Max Open File limits
```bash
# 查看打开文件数量限制,默认一般是65535
ulimit -n
# 临时修改
ulimit -n 1000000
# 永久修改
vim /etc/security/limits.conf
# 追加
root soft nofile 1000000
root hard nofile 1000000
* soft nofile 1000000
* hard nofile 1000000
```

### 4. java 安装：
wget http://172.16.10.98:8086/jst/install/java.sh && chmod +x java.sh && ./java.sh

### 5. SSD 初始化

[SSD安装步骤](https://docs.aerospike.com/docs/operations/plan/ssd/ssd_setup.html)
1. 执行dd命令
磁盘完全 dd 后， dd 将以消息No space left on device或out of space error. 这表明 dd 已成功完成对整个磁盘的写入，并且 dd 已没有剩余空间可以继续。
```bash
$ dd if=/dev/zero of=/dev/vdb bs=131072
dd: error writing ‘/dev/vdb’: No space left on device
14647297+0 records in
14647296+0 records out
1919850381312 bytes (1.9 TB) copied, 1733.02 s, 1.1 GB/s
```
2. 磁盘分配（如果单盘，不需要切分，忽略此步骤）
```shell
$ fdisk /dev/vdb
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table
Building a new DOS disklabel with disk identifier 0x0b06f23b.

Command (m for help): g
Building a new GPT disklabel (GUID: C1926E81-69DA-40A9-917F-73F7A31D98B8)


Command (m for help): o
Building a new DOS disklabel with disk identifier 0x438e3cec.

Command (m for help): n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p):
Using default response p
Partition number (1-4, default 1):
First sector (2048-872415231, default 2048):
Using default value 2048
Last sector, +sectors or +size{K,M,G} (2048-872415231, default 872415231):
Using default value 872415231
Partition 1 of type Linux and of size 416 GiB is set

Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.
```


## AS安装部署
因为是centos 7的系统，所以安装el7,如果是el6的系统需要修改下载链接。

### 1. 部署安装
```bash
wget -O aerospike-server-community.tgz 'http://aerospike.com/download/server/latest/artifact/el7'
tar -zxvf aerospike-server-community.tgz
cd aerospike-server-community-5.7.0.7-el7
./asinstall

```

### 2. 修改配置
vim /etc/aerospike/aerospike.conf
```bash

storage-engine device {
        device /dev/vdb
        # device /dev/<device>
        write-block-size 128K
}
```
![](https://www.azheimage.top/markdown-img-paste-20220316151559271.png)
### 3. 启动
service aerospike start

### 4. 测试
```sql
$ aql
Seed:         127.0.0.1
User:         None
Config File:  /etc/aerospike/astools.conf /root/.aerospike/astools.conf
Aerospike Query Client
Version 6.1.0
C Client Version 5.2.3
Copyright 2012-2021 Aerospike. All rights reserved.
aql> INSERT INTO test.testset (PK, a, b) VALUES ('xyz', 'abc', 123)
OK, 1 record affected.

aql> select * from  test.testset
+-------+-----+
| a     | b   |
+-------+-----+
| "abc" | 123 |
+-------+-----+
1 row in set (0.041 secs)

OK
```

## CentOS部署AMC
```bash
wget https://download.aerospike.com/artifacts/aerospike-amc-community/4.0.27/aerospike-amc-community-4.0.27-linux.tar.gz
tar zxvf aerospike-amc-community-4.0.27-linux.tar.gz -C /
启动
/etc/init.d/amc start
```



