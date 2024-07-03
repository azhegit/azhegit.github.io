---
categories:
- 技术
- 虚拟化&云计算
date: '2019-07-28 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725103847120.png
title: 14-suse镜像制作
---
suse镜像制作，qcow2格式，提供给OpenStack使用
<!--more-->

[toc]
## windows镜像制作
### 1. 硬件及软件准备

#### 1. 物理机一台
要求支持硬件虚拟化，将centos7安装在物理机上 
#### 2. 下载windows镜像
下载地址：https://www.suse.com/zh-cn/products/server/download/
下载SLE-12-SP3-Server-DVD-x86_64-GM-DVD1.iso
#### 3. Mac操作环境
#### 4. Mac安装VNC viewer
https://www.realvnc.com/en/connect/download/viewer/

### 2. 环境准备 

#### 1. 检查系统是否支持kvm
egrep "(vmx|svm)" /proc/cpuinfo
支持正常有回显：
![](https://www.azheimage.top/markdown-img-paste-20190611120220539.png)
#### 2. 安装软件包
yum install qemu-kvm qemu-img –y
#### 3. 创建链接
ln -s /usr/libexec/qemu-kvm /usr/bin/kvm
ln -s /usr/bin/qemu-img /usr/bin/kvm-img

### 3. 镜像制作
#### 1. 创建镜像目录，suse12-sp3的iso文件拷贝到该目录
mkdir suse12-sp3
把下载好的文件上传到服务器
![](https://www.azheimage.top/markdown-img-paste-20190929153449441.png)
#### 2. 制作磁盘文件（.qcow2），磁盘大小根据系统需求设定
qemu-img create -f qcow2 suse_12sp2.qcow2 20G
#### 3. 给存放镜像及磁盘文件的目录赋权，否则创建云主机时无法打开磁盘文件
chown qemu:qemu suse_12sp2.qcow2
#### 4. 启动基于windows7的kvm虚拟机，映射驱动器到vfd软盘
```
kvm -name suse_12sp2 \
-m 2048 \
-cdrom SLE-12-SP2-Server-DVD-x86_64-GM-DVD1.iso \
-drive file=suse_12sp2.qcow2,if=virtio \
-boot d \
-net nic,model=virtio \
-net user \
-balloon virtio \
-display vnc=:10
```
>选项解释：
-fda file 使用file作为软盘镜像.我们也可以通过将/dev/fd0作为文件名来使用主机软盘.
-cdrom file 使用文件作为CD-ROM镜像（IDE光盘镜像）
-boot [a|c|d] 由软盘(a),硬盘(c)或是CD-ROM(d).在默认的情况下由硬盘启动
-net nic[,vlan=n][,macaddr=addr] 创建一个新的网卡并与VLAN n
-net user[,vlan=n]  使用用户模式网络堆栈,这样就不需要管理员权限来运行.如果没有指 定-	net选项,这将是默认的情况
-balloon virtio  使用virtio balloon
#### 5. 使用vnc客户端连接kvm安装系统及驱动
1. 输入10.57.30.15:10地址及端口
![](https://www.azheimage.top/markdown-img-paste-20190929160200270.png)
2. 点击continue
![](https://www.azheimage.top/markdown-img-paste-20190929160238140.png)
3. 选择installation，开始安装
![](https://www.azheimage.top/markdown-img-paste-20190929160417788.png)
4. 等待
![](https://www.azheimage.top/markdown-img-paste-20190929160816889.png)
5. 勾选同意，next
![](https://www.azheimage.top/markdown-img-paste-20190929161244166.png)
6. 跳过注册，next
![](https://www.azheimage.top/markdown-img-paste-20190929161352505.png)
7. 保持默认，next
![](https://www.azheimage.top/markdown-img-paste-20190929161419621.png)
![](https://www.azheimage.top/markdown-img-paste-20190929161939476.png)
8. 如果不分区，保持默认，next
![](https://www.azheimage.top/markdown-img-paste-20190929162011671.png)
如果分区，页面上将会出现Edit proposal settings（编辑提案设置）、Create Partition Setup    （创建分区设置）、Expert Partitioner（专家分割器）三个按钮，如图选择Expert Partitioner按钮
![](https://www.azheimage.top/markdown-img-paste-20190929212459442.png)
点击Hard Disks将会出现如下图右边页面，
![](https://www.azheimage.top/markdown-img-paste-20190929212551799.png)

9. 选择上海时区
![](https://www.azheimage.top/markdown-img-paste-20190929162044774.png)
10. 创建默认用户admin，并且管理员密码也跟admin密码一样
![](https://www.azheimage.top/markdown-img-paste-20190929162223148.png)
11. 选择software
![](https://www.azheimage.top/markdown-img-paste-20190929162357947.png)
12. 去除桌面，gnome
![](https://www.azheimage.top/markdown-img-paste-2019092916250345.png)
13. install
![](https://www.azheimage.top/markdown-img-paste-20190929162529701.png)
14. 自动重启
![](https://www.azheimage.top/markdown-img-paste-20190929163230718.png)
15. 登录成功
![](https://www.azheimage.top/markdown-img-paste-20190929163352885.png)
16. 关闭防火墙
suse12下操作为：
关闭防火墙
systemctl stop SuSEfirewall2.service
取消开机启动防火墙
systemctl disable SuSEfirewall2.service
17. 正常关机保存设置
查看磁盘文件格式并进行格式转换
qemu-img info suse_12sp2.qcow2
![](https://www.azheimage.top/markdown-img-paste-2019092916383074.png)
qemu-img convert -f qcow2 -O qcow2 suse_12sp2.qcow2  suse_12sp2_private_cloud.qcow2
#### 6. 上传制作好的镜像并激活
1. OpenStack界面操作上传镜像好的镜像
2. 创建实例
3. 将快照变成镜像
glance image-create --name "windows_server_2012_1" --file 8eb12b73-95ed-404f-89ce-939ff474569f --disk-format qcow2 --container-format bare --protected False --progress  --property visibility="public"

