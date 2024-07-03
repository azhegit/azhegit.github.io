---
categories:
- 技术
- 大数据
date: '2018-08-13 15:34:37+08:00'
tags:
- cdh
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180831191033396.png
title: 新增机器到cdh集群
---
## 背景
新增2台机器，没有挂磁盘，需要添加到已有cdh集群。
<!--more-->

10.57.16.207
10.57.16.168

---------------

### 一、准备工作
### 1. admin用户准备工作
1. 添加用户
`useradd -d /home/admin admin -m`
2. 修改密码
`passwd admin` <!-- adminpwd -->
3. 增加sudo权限
`vi /etc/sudoers`
```bash
## Allows people in group wheel to run all commands
%wheel  ALL=(ALL)       ALL
admin    ALL=(ALL) NOPASSWD:ALL
```
4. 到admin生成密钥
`ssh-keygen`

### 2. 磁盘挂载
1. 查看系统中磁盘信息
`sudo fdisk -l`
>Disk /dev/vdb: 536.9 GB
2. 格式化磁盘
`sudo mkfs -t xfs /dev/vdb`
3. 创建数据目录
`sudo mkdir /data02`
4. 修改fstab，以便系统启动时自动挂载磁盘，编辑fstab默认启动文件命令：`sudo vim /etc/fstab` 回车在其中添加一行
`/dev/vdb               /data02             xfs    defaults        0 0`
5. 挂载
`sudo mount -a`
6. 查看磁盘挂载情况
`df -lh`

### 3. 安装cdh
1. 添加2台机器的ip到原有集群的hosts文件
2. 从manager节点做到这2台机器的免密
3. 关闭selinux
`sudo sed -i s/^SELINUX=.*/SELINUX=disabled/ /etc/selinux/config;`
4. 关闭防火墙
```bash
sudo systemctl stop firewalld.service;
sudo systemctl disable firewalld.service;
```
5. 配置ntp时间同步
6. 安装tng-tools
```bash
sudo yum install -y rng-tools;
sudo systemctl enable rngd.service;
sudo systemctl start rngd.service;
```
7. 修改主机名
`sudo hostnamectl set-hostname cdh168`
8. 配置java环境
9. 上传cdh安装包，并解压
`sudo tar zxvf cloudera-manager-centos7-cm5.14.3_x86_64.tar.gz -C /opt/
`
10. 重启服务器
`sudo init 6`
11. 修改目标主机中agent配置文件中的server_host={改成cm-server的ip}
`sudo vim /opt/cm-5.14.3/etc/cloudera-scm-agent/config.ini`
12. 启动agent
`sudo /opt/cm-5.14.3/etc/init.d/cloudera-scm-agent start`
13. 启动之后，查看所有主机，发现新启动的机器已经发现，但是此时还没有真正添加到集群
![](https://www.azheimage.top/markdown-img-paste-20200813151203370.png)
14. 点击向集群添加新主机
![](https://www.azheimage.top/markdown-img-paste-20200813151456899.png)
15. 勾选继续
![](https://www.azheimage.top/markdown-img-paste-20200813151536917.png)
16. 添加相应角色。




