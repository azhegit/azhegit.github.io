---
categories:
- 技术
- 数据库
date: '2021-10-11 19:16:33+08:00'
tags:
- Aerospike
thumbnailImage: //www.azheimage.top/markdown-img-paste-20181113164516536.png
title: 4-ssd故障
---
[toc]
aerospike 选用SSD，格式故障

### 第一种方式，直接配置

<!--more-->
[配置参考地址](https://docs.aerospike.com/docs/operations/configure/namespace/storage/#recipe-for-an-ssd-storage-engine)

![](https://www.azheimage.top/markdown-img-paste-20211011192002841.png)
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

配置挂载完，启动as会把SSD挂载出现64Z问题

![](https://www.azheimage.top/markdown-img-paste-20211011192145581.png)

### 第二种方式，先格式化
[配置参考地址](https://docs.aerospike.com/docs/operations/plan/ssd/ssd_setup.html)
参考步骤：
![](https://www.azheimage.top/markdown-img-paste-2021101413443185.png)
保存完，也是出现64Z的情况

### 磁盘信息
机器信息
![](https://www.azheimage.top/markdown-img-paste-20211014135021325.png)
磁盘信息
![](https://www.azheimage.top/markdown-img-paste-20211014135122222.png)

#### 磁盘恢复处理方法
先卸载再挂载
`umount /data/disk02`
如果卸载不掉，通过lsof查看磁盘占用程序，先关掉
`lsof /dev/vdc1`
重新挂载，如果报错就需要格式化，在挂载
sudo mkfs -t ext4 /dev/vdc1
mount -t ext4 /dev/vdc1 /data/disk02

如果找不到vdc1，那就用fdisk重建分区
`fdisk /dev/vdc`一直回车就可以，然后用wp保存
然后挂载
如果还挂载不上，有可能挂载指定了uuid，重建之后uuid不一致

查看当前uuid
`blkid /dev/vdc1`
查看原来的uuid
`cat /etc/fstab`
将原来的uuid指定给新的分区
`tune2fs -U 7fda7ebd-67e7-4c77-b60a-18ca0275eca9 /dev/vdc1`
再次挂载可以




按照Aerospike官网安装文档，选用索引放内存，数据存SSD裸盘，部署启动之后，对应的SSD磁盘大小变成64Z，占用100%
