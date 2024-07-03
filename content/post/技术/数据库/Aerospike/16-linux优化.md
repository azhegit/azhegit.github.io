---
categories:
- 技术
- 数据库
date: '2022-06-14 20:53:06+08:00'
tags:
- Aerospike
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110144117219.png
title: 16-linux优化
---
Aerospike 数据库Linux优化
<!--more-->

## 服务
推荐值 service-threads 取决于aerospike.conf文件中命名空间的配置：

如果任何命名空间已 storage-engine 设置device并 data-in-memory设置为falseor ( data-in-memoryisfalse和 commit-to-device is true)，那么建议的值service-threads是每个 CPU/vCPU 至少 3 个，我们建议在这种配置中默认为每个 CPU/vCPU 5 个。
否则storage-engine，要么设置为，要么设置为 pmem并设置为，则推荐 和建议的值 至少为每个 CPU/vCPU 1，这也是此类配置的默认值。memorystorage-enginedevicedata-in-memorytruecommit-to-devicefalseservice-threads
在service-threads服务器启动时检查最佳实践。

## 内存
我们建议 memory-size 配置的累积总和不要超过机器上的总内存。

在memory-size服务器启动时检查最佳实践。

## Linux 最佳

### min_free_kbytes
内核参数控制有min_free_kbytes 多少内存应该保持空闲并且不被文件系统缓存占用。通常，内核占用几乎所有带有文件系统缓存的空闲 RAM，并根据需要由进程分配空闲内存。由于 Aerospike 在共享内存（1GB 块）中执行大量分配，默认内核值可能会导致意外的 OOM（内存不足终止）。建议将参数配置为至少 1.1GB，如果使用云供应商驱动程序，最好配置为 1.25GB - 因为这些也可以进行大量分配。这可确保 Linux 始终保持足够的可用内存，并为大量分配提供空闲空间。

检查参数值：

```bash
$ cat /proc/sys/vm/min_free_kbytes
```

如果该值较低，请根据正在运行的内核对其进行相应调整，并在重新启动后保持不变：
```bash
echo 3 > /proc/sys/vm/drop_caches
echo 1310720 > /proc/sys/vm/min_free_kbytes
echo "vm.min_free_kbytes=1310720" >> /etc/sysctl.conf
```
在min_free_kbytes服务器启动时检查最佳实践。

### swap关闭
```bash
$ echo 0 > /proc/sys/vm/swappiness
$ echo "vm.swappiness=0" >> /etc/sysctl.conf
```

### 关闭THP
临时关闭
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag

创建脚本
```bash
cat << 'EOF' >/etc/init.d/disable-transparent-hugepages
#!/bin/bash
### BEGIN INIT INFO
# Provides:          disable-transparent-hugepages
# Required-Start:    $local_fs
# Required-Stop:
# X-Start-Before:    aerospike
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Disable Linux transparent huge pages
# Description:       Disable Linux transparent huge pages, to improve
#                    database performance.
### END INIT INFO

case $1 in
  start)
    if [ -d /sys/kernel/mm/transparent_hugepage ]; then
      thp_path=/sys/kernel/mm/transparent_hugepage
    elif [ -d /sys/kernel/mm/redhat_transparent_hugepage ]; then
      thp_path=/sys/kernel/mm/redhat_transparent_hugepage
    else
      return 0
    fi

    echo 'never' > ${thp_path}/enabled
    echo 'never' > ${thp_path}/defrag

    re='^[0-1]+$'
    if [[ $(cat ${thp_path}/khugepaged/defrag) =~ $re ]]
    then
      echo 0  > ${thp_path}/khugepaged/defrag
    else
      echo 'no' > ${thp_path}/khugepaged/defrag
    fi

    unset re
    unset thp_path
    ;;
esac
EOF
```
赋予执行权
`chmod +x /etc/init.d/disable-transparent-hugepages`
创建系统执行脚本
```bash
cat << 'EOF' > /etc/systemd/system/disable-transparent-huge-pages.service
[Unit]
Description=Disable Transparent Huge Pages

[Service]
Type=oneshot
ExecStart=/bin/bash /etc/init.d/disable-transparent-hugepages start

[Install]
WantedBy=multi-user.target
EOF
```
启动脚本
```bash
systemctl daemon-reload
systemctl enable disable-transparent-huge-pages.service
```

### 禁用区域回收
echo 0 > /proc/sys/vm/zone_reclaim_mode
cat /proc/sys/vm/zone_reclaim_mode

### NVMe SSD优化 做分区
根据Core数以及磁盘块数做分区

### 文件打开句柄数
系统修改重启生效
```bash
vim /etc/security/limits.conf

root soft nofile 200000
root hard nofile 200000
* soft nofile 200000
* hard nofile 200000
```
临时生效
ulimit -SHn 200000










>参考 https://docs.aerospike.com/server/operations/install/linux/bestpractices
