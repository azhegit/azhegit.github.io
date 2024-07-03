---
categories:
- 技术
- 虚拟化&云计算
date: '2019-08-26 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180831191423561.png
title: 22-centos设置默认网关
---
默认网关设置.
<!--more-->

第一生效文件
```bash
[root@openstack-ceph-01 ~]# grep -i gate /etc/sysconfig/network-scripts/ifcfg-eth0
GATEWAY=10.57.26.1
```
第二生效文件
```bash
[root@openstack-ceph-01 ~]# grep -i gate /etc/sysconfig/network
GATEWAY=10.57.26.1
```
第三：命令行有限，且临时生效
```bash
[root@openstack-ceph-01 ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.57.26.1      0.0.0.0         UG    0      0        0 eth0
10.57.26.0      0.0.0.0         255.255.255.0   U     0      0        0 eth0
169.254.0.0     0.0.0.0         255.255.0.0     U     1002   0        0 eth0
169.254.0.0     0.0.0.0         255.255.0.0     U     1003   0        0 eth1
169.254.169.254 192.168.2.2     255.255.255.255 UGH   0      0        0 eth1
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.2.0     0.0.0.0         255.255.255.0   U     0      0        0 eth1

route add default gw 10.57.26.1 dev eth1

route del default gw 192.168.2.1 



route add 0.0.0.0 gw 10.57.26.1 netmask 0.0.0.0 dev eth1
```




