---
categories:
- 技术
- 数据库
date: '2022-03-04 10:11:41+08:00'
tags:
- Aerospike
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716212442829.png
title: 12-Aerospike机器新增
---
## linux 优化

### 1.min_free_kbytes优化
min_free_kbytes 该参数即强制Linux 系统最低保留多少空闲内存（Kbytes），如果系统可用内存低于该值，默认会启用oom killer 或者强制重启，当耗尽内存直至系统最低保存内存时会有两种现象，根据内核参数vm.panic_on_\oom 设置值的不同而有不同的行为。
<!--more-->
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
$ dd if=/dev/zero of=/dev/vdb bs=131072 &
dd: error writing ‘/dev/vdb’: No space left on device
14647297+0 records in
14647296+0 records out
1919850381312 bytes (1.9 TB) copied, 1733.02 s, 1.1 GB/s


# 监控dd,23709替换成pid
while [ 1 ]
do kill -USR1 15241
sleep 60
done
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


## As 安装
1. 拷贝配置文件
```bash
scp aerospike-prometheus-exporter-1.5.0-x86_64.rpm aerospike-server-community-5.7.0.7-el7.tgz root@prod-jstdata-cache-5:`pwd`
```
2. 解压文件,并安装
```bash
tar zxvf aerospike-server-community-5.7.0.7-el7.tgz 
cd aerospike-server-community-5.7.0.7-el7/
./asinstall
```
3. 修改配置文件
```yaml
# 增加配置
mesh-seed-address-port prod-jstdata-cache-5 3002
```
创建日志目录：
mkdir /var/log/aerospike

启动
service aerospike start
3. 查看日志
journalctl -u aerospike -a -o cat -f

service aerospike stop

## 监控安装

安装
rpm -ivh aerospike-prometheus-exporter-1.5.0-x86_64.rpm
启动aerospike-prometheus-exporter
systemctl start aerospike-prometheus-exporter.service
验证是否启动端口
telnet localhost 9145
配置Prometheus


## 日志切分
vim /etc/logrotate.d/aerospike
```config
/var/log/aerospike/aerospike.log {
    daily
    rotate 90
    dateext
    compress
    olddir /var/log/aerospike/
    sharedscripts
    postrotate
        /bin/kill -HUP `pidof asd`
    endscript
}
```
测试输出：logrotate -f -v /etc/logrotate.d/aerospike







## 删除机器
要删除的机器先停止 service aerospike stop
然后在存活节点执行
asadm+>asinfo -v 'tip-clear:host-port-list=prod-jstdata-cache-4:3002'

修改配置文件，删除之前节点信息，以防止重启的时候，日志一直报连接不上，比如
Error while connecting socket to 172.16.20.61:3002


