---
categories:
- 技术
- 虚拟化&云计算
date: '2019-08-18 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110153448285.png
title: 21-kolla对接ceph(all-in-one)
---
kolla 对接ceph

<!--more-->

执行install-kolla.sh

编辑 /etc/kolla/globals.yml 配置文件
vim /etc/kolla/globals.yml
```bash
#kolla_internal_vip_address 外部dashboard访问的地址
#network_interface dashboard对应内部的网卡
#neutron_external_interface 外部网卡
Stein
openstack_release: "queens"
kolla_internal_vip_address: "10.57.30.16"
network_interface: "eth0"
neutron_external_interface: "lo"
enable_haproxy: "no"
docker_registry: "10.57.30.16:4000"

enable_cinder: "yes"

# 以下为ceph配置
enable_ceph: "yes"
enable_ceph_rgw: "yes"
enable_ceph_rgw_keystone: "yes"
#ceph_target_max_bytes: ""  # 表示每个cache pool最大大小。注意，如果配置了cache盘，此项不配置会导致cache不会自动清空。cache_osd_size*cache_osd_num/replicated/cache_pool_num
#ceph_target_max_objects: "" # 表示cache pool最大的object数量
glance_backend_ceph: "yes"
glance_backend_file: "no"

#如果是使用虚拟化实验环境，那么你需要把nova_compute_virt_type: "qemu" :
nova_compute_virt_type: "qemu"
ceph_osd_store_type: "filestore"
```

systemctl daemon-reload && systemctl restart docker


目前安装kolla-ansible默认使用bluestore得ceph。这里演示使用filestore。需修改文件
vim /usr/share/kolla-ansible/ansible/group_vars/all.yml
修改如下属性：
ceph_osd_store_type: "filestore"


编辑密码文件，配置keystone管理员用户的密码。
vim /etc/kolla/passwords.yml
database_password: Td@123
keystone_admin_password: admin


umount /dev/vdb
格式化
mke2fs -t ext4 /dev/vdb

parted /dev/vdb -s -- mklabel gpt mkpart KOLLA_CEPH_OSD_BOOTSTRAP 1 -1

parted /dev/vdb print

kolla-ansible prechecks -i all-in-one

`docker rmi $(docker images | awk '{print $1":"$2}')`
kolla-ansible pull -i all-in-one

kolla-ansible deploy -i all-in-one

kolla-ansible destroy -i all-in-one --yes-i-really-really-mean-it


parted /dev/vdb -s -- mklabel gpt mkpart KOLLA_CEPH_OSD_BOOTSTRAP 1 -1


parted /dev/sdb -s -- mklabel gpt mkpart KOLLA_CEPH_OSD_BOOTSTRAP 1 -1
parted /dev/sdb print

kolla-ansible deploy -t ceph


mke2fs -t ext4 /dev/sda
删除原来osd信息
rm -rf /var/lib/ceph/

parted /dev/sda -s -- mklabel gpt mkpart KOLLA_CEPH_OSD_BOOTSTRAP 1 -1





