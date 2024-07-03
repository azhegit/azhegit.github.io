---
categories:
- 技术
- 数据库
date: 2018-07-24 19:18:38+08:00
tags:
- mysql
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725101125909.png
title: mysql安装
---
在centos7上离线包安装安装，以及mysql包的依赖关系
<!--more-->

#### 手动安装MySQL

1. 卸载mariadb-libs：`rpm -e --nodeps mariadb-libs`
2. 安装mysql-community-common-5.7.22-1.el7.x86_64.rpm
3. 安装mysql-community-libs-5.7.22-1.el7.x86_64.rpm
4. 安装mysql-connector-python-8.0.11-1.el7.x86_64.rpm
5. 安装net-tools-2.0-0.22.20131004git.el7.x86_64.rpm
6. 安装mysql-community-client-5.7.22-1.el7.x86_64.rpm
7. **安装mysql-community-server-5.7.22-1.el7.x86_64.rpm**

#### 图解mysql安装依赖：
![](https://www.azheimage.top/markdown-img-paste-20180725100150545.png)

```mermaid
graph LR

MySQL-sever-->卸载mariadb-libs;
mysql-community-libs-->mysql-community-common;
mysql-community-client-->mysql-community-libs;
MySQL-sever-->mysql-connector-python;
MySQL-sever-->net-tools;
MySQL-sever-->mysql-community-client;

python-backports-ssl_match_hostname-->python-backports;
python-backports-ssl_match_hostname-->python-ipaddress;
python-setuptools-->python-backports-ssl_match_hostname;
python_setup.py_build-->mysql-community-devel-5.7.22-1.el7.x86_64.rpm
gcc-->cpp-4.8.5-28.el7_5.1.x86_64;
gcc-->glibc-devel-2.17-222.el7.x86_64;
glibc-devel-2.17-222.el7.x86_64-->glibc-headers-2.17-222.el7.x86_64;
glibc-headers-2.17-222.el7.x86_64-->kernel-headers-3.10.0-862.9.1.el7.x86_64;
gcc-->libgcc-4.8.5-28.el7_5.1.x86_64;
gcc-->libgomp-4.8.5-28.el7_5.1.x86_64;
cpp-4.8.5-28.el7_5.1.x86_64-->libmpc-1.0.1-3.el7.x86_64;
libmpc-1.0.1-3.el7.x86_64-->mpfr-3.1.1-4.el7.x86_64;

python-devel-->python-2.7.5-69.el7_5.x86_64.rpm;
python-devel-->python-libs-2.7.5-69.el7_5.x86_64.rpm;

python_setup.py_build-->MySQL-sever;
python_setup.py_build-->python-setuptools;
python_setup.py_build-->gcc;
python_setup.py_build-->python-devel;
python_setup.py_install
```

#### 安装中的错误以及解决办法
>sh: mysql_config: 未找到命令
Traceback (most recent call last):
  File "setup.py", line 17, in <module>
    metadata, options = get_config()
  File "/root/MySQL-python-1.2.5/setup_posix.py", line 43, in get_config
    libs = mysql_config("libs_r")
  File "/root/MySQL-python-1.2.5/setup_posix.py", line 25, in mysql_config
    raise EnvironmentError("%s not found" % (mysql_config.path,))
EnvironmentError: mysql_config not found

安装mysql-community-devel-5.7.22-1.el7.x86_64.rpm

>unable to execute gcc: No such file or directory
error: command 'gcc' failed with exit status 1

安装gcc
