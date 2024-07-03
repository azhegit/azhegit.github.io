---
categories:
- 技术
- 虚拟化&云计算
date: '2019-06-07 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-2019011014402315.png
title: 3-openstack操作
---
环境部署好了，界面操作
<!--more-->
[toc]
访问连接：http://10.58.10.19/dashboard

## OpenStack操作

### 1. 新建实例类型
管理员-->系统-->实例类型-->新建实例类型：
![](https://www.azheimage.top/markdown-img-paste-2019052318514522.png)

### 2. 创建镜像
![](https://www.azheimage.top/markdown-img-paste-2019052318551439.png)

### 3. 创建网络
1. 创建 
![](https://www.azheimage.top/markdown-img-paste-2019060411225204.png)
![](https://www.azheimage.top/markdown-img-paste-20190523194345497.png)
2. 创建子网
![](https://www.azheimage.top/markdown-img-paste-20190523194121574.png)
3. 子网配置
![](https://www.azheimage.top/markdown-img-paste-20190523194216797.png)
成功
![](https://www.azheimage.top/markdown-img-paste-2019052319432000.png)
4. 添加路由器
项目-->网络-->路由-->新建路由：
![](https://www.azheimage.top/markdown-img-paste-20190523194718557.png)
![](https://www.azheimage.top/markdown-img-paste-20190523194805573.png)

### 4. 新建实例
1. 创建实例
![](https://www.azheimage.top/markdown-img-paste-20190523195048238.png)
2. 选择镜像
![](https://www.azheimage.top/markdown-img-paste-20190523195107587.png)
3. 选择实例类型
![](https://www.azheimage.top/markdown-img-paste-20190523195122437.png)
4. 选择网络，网络接口不要管自动dhcp分配
![](https://www.azheimage.top/markdown-img-paste-20190523195154932.png)
5. 配置中添加修改用户名centos的密码为centos
![](https://www.azheimage.top/markdown-img-paste-20190523195429275.png)

![](https://www.azheimage.top/markdown-img-paste-20190524112643792.png)

