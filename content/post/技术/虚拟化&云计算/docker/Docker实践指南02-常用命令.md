---
categories:
- 技术
- 虚拟化&云计算
date: 2018-11-02 13:35:51+08:00
tags:
- docker
thumbnailImage: //www.azheimage.top/markdown-img-paste-20181113164859849.png
title: Docker实践指南02-常用命令
---
Docker实践指南02-常用命令
<!--more-->

## Docker常用命令
![](https://www.azheimage.top/markdown-img-paste-20181101182650845.png)
#### 1. 查找镜像:
`docker search hello`
![](https://www.azheimage.top/markdown-img-paste-20181101210456163.png)
#### 2. 拉取镜像：
`docker pull hello-world`
#### 3. 查看本机镜像：
`docker images`
![](https://www.azheimage.top/markdown-img-paste-20181101210757745.png)
#### 4. 删除本机镜像：
`docker rmi wzq/neo4j:1.0`/`docker rmi <IMAGE ID>`
#### 5. 提交镜像：
`docker commit <container id> <REPOSITORY:TAG>`
#### 6. 从容器导出、导入镜像：
`docker export 890sadfae12se2 > centos_cms11.tar`
`cat centos_cms11.tar | docker import -registry:5000/centos_cms:v1`
#### 7. 存出和载入镜像:
`docker save registry:5000/centos_cms:v1.0 > centos_cms11.tar`
`docker load < centos_cms11.tar`
#### 8. 停止容器
`docker stop containerID`
#### 9. 启动容器
`docker start containerID`
#### 10. 重启容器
`docker restart containerID`
#### 11. 删除容器
`docker rm –f containerID`
#### 12. 强制停止容器
`docker kill containerID`
#### 13. 进入镜像
`docker exec -it containerID bash`
#### 14. 构建镜像
`docker build -t <REPOSITORY:TAG>:1.0 .`
>-t  second : v1.0  给新构建的镜像取名为 second， 并设定版本为 v1.0 。
docker build： 用 Dockerfile 构建镜像的命令关键词。
[OPTIONS] : 命令选项，常用的指令包括 -t 指定镜像的名字，
    -f 显示指定构建镜像的 Dockerfile 文件（Dockerfile 可不在当前路径下），
     如果不使用 -f，则默认将上下文路径下的名为 Dockerfile 的文件认为是构建镜像的 "Dockerfile" 。
上下文路径|URL： 指定构建镜像的上下文的路径，构建镜像的过程中，可以且只可以引用上下文中的任何文件 。
#### 15. 删除所有容器
`docker rm $(docker ps -a -q)`
#### 16. 删除所有镜像
`docker rmi $(docker images -q)`
#### 17. 停止所有镜像
`docker stop $(docker ps -q)`
`docker kill $(docker ps -q)`
#### 18. 查看容器inspect
`docker inspect 43 | grep IPAddress`
#### 18. 查看容器
docker ps --format "table {{.Names}}\t{{.Status}}"


## docker启动Nginx
### 1. 使用[网易云镜像](https://c.163yun.com/hub#/m/home/)
### 2. 拉取镜像到本地
`docker pull hub.c.163.com/library/nginx:latest`
### 3. 查看本地镜像
`docker images`
![](https://www.azheimage.top/markdown-img-paste-20181025120216798.png)
### 4. 启动Nginx docker镜像
`docker run -d -p 9090:80 hub.c.163.com/library/nginx`
![](https://www.azheimage.top/markdown-img-paste-20181025120924425.png)
![](https://www.azheimage.top/markdown-img-paste-20181025121021886.png)
### 5. 进入容器`docker exec -it 46 bash`
### 6. 关闭应用：
![](https://www.azheimage.top/markdown-img-paste-20181025121456370.png)
### 7. 加载自己的资源：
`docker run --rm  -v /Users/azhe/Downloads/dist:/usr/share/nginx/html:ro -v /Users/azhe/Downloads/nginx.conf:/etc/nginx/nginx.conf -d -p 2018:2018 hub.c.163.com/library/nginx`


## docker启动mysql
### 1. 拉取镜像
  `docker pull hub.c.163.com/library/mysql:5.7`
### 2. 运行镜像
  `docker run -e MYSQL_ROOT_PASSWORD="jkljkl" -d  -p 3306:3306 hub.c.163.com/library/mysql:5.7`
### 3. 查看ip:
  `docker inspect 43 | grep IPAddress`
### 4. 修改远程访问权限
  `ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';`
