---
categories:
- 技术
- 数据库
date: '2021-10-26 16:53:06+08:00'
tags:
- Aerospike
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110153448285.png
title: 8-ACT认证
---
## ACT 测试过程

### 安装
安装 iostat（Centos 安装示例）。需要安装包含 iostat 的 sysstat 包。
<!--more-->
yum install sysstat  

[ACT git地址](https://github.com/aerospike/act)

```shell
wget https://github.com/aerospike/act/archive/refs/heads/master.zip
unzip master.zip
cd act-master/
yum install make gcc
make
```


dd if=/dev/zero of=/dev/vdb bs=128K &
dd if=/dev/zero of=/dev/vdc bs=128K &
dd if=/dev/zero of=/dev/vdd bs=128K &
dd if=/dev/zero of=/dev/vde bs=128K &

while [ 1 ]
do kill -USR1 3816
sleep 60
done

1919850381312 bytes (1.9 TB) copied, 1700.97 s, 1.1 GB/s




### 测试
1. 使用 act_prep 准备驱动器 - 仅限第一次，预写数据
此可执行文件通过在磁盘的每个扇区上写入零，然后用随机数据填充它（加盐）来为 ACT 准备设备。这模拟了正常的生产状态。
./target/bin/act_prep /dev/vdb &
./target/bin/act_prep /dev/vdc &
./target/bin/act_prep /dev/vdd &
./target/bin/act_prep /dev/vde &



2. 修改配置文件
cp config/act_storage.conf
```yaml
cp config/act_storage.conf actconfig.conf
vim actconfig.conf

device-names: /dev/vdb,/dev/vdc,/dev/vdd,/dev/vde
#read-reqs-per-sec: 2000 
# 30x
read-reqs-per-sec: 240000
#write-reqs-per-sec: 1000
# 30x
write-reqs-per-sec: 120000
# replication-factor: 1
replication-factor: 2
#update-pct: 0
update-pct: 40
```
3. 启动测试
./target/bin/act_storage actconfig.conf > output30x.txt &
4. 分析 ACT 输出
运行 /analysis/act_latency.py 以处理 ACT 日志文件并制表数据。请注意，您可以在测试尚未完成时运行脚本，您将看到部分结果。

例如：
./analysis/act_latency.py -l output15x.txt
```bash
act_latency.py -l output128k15x.txt
output128k15x.txt is ACT version 6.2

ACT-STORAGE CONFIGURATION
device-names: /dev/vdb /dev/vdc /dev/vdd /dev/vde
num-devices: 4
service-threads: 160
test-duration-sec: 86400
report-interval-sec: 1
microsecond-histograms: no
read-reqs-per-sec: 120000
write-reqs-per-sec: 60000
record-bytes: 1536
record-bytes-range-max: 0
large-block-op-kbytes: 128
replication-factor: 1
update-pct: 0
defrag-lwm-pct: 50
compress-pct: 100
disable-odsync: no
commit-to-device: no
commit-min-bytes: 0
tomb-raider: no
tomb-raider-sleep-usec: 0
max-lag-sec: 10
scheduler-mode: noop

DERIVED CONFIGURATION
record-stored-bytes: 1536 ... 1536
internal-read-reqs-per-sec: 120000
internal-write-reqs-per-sec: 0
large-block-reads-per-sec: 1411.76
large-block-writes-per-sec: 1411.76

HISTOGRAM NAMES
reads
/dev/vdb-reads
/dev/vdc-reads
/dev/vdd-reads
/dev/vde-reads
large-block-reads
large-block-writes

        reads                                           
        %>(ms)                                          
slice        1      2      4      8     16     32     64
-----   ------ ------ ------ ------ ------ ------ ------
    1    40.43  21.31   2.29   0.01   0.01   0.00   0.00
    2    30.83  13.74   0.94   0.01   0.01   0.00   0.00
    3    33.02  15.17   1.11   0.01   0.01   0.00   0.00
    4    32.47  14.83   1.07   0.01   0.01   0.00   0.00
    5    32.51  14.83   1.06   0.01   0.01   0.00   0.00
    6    32.71  14.87   1.04   0.01   0.01   0.00   0.00
    7    32.63  14.85   1.05   0.01   0.01   0.00   0.00
    8    32.68  14.87   1.04   0.01   0.01   0.00   0.00
    9    32.73  14.91   1.05   0.01   0.01   0.00   0.00
   10    32.79  14.95   1.05   0.01   0.01   0.00   0.00
   11    32.77  14.93   1.05   0.01   0.01   0.00   0.00
   12    32.77  14.92   1.05   0.01   0.01   0.00   0.00
   13    32.75  14.92   1.05   0.01   0.01   0.00   0.00
   14    32.75  14.92   1.05   0.01   0.01   0.00   0.00
   15    32.81  14.96   1.05   0.01   0.01   0.00   0.00
   16    32.82  14.93   1.05   0.01   0.01   0.00   0.00
   17    32.84  14.97   1.05   0.01   0.01   0.00   0.00
   18    32.80  14.93   1.05   0.01   0.01   0.00   0.00
   19    32.93  14.99   1.06   0.01   0.01   0.00   0.00
   20    32.83  14.96   1.06   0.01   0.01   0.00   0.00
   21    32.79  14.94   1.05   0.01   0.01   0.00   0.00
   22    32.82  14.95   1.05   0.01   0.01   0.00   0.00
   23    32.79  14.89   1.04   0.01   0.01   0.00   0.00
   24    32.79  14.95   1.05   0.01   0.01   0.00   0.00
-----   ------ ------ ------ ------ ------ ------ ------
  avg    33.00  15.15   1.10   0.01   0.01   0.00   0.00
  max    40.43  21.31   2.29   0.01   0.01   0.00   0.00
```



通过`iostate -x 3`查看磁盘负载
```bash
Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
vda               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00
vdb               0.00     0.00    0.00 9425.33     0.00 1206442.67   256.00     7.86    0.84    0.00    0.84   0.11 100.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           0.08    0.00    1.09   13.70    0.00   85.12
```
