---
categories:
- 技术
- 虚拟化&云计算
date: 2018-11-02 13:45:51+08:00
tags:
- docker
thumbnailImage: //www.azheimage.top/markdown-img-paste-20181113165255716.png
title: docker离线安装
---
docker离线安装
<!--more-->

### 安装docker
1. [下载docker](https://download.docker.com/linux/static/stable/x86_64/)，解压docker-18.03.1-ce.tgz 放到用户目录下，并移动到该目录执行下述命令解压二进制包
<!--more-->
`tar xzvf docker-18.03.1-ce.tgz`
2. 将解压出来的 docker 文件所有内容移动到 /usr/bin/ 目录下
`sudo cp docker/* /usr/bin/`
`sudo chown admin:admin /usr/bin/docker*`
3. 新建用户组
`sudo groupadd docker`
4. 将您的用户添加到该docker组。
`sudo usermod -aG docker $USER`
newgrp docker                         #更新用户组
5. 新建启动服务：
sudo vim /usr/lib/systemd/system/docker.service
```
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target

[Service]
Type=notify
# the default is not to use systemd for cgroups because the delegate issues still
# exists and systemd currently does not support the cgroup feature set required
# for containers run by docker
ExecStart=/usr/bin/dockerd \
        --graph /opt/docker
ExecReload=/bin/kill -s HUP $MAINPID
# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
# Uncomment TasksMax if your systemd version supports it.
# Only systemd 226 and above support this version.
#TasksMax=infinity
TimeoutStartSec=0
# set delegate yes so that systemd does not reset the cgroups of docker containers
Delegate=yes
# kill only the docker process, not all processes in the cgroup
KillMode=process
# restart the docker process if it exits prematurely
Restart=on-failure
StartLimitBurst=3
StartLimitInterval=60s
[Install]
WantedBy=multi-user.target
```
sudo sudo chown admin:admin /usr/lib/systemd/system/docker.service


6. 注销并重新登录，以便重新评估您的组成员身份。
7. 创建docker目录：`mkdir /opt/docker`，把/opt/docker目录拥有者改成当前用户
7. 启动docker：
`sudo service docker start`
8. 现在你可以尝试着打印下版本号，试着看看 images，看看 info，看看容器了
### 安装docker-compose
1. 下载[docker-compose](https://github.com/docker/compose/releases/)
2. 拷贝下载好的docker-compose拷贝到/usr/bin
`sudo cp docker-compose-Linux-x86_64 /usr/bin/docker-compose`
3. 给docker-compose加权：
`sudo chmod +x /usr/bin/docker-compose`
4. 查看docker-compose版本：
`docker-compose --version`
