---
categories:
- 技术
- 虚拟化&云计算
date: '2019-08-13 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725100954649.png
title: 19-ceph-deploy安装ceph
---
<!--more-->

1. 配置yum源
```bash
cat <<END >/etc/yum.repos.d/ceph.repo
[Ceph]
name=Ceph packages for $basearch
baseurl=http://mirrors.aliyun.com/ceph/rpm-luminous/el7/$basearch
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=https://download.ceph.com/keys/release.asc

[Ceph-noarch]
name=Ceph noarch packages
baseurl=http://mirrors.aliyun.com/ceph/rpm-luminous/el7/noarch
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=https://download.ceph.com/keys/release.asc

[ceph-source]
name=Ceph source packages
baseurl=http://mirrors.aliyun.com/ceph/rpm-luminous/el7/SRPMS
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=https://download.ceph.com/keys/release.asc
END
```
2. 安装yum相关依赖
yum -y install yum-plugin-priorities
yum install -y yum-utils snappy leveldb gdiskpython-argparse gperftools-libs ntpdate
yum install ceph-deploy
3. 创建目录作为部署目录，存放key密钥，日志等
cd 
mkdir ceph
4. ceph软件包安装
ceph-deploy install --no-adjust-repos ceph-03
5. 创建ceph集群
ceph-deploy new --cluster-network 10.57.26.0/24  ceph-03
6. 修改ceph.conf，添加参数
```bash
[global]
fsid = 56c894f9-3173-476f-bbd0-169d0c0e86eb
cluster_network = 10.57.26.0/24
mon_initial_members = ceph-03
mon_host = 10.57.26.32
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx
#添加一下参数
osd_pool_default_size = 1
rbd_default_features = 1
```
7. 创建monitor
ceph-deploy mon create ceph-03
8. 为节点准备key
ceph-deploy gatherkeys ceph-03
9. 创建osd
ceph-deploy osd prepare ceph-03:/dev/vdb
10. 激活osd
ceph-deploy osd activate ceph-03:/dev/vdb
11. 允许一主机以管理员权限执行 Ceph 命令
ceph-deploy admin ceph-03
12. 把改过的配置文件分发给集群内各主机
ceph-deploy --overwrite-conf config push ceph-03
13. 创建监控
ceph-deploy mgr create ceph-03
14. 查看mgr状态
netstat -tunlp|grep 7000
15. 开启dashboard
ceph mgr module enable dashboard