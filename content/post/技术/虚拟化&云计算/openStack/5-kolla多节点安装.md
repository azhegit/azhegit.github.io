---
categories:
- 技术
- 虚拟化&云计算
date: '2019-06-09 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716210809882.png
title: 5-kolla多节点安装
---
通过kolla多节点安装部署
<!--more-->
## kolla多节点安装
### ip
|主机|em1|em2|
|-|-|-|
|dataocean-d-030016.te.td|10.57.30.16|10.57.30.161
|dataocean-d-030018.te.td|10.57.30.18|10.57.30.165

### 1. 安装docker(所有机器都需要安装)
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
yum install docker-engine-1.12.6 docker-engine-selinux-1.12.6
4. 设置Docker
mkdir /etc/systemd/system/docker.service.d 
```bash
tee /etc/systemd/system/docker.service.d/kolla.conf <<'EOF'
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
tee /etc/docker/daemon.json << 'EOF'
{
"registry-mirrors": ["https://a5aghnme.mirror.aliyuncs.com"]
}
EOF
```
7. 重启下服务
systemctl daemon-reload &&  systemctl restart docker
8. 加载docker镜像
docker load < kolla-openstack-Queens-images.tar
9. 安装 pip
yum install python-pip
pip install -U pip
10. 安装 Docker python libraries， 否则会报错
pip install -U docker

### 2. 安装kolla（主节点安装）
1. 安装基础软件
yum install python-devel libffi-devel gcc openssl-devel libselinux-python
2. 安装ansible
pip install -U ansible
3. 安装 kolla-ansible
pip install  --ignore-installed -U kolla-ansible
4. 复制相关配置文件
cp -r /usr/share/kolla-ansible/etc_examples/kolla /etc/
cp /usr/share/kolla-ansible/ansible/inventory/* ~/
5. 生成密码文件
kolla-genpwd
6. 编辑密码文件，配置keystone管理员用户的密码。
vim /etc/kolla/passwords.yml
database_password: Td@123
keystone_admin_password: admin
同时，也是登录Dashboard，admin使用的密码，你可以根据自己需要进行修改。
7. 编辑 /etc/kolla/globals.yml 配置文件
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
cp multinode my-multinode
vim my-multinode
```bash
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

[monitoring]
dataocean-d-030016

[storage]
dataocean-d-030016

[deployment]
localhost       ansible_connection=local
.......
```
8. 修改物理网卡的neutron配置（为vlan模式配置）
vim /usr/share/kolla-ansible/ansible/roles/neutron/templates/ml2_conf.ini.j2
![](https://www.azheimage.top/markdown-img-paste-20190603110933366.png)
9. 部署前检查
kolla-ansible prechecks -i my-multinode
10. 部署
kolla-ansible -i my-multinode deploy
11. 销毁
kolla-ansible destroy -i my-multinode --yes-i-really-really-mean-it
12. 生成环境变量
单节点
kolla-ansible post-deploy
多节点
kolla-ansible post-deploy -i /usr/share/kolla-ansible/ansible/inventory/multinode
13. 部署完成后如果需要重新配置
如果修改了/etc/config/[server]/[server].conf
单节点：
kolla-ansible reconfigure 
多节点：
kolla-ansible reconfigure -i /usr/share/kolla-ansible/ansible/inventory/multinode
如果修改了全局配置 /etc/kolla/globals.yml
单节点：
kolla-ansible upgrade
kolla-ansible post-deploy
多节点：
kolla-ansible upgrade -i /usr/share/kolla-ansible/ansible/inventory/multinode
kolla-ansible post-deploy -i /usr/share/kolla-ansible/ansible/inventory/multinode

14. 创建vlan网络

neutron net-create vlan-130 --shared --provider:physical_network physnet1 --provider:network_type vlan --provider:segmentation_id 130
neutron subnet-create vlan-130 10.57.26.0/24 --name provider-130-subnet --gateway 10.57.26.1




### 错误
#### 1. 执行"kolla-ansible prechecks -i my-multinode"报错：No module named docker
>fatal: [dataocean-d-030018]: FAILED! => {"changed": false, "cmd": ["/usr/bin/python", "-c", "import docker; print docker.__version__"], "delta": "0:00:00.160687", "end": "2019-05-31 10:33:01.954268", "failed_when_result": true, "msg": "non-zero return code", "rc": 1, "start": "2019-05-31 10:33:01.793581", "stderr": "Traceback (most recent call last):\n  File \"<string>\", line 1, in <module>\nImportError: No module named docker", "stderr_lines": ["Traceback (most recent call last):", "  File \"<string>\", line 1, in <module>", "ImportError: No module named docker"], "stdout": "", "stdout_lines": []}
##### 解决办法
>在dataocean-d-030018安装pip
yum install python-pip
pip install -U docker

#### 2. 执行"kolla-ansible prechecks -i my-multinode"报错
>TASK [memcached : Get container facts] ************************************************************************************************
fatal: [dataocean-d-030016]: FAILED! => {"changed": false, "module_stderr": "Shared connection to dataocean-d-030016 closed.\r\n", "module_stdout": "Traceback (most recent call last):\r\n  File \"/root/.ansible/tmp/ansible-tmp-1559271675.06-262399488761708/AnsiballZ_kolla_container_facts.py\", line 114, in <module>\r\n    _ansiballz_main()\r\n  File \"/root/.ansible/tmp/ansible-tmp-1559271675.06-262399488761708/AnsiballZ_kolla_container_facts.py\", line 106, in _ansiballz_main\r\n    invoke_module(zipped_mod, temp_path, 
##### 解决办法
>docker 没有启动,重启docker

#### 3. 执行"kolla-ansible prechecks -i my-multinode"报错
>TASK [neutron : Checking if 'MountFlags' for docker service is set to 'shared'] *********
fatal: [dataocean-d-030016]: FAILED! => {"changed": false, "cmd": ["systemctl", "show", "docker"], "delta": "0:00:00.115063", "end": "2019-05-31 11:18:09.555517", "failed_when_result": true, "rc": 0, "start": "2019-05-31 11:18:09.440454", "stderr": ""
##### 解决办法
>设置Docker
mkdir /etc/systemd/system/docker.service.d 
tee /etc/systemd/system/docker.service.d/kolla.conf <<'EOF'
[Service]
MountFlags=shared
EOF
systemctl daemon-reload &&  systemctl restart docker

#### 4. 创建的虚拟机宿主机连接不上
##### 解决办法
项目--网络--安全组，修改default管理规则，新增2个管理规则
![](https://www.azheimage.top/markdown-img-paste-20190531192203835.png)

#### 5. 网络创建不了
![](https://www.azheimage.top/markdown-img-paste-20190530133246391.png)
##### 解决办法
![](https://www.azheimage.top/markdown-img-paste-2019060411225204.png)







