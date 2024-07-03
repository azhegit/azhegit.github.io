---
categories:
- 技术
- 虚拟化&云计算
date: 2018-11-02 13:40:51+08:00
tags:
- docker
thumbnailImage: //www.azheimage.top/markdown-img-paste-2018111316510833.png
title: Docker实践指南03-制作镜像及自动化启动
---

Docker实践指南03-制作镜像及启动
<!--more-->

![](https://www.azheimage.top/markdown-img-paste-20181101182650845.png)
## 制作Nginx镜像
### 1. 编写Dockerfile
```bash
# 基础镜像
FROM hub.c.163.com/library/nginx
# 编写者信息
MAINTAINER zheqing.wang "azheemail@163.com"
# 增加只读层，加载自己的资源
ADD dist /usr/share/nginx/html
# 设置服务器环境编码
ENV LANG en_GB.utf8
# 拷贝ngnix配置文件
COPY nginx.conf /etc/nginx/nginx.conf
# 曹蓓vin安装包
COPY vim-deb/ /opt
# 时间时区改为上海时区
RUN yes|cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
# 安装vim
RUN dpkg -i /opt/*
```
### 2. 制作镜像
`docker build -t wzq/nginx:1.0 .`

### 3. 启动镜像
`docker run --name kraken-nginx -p 2018:2018 --rm -d wzq/nginx:1.0`

## Dockerfile指令
|指令(常用命令加粗)|说明|
|-|-|
|**FROM**|指定所创建镜像的基础镜像
|**RUN**|运行命令
|**CMD**|指定启动容器时默认执行的命令
|LABEL|指定生成镜像的元数据标签信息
|EXPOSE|声明镜像内服务所监听的端口
|**ENV**|指定环境变量
|**ADD**|赋值指定的<src>路径下的内容到容器中的<dest>路径下，<src>可以为URL；如果为tar文件，会|自动解压到<dest>路径下
|**COPY**|赋值本地主机的<scr>路径下的内容到容器中的<dest>路径下；一般情况下推荐使用COPY而不是ADD
|**ENTRYPOINT**|指定镜像的默认入口
|**VOLUME**|创建数据挂载点
|USER|指定运行容器时的用户名或UID
|WORKDIR|配置工作目录
|ARG|指定镜像内使用的参数(例如版本号信息等)
|ONBUILD|配置当前所创建的镜像作为其他镜像的基础镜像时，所执行的创建操作的命令
|STOPSIGNAL|容器退出的信号
|HEALTHCHECK|如何进行健康检查
|SHELL|指定使用SHELL时的默认SHELL类型
