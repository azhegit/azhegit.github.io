---
categories:
- 技术
- 虚拟化&云计算
date: '2019-06-15 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725101125909.png
title: 11-Kolla环境部署命令
---
kolla部署OpenStack，常用部署运维命令
<!--more-->
### kolla常用命令集

1. 根据需要，配置/etc/kolla/global.yml，可选择需要部署的容器；
2. 在/etc/kolla/passwords.yml设置horizon密码、keystone认证密码或数据库密码等；
3. 在部署节点执行kolla-ansible命令
    1. 如果是单节点执行：#kolla-ansible deploy
    2. 如果是多节点执行：#kolla-ansible -i multinode deploy
4. 生成admin-openrc.sh认证文件执行
kolla-ansible post-deploy
5. 如果执行失败执行destroy操作
kolla-ansible destroy -i delete-compute --yes-i-really-really-mean-i
6. 单独部署某一容器
    1. 单节点：#kolla-ansible deploy -t nova（指定容器）
    2. 多节点：#kolla-ansible -i multinode deploy -t nova（指定容器）
7. 部署前检查
kolla-ansible prechecks -i my-multinode
8. 部署
kolla-ansible -i my-multinode deploy
9. 销毁
kolla-ansible destroy -i my-multinode --yes-i-really-really-mean-it
10. 生成环境变量
单节点
kolla-ansible post-deploy
多节点
kolla-ansible post-deploy -i /usr/share/kolla-ansible/ansible/inventory/multinode
11. 部署完成后如果需要重新配置
如果修改了/etc/config/[server]/[server].conf
单节点：
kolla-ansible reconfigure 
多节点：
kolla-ansible reconfigure -i /usr/share/kolla-ansible/ansible/inventory/multinode
如果修改了全局配置 /etc/kolla/globals.yml
单节点：
kolla-ansible upgrade
kolla-ansible post-deploy
多节点：
kolla-ansible upgrade -i /usr/share/kolla-ansible/ansible/inventory/multinode
kolla-ansible post-deploy -i /usr/share/kolla-ansible/ansible/inventory/multinode

12. 查询镜像
glance image-list
13. 导出镜像
glance image-download --file /root/win2012_server_R2.qcow2 24b8c1d8-75cd-48a3-a68e-3cbd86d4e59c
14. 

下载安装openstack软件仓库（queens版本）
yum install centos-release-openstack-queens -y
