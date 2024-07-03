---
categories:
- 技术
- 虚拟化&云计算
date: '2019-06-05 13:36:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180831191033396.png
title: 0-OpenStack研究
---
研究OpenStack云平台
<!--more-->
--------
# OpenStack研究
<!-- [ton] -->
## 1. 架构图
![](https://www.azheimage.top/markdown-img-paste-20190530163441933.png)
![](https://www.azheimage.top/markdown-img-paste-2019053016351624.png)

## 2. 包含组件
### 共享服务项目3个
1. 认证服务
服务名：认证服务
项目名：Keystone
功能：为访问openstack各组件提供认证和授权功能，认证通过后，提供一个服务列表（存放你有权访问的服务），可以通过该列表访问各个组件。
2. 镜像服务
服务名：镜像服务
项目名：Glance
功能：为云主机安装操作系统提供不同的镜像选择
3. 计费服务
服务名：计费服务
项目名：Ceilometer
功能：收集云平台资源使用数据，用来计费或者性能监控

### 核心项目3个
1. 控制台
服务名：Dashboard
项目名：Horizon
功能：web方式管理云平台，建云主机，分配网络，配安全组，加云盘

2. 计算
服务名：计算
项目名：Nova
功能：负责响应虚拟机创建请求、调度、销毁云主机
3. 网络
服务名：网络
项目名：Neutron
功能：实现SDN（软件定义网络），提供一整套API,用户可以基于该API实现自己定义专属网络，不同厂商可以基于此API提供自己的产品实现
### 存储项目2个
1. 对象存储
服务名：对象存储
项目名：Swift
功能：REST风格的接口和扁平的数据组织结构。RESTFUL HTTP API来保存和访问任意非结构化数据，ring环的方式实现数据自动复制和高度可以扩展架构，保证数据的高度容错和可靠性
2. 块存储
服务名：块存储
项目名：Cinder
功能：提供持久化块存储，即为云主机提供附加云盘。

### 高层服务项目1个
1. 编排服务
服务名：编排服务
项目名：Heat
功能：自动化部署应用，自动化管理应用的整个生命周期.主要用于Paas 

## 3. 创建虚拟机过程
![](https://www.azheimage.top/markdown-img-paste-20190530164052193.png)
1. 界面或命令行通过RESTful API向keystone获取认证信息。
2. keystone通过用户请求认证信息，并生成auth-token返回给对应的认证请求。
3. 界面或命令行通过RESTful API向nova-api发送一个boot instance的请求（携带auth-token），包含需要创建的虚拟机信息，如CPU、内存、硬盘、网络等。
4. nova-api接受请求后向keystone发送认证请求，查看token是否为有效用户和token。
5. keystone验证token是否有效，如有效则返回有效的认证和对应的角色（注：有些操作需要有角色权限才能操作）。
6. 通过认证后nova-api和数据库通讯。
7. 初始化新建虚拟机的数据库记录。
8. nova-api通过rpc.call向nova-scheduler请求是否有创建虚拟机的资源(Host ID)。
9. nova-scheduler进程侦听消息队列，获取nova-api的请求。
10. nova-scheduler通过查询nova数据库中计算资源的情况，并通过调度算法计算符合虚拟机创建需要的主机。
11. 对于有符合虚拟机创建的主机，nova-scheduler更新数据库中虚拟机对应的物理主机信息。
12. nova-scheduler通过rpc.cast向nova-compute发送对应的创建虚拟机请求的消息（调度到选定的nova-compute上创建VM）。
13. nova-compute会从对应的消息队列中获取创建虚拟机请求的消息（新版的openstack，不允许Nova-compute直接连接数据库，只能通过nova-conductor去调用），有多个nova-compute节点）
14. nova-compute通过rpc.call向nova-conductor请求获取虚拟机消息。（Flavor）
15. nova-conductor从消息队队列中拿到nova-compute请求消息。
16. nova-conductor根据消息查询虚拟机对应的信息。
17. nova-conductor从数据库中获得虚拟机对应信息。
18. nova-conductor把虚拟机信息通过消息的方式发送到消息队列中。
19. nova-compute从对应的消息队列中获取虚拟机信息消息。
20. nova-compute通过keystone的RESTfull API拿到认证的token，并通过HTTP请求glance-api获取创建虚拟机所需要镜像。
21. glance-api向keystone认证token是否有效，并返回验证结果。
22. token验证通过，nova-compute获得虚拟机镜像信息(URL)。
23. nova-compute通过keystone的RESTfull API拿到认证k的token，并通过HTTP请求neutron-server获取创建虚拟机所需要的网络信息。
24. neutron-server向keystone认证token是否有效，并返回验证结果。
25. token验证通过，nova-compute获得虚拟机网络信息。
26. nova-compute通过keystone的RESTfull API拿到认证的token，并通过HTTP请求cinder-api获取创建虚拟机所需要的持久化存储信息。
27. cinder-api向keystone认证token是否有效，并返回验证结果。
28. token验证通过，nova-compute获得虚拟机持久化存储信息。
29. nova-compute根据instance的信息调用配置的虚拟化驱动来创建虚拟机。
## 4. 工作任务及计划
![](https://www.azheimage.top/markdown-img-paste-20190530162415784.png)
## 5. 访问地址
1. 手动安装版本（集群）：http://10.57.30.57
2. kolla安装版本（单机）：http://10.57.30.15

## 6. 问题难点：
1. 手动安装部署困难
2. 架构比较复杂，涉及运维技术比较多，学习门槛比较高
3. 系统不熟悉，维护难度比较大
