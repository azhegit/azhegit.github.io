---
categories:
- 技术
- 虚拟化&云计算
date: '2019-06-08 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //d1u9biwaxjngwg.cloudfront.net/welcome-to-tranquilpeak/city-750.jpg
title: 4-kolla安装单节点
---
kolla是基于自动化运维工具ansible，对OpenStack进行一键安装与部署，极大简化了部署流程，各组件是通多docker启动。
<!--more-->
## kolla安装单节点

### 1. 安全：
关闭防火墙与selinux：
systemctl disable firewalld.service
systemctl stop firewalld.service
systemctl status firewalld.service

setenforce 0

getenforce
sestatus
配置文件/etc/selinux/config，将SELINUX设置为disabled。

### ip
|主机|em1|em2|
|-|-|-|
|dataocean-d-030015.te.td|10.57.30.15|10.57.30.160


### 1. 安装docker
1. 添加Docker源
```bash
tee /etc/yum.repos.d/docker.repo << 'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/$releasever/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF
```
2. 添加代理
    1. yum 
        vim /etc/yum.conf
        ```ini
        proxy=http://10.57.22.8:3128
        proxy=ftp://10.57.22.8:3128
        proxy_username=username
        proxy_password=password
        ```
    2. http
        vim /etc/profile
        ```ini
        http_proxy=http://10.57.22.8:3128/
        https_proxy=https://10.57.22.8:3128/
        ftp_proxy=http://10.57.22.8:3128/
        export http_proxy
        export ftp_proxy
        export https_proxy
        ```
        source /etc/profile  
        curl  http://www.baidu.com

3. 安装docker1.12.6
yum install docker-engine-1.12.6 docker-engine-selinux-1.12.6 -y
4. 设置Docker
mkdir /etc/systemd/system/docker.service.d 
vim /etc/systemd/system/docker.service.d/kolla.conf
```bash
tee /etc/systemd/system/docker.service.d/kolla.conf << 'EOF'
[Service]
MountFlags=shared
EOF
```
5. 重启相关服务
systemctl daemon-reload
systemctl enable docker
systemctl restart docker
6. 配置阿里云的Docker加速器，加快pull registry镜像
mkdir -p /etc/docker
```bash
tee /etc/docker/daemon.json <<-'EOF'
{
"registry-mirrors": ["https://a5aghnme.mirror.aliyuncs.com"]
}
EOF
```
7. 重启下服务
systemctl daemon-reload && systemctl restart docker


### 2. 安装kolla
1. 安装 pip
yum install python-pip
pip install -U pip
2. 安装基础软件
yum install python-devel libffi-devel gcc openssl-devel libselinux-python git
3. 安装ansible
pip install -U ansible
4. 安装 kolla-ansible
pip install  --ignore-installed -U kolla-ansible
5. 复制相关配置文件
cp -r /usr/share/kolla-ansible/etc_examples/kolla /etc/
cp /usr/share/kolla-ansible/ansible/inventory/* /home/
6. 生成密码文件
kolla-genpwd
7. 编辑密码文件，配置keystone管理员用户的密码。
vim /etc/kolla/passwords.yml
keystone_admin_password: admin
database_password: Td@123
同时，也是登录Dashboard，admin使用的密码，你可以根据自己需要进行修改。
8 编辑 /etc/kolla/globals.yml 配置文件
vim /etc/kolla/globals.yml
```bash
#kolla_internal_vip_address 外部dashboard访问的地址
#network_interface dashboard对应内部的网卡
#neutron_external_interface 外部网卡

openstack_release: "queens"
kolla_internal_vip_address: "10.57.30.16"
network_interface: "em1"
neutron_external_interface: "em2"
enable_haproxy: "no"

```

9. 部署前检查
kolla-ansible prechecks -i /home/all-in-one
10. 先拉取镜像
导入镜像kolla-openstack-Queens-images.tar
docker load < kolla-openstack-Queens-images.tar
11. 安装 Docker python libraries， 否则会报错
pip install -U docker
12. 部署
kolla-ansible deploy -i /home/all-in-one
13. 修改网络vlan
vim /etc/kolla/neutron-server/ml2_conf.ini
```ini
[ml2]
#tenant_network_types = vxlan
#改为
tenant_network_types = vxlan,vlan
[ml2_type_vlan]
#network_vlan_ranges = 
#改为
network_vlan_ranges = physnet1:10:1000
```
vim /etc/kolla/neutron-openvswitch-agent/ml2_conf.ini
```ini
[ml2]
#tenant_network_types = vxlan
#改为
tenant_network_types = vxlan,vlan
[ml2_type_vlan]
#network_vlan_ranges = 
#改为
network_vlan_ranges = physnet1:10:1000
```
重启容器
docker restart neutron_server neutron_openvswitch_agent
docker exec -u root neutron_openvswitch_agent ovs-vsctl show
![](https://www.azheimage.top/markdown-img-paste-20190530134004609.png)
14. 验证部署，创建 /etc/kolla/admin-openrc.sh 文件
kolla-ansible post-deploy

15. 创建网络
neutron net-create vlan-130 --shared --provider:physical_network physnet1 --provider:network_type vlan --provider:segmentation_id 130
neutron subnet-create vlan-130 10.57.26.0/24 --name provider-130-subnet --gateway 10.57.26.1

16. 卸载OpenStack
kolla-ansible destroy -i /home/all-in-one --yes-i-really-really-mean-it
17. 单独安装某个组件
kolla-ansible deploy -t  mariadb

pip install --ignore-installed python-openstackclient


