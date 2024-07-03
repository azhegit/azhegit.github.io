---
categories:
- 技术
- 虚拟化&云计算
date: '2019-06-14 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110143922992.png
title: 10-制作centos7镜像
---
centos7镜像制作，qcow2格式，提供给OpenStack使用
<!--more-->
## 基于centos官方的cloud镜像制作镜像
[toc]
### 1. 下载clould 镜像
最简单的方法是使用标准镜像。主流的Linux发行版都提供可以在 OpenStack 中直接使用的cloud镜像，下载地址：
CentOS6：http://cloud.centos.org/centos/6/images/
CentOS7：http://cloud.centos.org/centos/7/images/
Ubuntu14.04：http://cloud-images.ubuntu.com/trusty/current/
Ubuntu16.04：http://cloud-images.ubuntu.com/xenial/current/

### 2. 创建Glance镜像
登录 OpenStack，打开 “项目->计算->镜像”菜单。创建镜像并上传
![](https://www.azheimage.top/markdown-img-paste-20190612162149256.png)

### 3. 定制镜像
cloud 镜像是标准镜像，没有图像界面，是美国时区，而且只能通过密钥登录。可以根据需要对该镜像进行定制，其方法是：
#### 1. 通过cloud镜像部署出一个实例(使用密钥对)
![](https://www.azheimage.top/markdown-img-paste-20190612162255456.png)
#### 2. 定制该实例。
1. 通过密钥对登录
ssh -i /Users/azhe/Downloads/os-key.pem centos@xx.xx.xx.xx
2. 切换root用户
sudo -i
3. 改root密码
passwd
Td@123
4. 设置时区
timedatectl set-timezone Asia/Shanghai
5. 设置yum 源
从别的机器拷贝yum源
scp -i ~/os-key.pem CentOS-Base.repo epel.repo rpmforge.repo saltstack.repo centos@xx.xx.xx.xx:~
移动yum源
mv ./*.repo /etc/yum.repos.d/
6. 删除centos用户
userdel -f centos
7. 修改cloud-init
vi /etc/cloud/cloud.cfg
```bash
ssh_pwauth:   1
    name: admin
```
8. 修改远程登录
vi /etc/ssh/sshd_config
```bash
#关闭root远程登录
PermitRootLogin no
```
9. 关机，拍快照
10. 将快照变成镜像
glance image-create --name "centos7_private_cloud" --file /var/lib/docker/volumes/glance/_data/images/a20112d0-c502-47bd-9b9a-06d501788d9c --disk-format qcow2 --container-format bare --protected False --progress  --property visibility="public"




