---
categories:
- 技术
- 虚拟化&云计算
date: '2019-08-09 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //d1u9biwaxjngwg.cloudfront.net/welcome-to-tranquilpeak/city-750.jpg
title: 16-openstack停电故障修复
---
集群物理机停电重启，部分虚拟机启动失败
<!--more-->

## 修复OpenStack集群重启，导致虚拟机启动失败
### 问题描述
宿主机停电，OpenStack集群down掉。集群重启，OpenStack集群自动恢复，但是虚拟机重启失败，启动日志如下：
```
[[32m  OK  [0m] Found device /dev/disk/by-uuid/f41e390f-835b-4223-a9bb-9b45984ddf8d.
[[32m  OK  [0m] Started dracut initqueue hook.
[[32m  OK  [0m] Reached target Remote File Systems (Pre).
[[32m  OK  [0m] Reached target Remote File Systems.
         Starting File System Check on /dev/...f-835b-4223-a9bb-9b45984ddf8d...
[[32m  OK  [0m] Started File System Check on /dev/d...90f-835b-4223-a9bb-9b45984ddf8d.
         Mounting /sysroot...
[    3.108998] SGI XFS with ACLs, security attributes, no debug enabled
[    3.116360] XFS (vda1): Mounting V5 Filesystem
[    3.138137] blk_update_request: I/O error, dev vda, sector 8403339
[    3.140523] blk_update_request: I/O error, dev vda, sector 8404363
[    3.142606] blk_update_request: I/O error, dev vda, sector 8405371
[    3.157300] blk_update_request: I/O error, dev vda, sector 8406395
[    3.159398] blk_update_request: I/O error, dev vda, sector 8407419
[    3.161713] XFS (vda1): xfs_do_force_shutdown(0x1) called from line 1266 of file fs/xfs/xfs_buf.c.  Return address = 0xffffffffc04608cc
[    3.165808] XFS (vda1): I/O Error Detected. Shutting down filesystem
[    3.167948] XFS (vda1): Please umount the filesystem and rectify the problem(s)
[    3.170751] XFS (vda1): metadata I/O error: block 0x80318b ("xlog_bwrite") error 5 numblks 8192
[    3.174063] XFS (vda1): failed to locate log tail
[    3.175778] XFS (vda1): log mount/recovery failed: error -5
[    3.177831] XFS (vda1): log mount failed
[    3.185537] blk_update_request: I/O error, dev vda, sector 0
[[1;31mFAILED[0m] Failed to mount /sysroot.
See 'systemctl status sysroot.mount' for details.
[[1;33mDEPEND[0m] Dependency failed for Initrd Root File System.
[[1;33mDEPEND[0m] Dependency failed for Reload Configuration from the Real Root.
[[32m  OK  [0m] Reached target Initrd File Systems.
[[32m  OK  [0m] Stopped target Basic System.
[[32m  OK  [0m] Stopped target System Initialization.
         Starting Setup Virtual Console...
[[32m  OK  [0m] Stopped dracut initqueue hook.
[[32m  OK  [0m] Stopped dracut pre-trigger hook.
[[32m  OK  [0m] Stopped dracut pre-udev hook.
[[32m  OK  [0m] Stopped dracut cmdline hook.
[[32m  OK  [0m] Started Setup Virtual Console.
[] Started Emergency Shell.
[[32m  OK  [0m] Reached target Emergency Mode.
```
是虚拟机的系统盘损坏导致系统启动不了

### 解决办法
此集群存储用的是ceph，把系统盘从ceph集群映射到宿主机，在宿主机通过磁盘修复，把系统盘修复好，虚拟机就可以恢复。

