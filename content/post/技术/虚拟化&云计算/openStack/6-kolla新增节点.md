---
categories:
- 技术
- 虚拟化&云计算
date: '2019-06-10 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-2019011014402315.png
title: 6-kolla新增节点
---
已安装好的环境，通过kolla新增机器节点
<!--more-->
## kolla新增节点
[toc]

1. 修改hosts文件，添加新节点host
2. 添加Docker源
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
3. 添加代理
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
4. 安装docker1.12.6
yum install -y docker-engine-1.12.6 docker-engine-selinux-1.12.6
5. 设置Docker
mkdir /etc/systemd/system/docker.service.d 
```bash
tee /etc/systemd/system/docker.service.d/kolla.conf <<'EOF'
[Service]
MountFlags=shared
EOF
```
6. 重启相关服务
systemctl daemon-reload
systemctl enable docker
systemctl restart docker
7. 开启root远程登录
vim /etc/ssh/sshd_config 
```bash
#PermitRootLogin yes
#改为
PermitRootLogin yes
```
 service sshd restart
8. 部署节点到新增节点免密钥
9. 拷贝镜像到新节点
scp kolla-openstack-Queens-images.tar dataocean-d-030019:~/
10. 加载镜像
docker load <  kolla-openstack-Queens-images.tar
11. 新增节点配置
vim add-compute
```ini
[control]
dataocean-d-030016
dataocean-d-030018
[network]
dataocean-d-030016
dataocean-d-030018
[inner-compute]
[external-compute]
[compute:children]
[compute]
dataocean-d-030016
dataocean-d-030018
#新增
dataocean-d-030019
[monitoring]
dataocean-d-030016
[storage]
dataocean-d-030016
...
```
12. 测试连通
ansible -i add-compute -m ping all
13. 预检查
kolla-ansible -i add-compute prechecks
14. 安装pip
yum install python-pip
15. pip升级docker
pip install -U docker
16. 安装compute
kolla-ansible -i add-compute deploy





### 错误
#### 1. 检查docker sdk报错
>TASK [prechecks : Checking docker SDK version] ****************************************************************************************
skipping: [localhost]
[DEPRECATION WARNING]: Using tests as filters is deprecated. Instead of using `result|failed` use `result is failed`. This feature
will be removed in version 2.9. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
fatal: [dataocean-d-030019]: FAILED! => {"changed": false, "cmd": ["/usr/bin/python", "-c", "import docker; print docker.__version__"]
##### 解决办法
>pip升级docker
pip install -U docker











