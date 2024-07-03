---
categories:
- 技术
- 数据库
date: '2022-06-23 16:42:49+08:00'
tags:
- Aerospike
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110153448285.png
title: 17-本机docker搭建集群
---
docker-compose.yml
<!--more-->
```yml
aerospike-amc:
  image: aerospike/amc
  ports:
    - "8081:8081"


aerospike-1:
  image: aerospike:ce-5.7.0.7
  container_name: aerospike-1
  ports:
    - "3000:3000"
    - "3001:3001"
    - "3002:3002"
  volumes:
    - /etc/localtime:/etc/localtime
  environment:
    NAMESPACE: large

aerospike-2:
  image: aerospike:ce-5.7.0.7
  container_name: aerospike-2
  ports:
    - "4000:3000"
    - "4001:3001"
    - "4002:3002"
  volumes:
    - /etc/localtime:/etc/localtime
  environment:
    NAMESPACE: large

aerospike-3:
  image: aerospike:ce-5.7.0.7
  container_name: aerospike-3
  ports:
    - "5000:3000"
    - "5001:3001"
    - "5002:3002"
  volumes:
    - /etc/localtime:/etc/localtime
  environment:
    NAMESPACE: large

```
启动
sudo docker-compose up -d

docker exec -e "AEROSPIKE2=$(docker exec -ti aerospike-2 asinfo -v service|cut -d ':' -f1)" -ti aerospike asinfo -v 'tip:host=$AEROSPIKE2;port=3002'

docker exec -e "AEROSPIKE2=$(docker exec -ti aerospike-3 asinfo -v service|cut -d ':' -f1)" -ti aerospike asinfo -v 'tip:host=$AEROSPIKE2;port=3002'

或者
asinfo -v 'tip:host=172.17.0.3;port=3002'
asinfo -v 'tip:host=121.40.238.63;port=4002'


asinfo -v 'tip:host=121.40.238.63;port=5002'
asinfo -v 'tip:host=172.16.20.194;port=3002'


