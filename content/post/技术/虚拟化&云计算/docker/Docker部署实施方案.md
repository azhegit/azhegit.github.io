---
categories:
- 技术
- 虚拟化&云计算
date: 2018-11-02 13:50:51+08:00
tags:
- docker
thumbnailImage: //www.azheimage.top/markdown-img-paste-2018111316554474.png
title: Docker部署实施方案
---
Docker部署实施方案
<!--more-->
### Docker及docker-compose环境安装
安装docker并启动，具体步骤参考[docker离线安装]

### 查看镜像
`docker images`

### 保存镜像对应版本

把复杂网络相关的镜像保存下来，保存命令例如：
`docker save kraken/neo4j:1.0 > /data01/images/kraken/neo4j-1.0.tar`

### 拷贝保存好的镜像文件以及docker-compose.yml到对应服务器
把保存好的镜像文件拷贝到需要部署的服务器上（复杂网络docker-compose在/data01/docker/private-docker/kraken-docker）

### 导入镜像

把保存好的镜像文件拷贝到需要部署的服务器上，前提是docker已经安装好，并且已经启动，再执行导入命令:
`docker load < neo4j-1.0.tar`


### 查看镜像
docker images 检查镜像是否导入成功

### docker-compose启动复杂网络容器
安装好docker-compose之后，在docker-compose.yml当前路径执行启动命令：
`docker-compose down && docker-compose up`
