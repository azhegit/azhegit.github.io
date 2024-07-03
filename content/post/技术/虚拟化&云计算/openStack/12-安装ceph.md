---
categories:
- 技术
- 虚拟化&云计算
date: '2019-07-20 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716211900993.png
title: 12-安装ceph
---
kolla安装ceph
<!--more-->
### kolla安装ceph
1. 上传离线安装的docker依赖及执行脚本
2. ./install-rpms.sh rpms/docker-engine
3. 添加代理上外网
echo '
http_proxy=http://10.57.22.8:3128/
ftp_proxy=http://10.57.22.8:3128/
export http_proxy
export ftp_proxy
https_proxy=http://10.57.22.8:3128/
export https_proxy
' >> /etc/profile

source /etc/profile
curl http://www.baidu.com
4. 配置阿里云的Docker加速器，加快pull registry镜像
mkdir -p /etc/docker
```bash
tee /etc/docker/daemon.json << 'EOF'
{
"registry-mirrors": ["https://a5aghnme.mirror.aliyuncs.com"]
}
EOF
mkdir -p /etc/systemd/system/docker.service.d
tee /etc/systemd/system/docker.service.d/http-proxy.conf << 'EOF'
[Service]
Environment="HTTP_PROXY=http://10.57.22.219:3128/"
EOF
```
重启docker：
systemctl daemon-reload
systemctl restart docker
5. 拉取镜像
docker pull ceph/daemon
6. 准备好一些目录
mkdir -p /etc/ceph
mkdir -p /var/lib/ceph/
7. 创建一个mon


