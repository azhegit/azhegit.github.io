---
categories:
- 技术
- 开发环境
date: 2018-07-24 19:18:38+08:00
tags:
- Linux
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725102054110.png
title: ansible依赖
---
安装ansible以及其他安装为cdh安装所准备的软件安装
<!--more-->
```
cdh-ansible-resources/
├── abase-ansible
│   ├── PyYAML-3.10-11.el7.x86_64.rpm
│   ├── base-PyYAML
│   │   └── libyaml-0.1.4-11.el7_0.x86_64.rpm
│   ├── base-python-jinja2
│   │   ├── python-babel-0.9.6-8.el7.noarch.rpm
│   │   └── python-markupsafe-0.11-10.el7.x86_64.rpm
│   ├── base-python-paramiko
│   │   ├── base_python2-cryptography
│   │   │   ├── base_python-backports
│   │   │   │   ├── base_python-backports-ssl
│   │   │   │   │   ├── python-backports-1.0-8.el7.x86_64.rpm
│   │   │   │   │   └── python-ipaddress-1.0.16-2.el7.noarch.rpm
│   │   │   │   └── python-backports-ssl_match_hostname-3.5.0.1-1.el7.noarch.rpm
│   │   │   ├── base_python-cffi
│   │   │   │   ├── base_python-pycparser
│   │   │   │   │   └── python-ply-3.4-11.el7.noarch.rpm
│   │   │   │   └── python-pycparser-2.14-1.el7.noarch.rpm
│   │   │   ├── python-cffi-1.6.0-5.el7.x86_64.rpm
│   │   │   ├── python-enum34-1.0.4-1.el7.noarch.rpm
│   │   │   ├── python-idna-2.4-1.el7.noarch.rpm
│   │   │   ├── python-setuptools-0.9.8-7.el7.noarch.rpm
│   │   │   ├── python-six-1.9.0-2.el7.noarch.rpm
│   │   │   └── python2-pyasn1-0.1.9-7.el7.noarch.rpm
│   │   └── python2-cryptography-1.7.2-2.el7.x86_64.rpm
│   ├── python-crypto-2.6.1-1.el7.centos.x86_64.rpm
│   ├── python-jinja2-2.7.2-2.el7.noarch.rpm
│   ├── python-paramiko-2.1.1-4.el7.noarch.rpm
│   └── sshpass-1.06-2.el7.x86_64.rpm
├── abase-expect
│   └── tcl-8.5.13-8.el7.x86_64.rpm
├── abase-httpd
│   ├── apr-1.4.8-3.el7_4.1.x86_64.rpm
│   ├── apr-util-1.5.2-6.el7.x86_64.rpm
│   ├── httpd-tools-2.4.6-80.el7.centos.1.x86_64.rpm
│   └── mailcap-2.1.41-2.el7.noarch.rpm
├── abase-jq
│   └── oniguruma-5.9.5-3.el7.x86_64.rpm
├── abase-ntp
│   ├── autogen-libopts-5.18-5.el7.x86_64.rpm
│   └── ntpdate-4.2.6p5-28.el7.centos.x86_64.rpm
├── abase-vim
│   ├── gpm-libs-1.20.7-5.el7.x86_64.rpm
│   ├── perl-5.16.3-292.el7.x86_64.rpm
│   ├── perl-Carp-1.26-244.el7.noarch.rpm
│   ├── perl-Encode-2.51-7.el7.x86_64.rpm
│   ├── perl-Exporter-5.68-3.el7.noarch.rpm
│   ├── perl-File-Path-2.09-2.el7.noarch.rpm
│   ├── perl-File-Temp-0.23.01-3.el7.noarch.rpm
│   ├── perl-Filter-1.49-3.el7.x86_64.rpm
│   ├── perl-Getopt-Long-2.40-3.el7.noarch.rpm
│   ├── perl-HTTP-Tiny-0.033-3.el7.noarch.rpm
│   ├── perl-PathTools-3.40-5.el7.x86_64.rpm
│   ├── perl-Pod-Escapes-1.04-292.el7.noarch.rpm
│   ├── perl-Pod-Perldoc-3.20-4.el7.noarch.rpm
│   ├── perl-Pod-Simple-3.28-4.el7.noarch.rpm
│   ├── perl-Pod-Usage-1.63-3.el7.noarch.rpm
│   ├── perl-Scalar-List-Utils-1.27-248.el7.x86_64.rpm
│   ├── perl-Socket-2.010-4.el7.x86_64.rpm
│   ├── perl-Storable-2.45-3.el7.x86_64.rpm
│   ├── perl-Text-ParseWords-3.29-4.el7.noarch.rpm
│   ├── perl-Time-HiRes-1.9725-3.el7.x86_64.rpm
│   ├── perl-Time-Local-1.2300-2.el7.noarch.rpm
│   ├── perl-constant-1.27-2.el7.noarch.rpm
│   ├── perl-libs-5.16.3-292.el7.x86_64.rpm
│   ├── perl-macros-5.16.3-292.el7.x86_64.rpm
│   ├── perl-parent-0.225-244.el7.noarch.rpm
│   ├── perl-podlators-2.5.1-3.el7.noarch.rpm
│   ├── perl-threads-1.87-4.el7.x86_64.rpm
│   ├── perl-threads-shared-1.43-6.el7.x86_64.rpm
│   ├── vim-common-7.4.160-4.el7.x86_64.rpm
│   └── vim-filesystem-7.4.160-4.el7.x86_64.rpm
├── ansible-2.6.1-1.el7.ans.noarch.rpm
├── expect-5.45-14.el7_1.x86_64.rpm
├── httpd-2.4.6-80.el7.centos.1.x86_64.rpm
├── jq-1.5-1.el7.x86_64.rpm
├── ntp-4.2.6p5-28.el7.centos.x86_64.rpm
└── vim-enhanced-7.4.160-4.el7.x86_64.rpm
```
