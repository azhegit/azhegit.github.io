---
categories:
- 技术
date: '2020-08-26 12:23:52+08:00'
tags:
- 自动化运维
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725100954649.png
title: ansible离线部署
---

通过ansible构建加密kafka集群,实现一键部署及一键卸载。
<!--more-->

# Ansible 离线环境自动化部署工程
[toc]
- 安装部署：上传软件安装包到指定主机组，修改软件相关配置文件，启动相关软件
  1. hostname模块，用于hostname修改及添加主机映射
  2. ssh-key模块，用于互相免密
  3. java模块，部署jdk
  4. rpm模块，安装常用软件模块
  5. zookeeper模块，zookeeper集群部署及启动
  6. kafka模块，kafka集群部署及启动
  7. kafka-manager模块，kafka-manager部署及启动
  8. docker模块，docker部署及启动
  9. monitor模块，grafana及prometheus部署及启动

- 卸载脚本：停止对应模块的服务，删除对应软件添加的环境变量及恢复修改的每一个配置文件
  1. monitor模块，grafana及prometheus停止，删除软件安装目录及数据目录
  2. docker模块，docker停止，删除软件安装目录及数据目录
  3. kafka-manager模块，kafka-manager停止，删除软件安装目录及数据目录
  4. kafka模块，kafka集群停止，删除软件安装目录及数据目录
  5. zookeeper模块，zookeeper集群停止，删除软件安装目录及数据目录
  6. rpm模块，安装的对应软件卸载
  7. java模块，删除软件安装目录
  8. ssh-key模块，删除ansible安装添加的密钥
  9. hostname模块，删除添加主机映射

## 要求

试用于Centos7

## 开发测试环境

- ansible `2.6.1`
- 运行os `MacOs`/`CentosOS/Redhat`
- 目标os `Centos 7.5`
- 运行python `2.7.16`

## 依赖
1. 部署用户拥有sudo权限
2. 部署用户的密码

## 结构
```yaml
#离线部署安装包及部分shell脚本
├── basic-files
│   ├── docker
│   ├── exporter
│   ├── java
│   ├── kafka
│   ├── kafka-manager
│   ├── monitor
│   ├── rpms
│   └── zookeeper
#git提交脚本
├── gitPush.sh
#部署脚本
├── install.sh
#卸载脚本
│── uninstall.sh
#ansible工程
├── private-devops
│   ├── README.md
#安装剧本
│   ├── install.yml
#主机配置及全局变量
│   ├── inventory
#角色
│   ├── roles
#卸载剧本
└   └── uninstall.yml


```
### 配置环境：
```ini
;配置机器name及ip
[machines]
kafka-1 ansible_ssh_host=10.57.26.110
kafka-2 ansible_ssh_host=10.57.26.111
kafka-3 ansible_ssh_host=10.57.26.112

;配置角色主机组
[hostname:children]
machines

[ssh:children]
machines

[java]
kafka-1
kafka-2
kafka-3

;全局变量
[all:vars]
;操作用户
ansible_user=admin
;操作用户的密码
ansible_ssh_pass="adminpwd"
;指定离线安装包目录
basic_files_path=../basic-files
;安装器
;installer_ssh=uninstall

;角色变量
[kafka:vars]
;kafka权限相关配置
sasl_enable= true
;sasl_user: "admin"
;sasl_password: "adminpwd"

[rpm:vars]
;rpm模块需要安装的软件
soft= ['perl','vim']
```
### 剧本
模块化配置，配置文件对应参考install.yml

```yaml
- name: hostname
#指定主机组模板
  hosts: hostname
#是否开启sudo权限
  become: true
  roles:
#指定模板
    - role: hostname
```

### 命令介绍
部署脚本:./install.sh -v
卸载脚本:./uninstall.sh -v
>后面参数可以是-v -vv -vvv 用于调试级别,也可以保持默认

或者手动通过ansible-playbook命令指定环境，及剧本执行安装：`ansible-playbook -i private-devops/inventory/install.ini private-devops/install.yml`


## 快速开始
### 环境准备
1. 将项目工程拷贝到执行部署的机器上
2. 编写环境变量，[变量介绍](private-devops/inventory/README.md)，也可以参考默认安装变量配置：[加密kafka集群](private-devops/inventory/install.ini)
3. 编写剧本，[剧本介绍](private-devops/README.md)，可根据已有的模块任意搭配，调整模块执行顺序，[默认安装剧本](private-devops/install.yml)`install.yml`是安装加密kafka集群及监控，`uninstall.yml`是卸载kafka集群及监控
### 部署
1. 执行对应的脚本，安装脚本`install.sh`，卸载脚本`uninstall.sh`
![](https://www.azheimage.top/markdown-img-paste-20200826121526678.png)
2. 安装完成
![](https://www.azheimage.top/markdown-img-paste-20200826121505908.png)
3. 登录grafana
![](https://www.azheimage.top/markdown-img-paste-20200826121608702.png)
4. 配置grafana的数据源-prometheus
![](https://www.azheimage.top/markdown-img-paste-2020082612162508.png)
![](https://www.azheimage.top/markdown-img-paste-20200826121718837.png)
5. 配置prometheus数据源
![](https://www.azheimage.top/markdown-img-paste-20200826121730730.png)
6. 导入grafana图表配置

![](https://www.azheimage.top/markdown-img-paste-20200826121745711.png)
![](https://www.azheimage.top/markdown-img-paste-20200826121802263.png)
选择已经配置好的图表json文件，位置在basic-files/monitor/kafka集群监控-1593325791671.json
![](https://www.azheimage.top/markdown-img-paste-20200826121814428.png)
7. 查看grafana图表
![](https://www.azheimage.top/markdown-img-paste-20200826121831891.png)
8. kafka-manager配置
![](https://www.azheimage.top/markdown-img-paste-20200826121907599.png)
![](https://www.azheimage.top/markdown-img-paste-2020082612192219.png)

### 卸载
1. 编写环境变量，[变量介绍](private-devops/inventory/README.md)，也可以参考默认卸载变量配置：[加密kafka集群](private-devops/inventory/uninstall.ini)
2. 编写剧本，[剧本介绍](private-devops/README.md)，可根据已有的模块任意搭配，调整模块执行顺序，[默认卸载剧本](private-devops/uninstall.yml)`install.yml`是安装加密kafka集群及监控，`uninstall.yml`是卸载kafka集群及监控
3. 执行uninstall.sh
![](https://www.azheimage.top/markdown-img-paste-2020082612193568.png)
![](https://www.azheimage.top/markdown-img-paste-20200826121943908.png)
## 目前支持模块
- [x] [hostname](private-devops/roles/hostname)
- [x] [ssh](private-devops/roles/ssh)
- [x] [java](private-devops/roles/java)
- [x] [rpms](private-devops/roles/rpms)
- [x] [zookeeper](private-devops/roles/zookeeper)
- [x] [kafka](private-devops/roles/kafka)
- [x] [kafka-manager](private-devops/roles/kafka-manager)
- [x] [docker](private-devops/roles/docker)
- [x] [monitor](private-devops/roles/monitor)

## 未来可能支持模块
- [ ] hadoop
- [ ] flink
- [ ] springboot
- [ ] stream-server



