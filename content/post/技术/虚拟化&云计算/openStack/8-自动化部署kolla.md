---
categories:
- 技术
- 虚拟化&云计算
date: '2019-06-12 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20181113165255716.png
title: 8-自动化部署kolla
---
离线环境，自动化部署
<!--more-->
### 1. 新环境安装准备
1. 上传OpenStack离线部署相关资源包
2. 安装kolla及所需依赖
install-kolla.sh

### 3. 安装
1. 编辑 /etc/kolla/globals.yml 配置文件
vim /etc/kolla/globals.yml
```bash
#kolla_internal_vip_address 虚拟IP必须是一个ping不通的地址，外部dashboard访问的地址
#network_interface dashboard对应的网卡
#neutron_external_interface 内部网卡

openstack_release: "queens"
kolla_internal_vip_address: "10.57.30.16"
network_interface: "em1"
neutron_external_interface: "em2"
enable_haproxy: "yes"
docker_registry: "10.57.30.15:4000"
```
2. 修改docker配置
```bash
tee /etc/docker/daemon.json << 'EOF'
{
  "insecure-registries":["10.57.30.15:4000"]
}
EOF
```
3. 本地镜像仓库，拉取镜像
kolla-ansible -i add-compute pull

docker save -o registry.tar registry


`docker save $(docker images | grep -v REPOSITORY | awk 'BEGIN{OFS=":";ORS=" "}{print $1,$2}') -o kolla-openstack-Queens-images.tar`


docker tag busybox 10.57.30.15:4000/busybox:1.0

docker push 10.57.30.15:4000/busybox:1.0


docker pull 10.57.30.15:4000/busybox:1.0

#### 本地镜像删除
[root@master registry]# curl https://raw.githubusercontent.com/burnettk/delete-docker-registry-image/master/delete_docker_registry_image.py | sudo tee /usr/local/bin/delete_docker_registry_image >/dev/null

sudo chmod a+x /usr/local/bin/delete_docker_registry_image 