### 解决步骤
1. 宿主机下载ceph客户端
yum install ceph-common
2. 查看卷列表
rbd list -p volumes
```
volume-02242532-24da-40e8-b9a0-239792791883
volume-4119a5a0-b2f0-489d-8e24-d76a6e8796aa
volume-6fbd8049-1506-4acb-b41e-6139720c2bb8
volume-b354bdc6-3ea3-4d68-8d73-671ae7ac2bf0
volume-c71fce73-5840-4eaf-afaf-d043bdb77272
volume-d51d7ed9-adad-4ed5-aabb-10318b57bdcf
volume-ee585a9f-87bf-4757-af20-131319b78eee
volume-ff53a61f-377d-4cfc-bd14-e1864b5cc78c
```
3. 在页面控制台找到要修复OpenStack实例的卷id，ff53a61f-377d-4cfc-bd14-e1864b5cc78c
4. 把要修复的卷映射到宿主机
rbd map volume-02242532-24da-40e8-b9a0-239792791883 -p volumes
rbd map volume-4119a5a0-b2f0-489d-8e24-d76a6e8796aa -p volumes
rbd map volume-6fbd8049-1506-4acb-b41e-6139720c2bb8 -p volumes
rbd map volume-b354bdc6-3ea3-4d68-8d73-671ae7ac2bf0 -p volumes
rbd map volume-c71fce73-5840-4eaf-afaf-d043bdb77272 -p volumes
rbd map volume-d51d7ed9-adad-4ed5-aabb-10318b57bdcf -p volumes
rbd map volume-ee585a9f-87bf-4757-af20-131319b78eee -p volumes
rbd map volume-ff53a61f-377d-4cfc-bd14-e1864b5cc78c -p volumes


5. 映射失败
```
rbd: sysfs write failed
RBD image feature set mismatch. You can disable features unsupported by the kernel with "rbd feature disable".
In some cases useful info is found in syslog - try "dmesg | tail" or so.
rbd: map failed: (6) No such device or address
```
6. 查看卷feature
rbd info volume-ff53a61f-377d-4cfc-bd14-e1864b5cc78c -p volumes
```shell
rbd image 'volume-ff53a61f-377d-4cfc-bd14-e1864b5cc78c':
	size 51200 MB in 12800 objects
	order 22 (4096 kB objects)
	block_name_prefix: rbd_data.17a8c6b8b4567
	format: 2
	features: layering, exclusive-lock, object-map, fast-diff, deep-flatten
	flags:
```
7. 关闭卷的高级feature
rbd feature disable exclusive-lock object-map fast-diff deep-flatten --image volume-ff53a61f-377d-4cfc-bd14-e1864b5cc78c -p volumes
8. 重新映射
```shell
[root@o15 ~]# rbd map volume-ff53a61f-377d-4cfc-bd14-e1864b5cc78c -p volumes
/dev/rbd1
```
9. 磁盘修复
xfs_repair -L /dev/rbd0p1
xfs_repair -L /dev/rbd1p1
xfs_repair -L /dev/rbd2p1
xfs_repair -L /dev/rbd3p1
xfs_repair -L /dev/rbd4p1
xfs_repair -L /dev/rbd5p1
xfs_repair -L /dev/rbd6p1
xfs_repair -L /dev/rbd7p1
10. 查看ceph映射列表
```shell
[root@o15 ~]# rbd showmapped
id pool    image                                       snap device
0  volumes volume-02242532-24da-40e8-b9a0-239792791883 -    /dev/rbd0
1  volumes volume-4119a5a0-b2f0-489d-8e24-d76a6e8796aa -    /dev/rbd1
2  volumes volume-6fbd8049-1506-4acb-b41e-6139720c2bb8 -    /dev/rbd2
3  volumes volume-b354bdc6-3ea3-4d68-8d73-671ae7ac2bf0 -    /dev/rbd3
4  volumes volume-c71fce73-5840-4eaf-afaf-d043bdb77272 -    /dev/rbd4
5  volumes volume-d51d7ed9-adad-4ed5-aabb-10318b57bdcf -    /dev/rbd5
6  volumes volume-ee585a9f-87bf-4757-af20-131319b78eee -    /dev/rbd6
7  volumes volume-ff53a61f-377d-4cfc-bd14-e1864b5cc78c -    /dev/rbd7
```
11. 取消映射
```shell
rbd unmap volume-02242532-24da-40e8-b9a0-239792791883 -p volumes
rbd unmap volume-4119a5a0-b2f0-489d-8e24-d76a6e8796aa -p volumes
rbd unmap volume-6fbd8049-1506-4acb-b41e-6139720c2bb8 -p volumes
rbd unmap volume-b354bdc6-3ea3-4d68-8d73-671ae7ac2bf0 -p volumes
rbd unmap volume-c71fce73-5840-4eaf-afaf-d043bdb77272 -p volumes
rbd unmap volume-d51d7ed9-adad-4ed5-aabb-10318b57bdcf -p volumes
rbd unmap volume-ee585a9f-87bf-4757-af20-131319b78eee -p volumes
rbd unmap volume-ff53a61f-377d-4cfc-bd14-e1864b5cc78c -p volumes
```
12. 重新启动虚拟机，虚拟机不再报错
