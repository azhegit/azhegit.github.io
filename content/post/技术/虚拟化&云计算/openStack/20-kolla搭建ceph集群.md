---
categories:
- 技术
- 虚拟化&云计算
date: '2019-08-14 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180831191146955.png
title: 20-kolla搭建ceph集群
---
openstack 通过 kolla 搭建ceph 集群
<!--more-->

### 1. 安装docker及相关的环境（所有节点）
1. 上传相关文件

执行install-kolla.sh
2. 修改hosts

echo '
10.57.26.51 openstack-ceph-01
10.57.26.52 openstack-ceph-02
10.57.26.53 openstack-ceph-03
' >> /etc/hosts


### 2. 配置kolla，自动化部署OpenStack（主节点）
配置免密
ssh-keygen
ssh-copy-id openstack-ceph-01
ssh-copy-id openstack-ceph-02
ssh-copy-id openstack-ceph-03

修改物理网卡的neutron配置（为vlan模式配置）
vim /usr/share/kolla-ansible/ansible/roles/neutron/templates/ml2_conf.ini.j2
![](https://www.azheimage.top/markdown-img-paste-20190603110933366.png)

编辑 /etc/kolla/globals.yml 配置文件
vim /etc/kolla/globals.yml
```bash
#kolla_internal_vip_address 外部dashboard访问的地址
#network_interface dashboard对应内部的网卡
#neutron_external_interface 外部网卡
openstack_release: "queens"
kolla_internal_vip_address: "10.57.26.51"
network_interface: "eth0"
neutron_external_interface: "eth1"
docker_registry: "10.57.30.16:4000"
nova_compute_virt_type: "qemu"

enable_haproxy: "no"
# 以下为ceph配置
enable_ceph: "yes"
enable_ceph_rgw: "yes"
enable_cinder: "yes"

#如果是使用虚拟化实验环境，那么你需要把nova_compute_virt_type: "qemu" :

#目前安装kolla-ansible默认使用bluestore得ceph。这里演示使用filestore。需修改文件
#vim /usr/share/kolla-ansible/ansible/group_vars/all.yml
#修改如下属性：
#ceph_osd_store_type: "filestore"

ceph_osd_store_type: "filestore"
#副本数
osd_pool_default_size: 2

#Total PGs = ((Total_number_of_OSD * 100) / max_replication_count) / pool_count


ceph_pool_pg_num: 32
ceph_pool_pgp_num: 32
#ceph_target_max_bytes: ""  # 表示每个cache pool最大大小。注意，如果配置了cache盘，此项不配置会导致cache不会自动清空。cache_osd_size*cache_osd_num/replicated/cache_pool_num
#ceph_target_max_objects: "" # 表示cache pool最大的object数量
glance_backend_ceph: "yes"
glance_backend_file: "no"
enable_ceph_rgw_keystone: "yes"

```
编辑密码文件，配置keystone管理员用户的密码。
vim /etc/kolla/passwords.yml
database_password: Td@123
keystone_admin_password: admin


vim multinode
cat multinode|grep -v "^#"|grep -v "^$"
```bash
[control]
openstack-ceph-01
[network]
openstack-ceph-01
[inner-compute]
[external-compute]
[compute:children]
[compute]
openstack-ceph-01
openstack-ceph-02
openstack-ceph-03
[monitoring]
openstack-ceph-01
[storage:children]
compute
.....
```

[ml2_type_vlan]
{% if enable_ironic | bool %}
network_vlan_ranges = physnet1
{% else %}
network_vlan_ranges = physnet1
{% endif %}


cat /etc/kolla/config/ceph.conf
[global]
osd pool default size = 2
osd pool default min size = 1

查看磁盘
fdisk -l

umount /dev/vdb
格式化
mke2fs -t ext4 /dev/vdb


parted /dev/vdb -s -- mklabel gpt mkpart KOLLA_CEPH_OSD_BOOTSTRAP 1 -1

parted /dev/vdb print

kolla-ansible prechecks -i multinode

`docker rmi $(docker images | awk '{print $1":"$2}')`
kolla-ansible pull -i multinode

kolla-ansible deploy -i multinode



kolla-ansible deploy -t ceph


kolla-ansible destroy -i multinode --yes-i-really-really-mean-it
删除原来osd信息
rm -rf /var/lib/ceph/


### 问题
kolla-ansible 重新部署 ceph 遇到的问题
>TASK [ceph : Fetching Ceph keyrings] *******************************************fatal: [controller01]: FAILED! => {“failed”: true, “msg”: “The conditional check ‘{{ (ceph_files_json.stdout | from_json).changed }}’ failed. The error was: No JSON object could be decoded”

原因是在删除容器和配置文件后，kolla生成的相关volume是没有删除的。其还存在于/var/lib/docker/volume下。因此当再次构建kolla时，这些已经存在的volume会阻止ceph_mon的启动，会导致上述错误Ceph keyring无法获取而产生的一些错误。因此 删除掉docker volume ls下的卷。再次部署就能够成功的解决问题。
docker volume ls
>DRIVER              VOLUME NAME
local               ceph_mon
local               ceph_mon_config

docker volume rm ceph_mon ceph_mon_config
>ceph_mon
ceph_mon_config


4000/kolla/centos-binary-openvswitch-vswitchd


route add -host 169.254.169.254 gw 10.57.26.2 dev eth1
route -n
route del 169.254.169.254 gw 192.168.2.2


