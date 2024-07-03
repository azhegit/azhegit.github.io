---
categories:
- 技术
- 虚拟化&云计算
date: '2019-06-13 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110144117219.png
title: 9-windows镜像制作
---
windows镜像制作，qcow2格式，提供给OpenStack使用
<!--more-->
[toc]
## windows镜像制作
### 1. 硬件及软件准备

#### 1. 物理机一台
要求支持硬件虚拟化，将centos7安装在物理机上 
#### 2. 下载windows镜像
下载地址：https://msdn.itellyou.cn/
下载cn_windows_server_2012_r2_vl_x64_dvd_2979220.iso
#### 3. 下载virtio-win.iso
下载地址
https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso
或
https://fedoraproject.org/wiki/Windows_Virtio_Drivers#Direct_download
https://docs.fedoraproject.org/en-US/quick-docs/creating-windows-virtual-machines-using-virtio-drivers/index.html 
因为win默认不支持virtio驱动，而通过openstack管理虚拟机是需要virtio驱动的。需要两个virtio驱动，一个是硬盘的，一个是网卡 。
备注：要求对虚拟机进行内存监控，故在模版制作过程中需要安装virtio-balloon驱动
#### 4. 下载cloudbase-init
https://cloudbase.it/cloudbase-init/#download
#### 5. Mac操作环境
#### 6. Mac安装VNC viewer
https://www.realvnc.com/en/connect/download/viewer/

### 2. 环境准备 

#### 1. 检查系统是否支持kvm
egrep "(vmx|svm)" /proc/cpuinfo
支持正常有回显：
![](https://www.azheimage.top/markdown-img-paste-20190611120220539.png)
#### 2. 安装软件包
yum install qemu-kvm qemu-img –y
#### 3. 创建链接
ln -s /usr/libexec/qemu-kvm /usr/bin/kvm
ln -s /usr/bin/qemu-img /usr/bin/kvm-img

### 3. 镜像制作
#### 1. 创建镜像目录，仅windows的iso以及virito文件拷贝到该目录
mkdir win2012
把下载好的文件上传到服务器
![](https://www.azheimage.top/markdown-img-paste-2019061113493969.png)
#### 2. 制作磁盘文件（.qcow2），磁盘大小根据系统需求设定
qemu-img create -f qcow2 win2012.qcow2 20G
#### 3. 给存放镜像及磁盘文件的目录赋权，否则创建云主机时无法打开磁盘文件
chown -R qemu:qemu /root/win2012
#### 4. 启动基于windows7的kvm虚拟机，映射驱动器到vfd软盘
kvm -name win-lh \
-m 2048 \
-cdrom /root/win2012/cn_windows_server_2012_r2_vl_x64_dvd_2979220.iso \
-drive file=/root/win2012/virtio-win-0.1.141.iso,media=cdrom,index=1 \
-drive file=win2012.qcow2,media=disk,index=1,if=virtio,format=qcow2 \
-fda /root/win2012/virtio-win_amd64.vfd \
-boot order=dc,once=d \
-net nic,model=virtio \
-net user -boot c \
-balloon virtio \
-display vnc=:3
>选项解释：
-fda file 使用file作为软盘镜像.我们也可以通过将/dev/fd0作为文件名来使用主机软盘.
-cdrom file 使用文件作为CD-ROM镜像（IDE光盘镜像）
-boot [a|c|d] 由软盘(a),硬盘(c)或是CD-ROM(d).在默认的情况下由硬盘启动
-net nic[,vlan=n][,macaddr=addr] 创建一个新的网卡并与VLAN n
-net user[,vlan=n]  使用用户模式网络堆栈,这样就不需要管理员权限来运行.如果没有指 定-	net选项,这将是默认的情况
-balloon virtio  使用virtio balloon
#### 5. 使用vnc客户端连接kvm安装系统及驱动
1. 输入10.57.30.15:3地址及端口
![](https://www.azheimage.top/markdown-img-paste-20190611140027583.png)
2. 回车，可以看到启动界面
![](https://www.azheimage.top/markdown-img-paste-20190611135948427.png)
3. continue
![](https://www.azheimage.top/markdown-img-paste-20190611140201636.png)
4. 现在安装
![](https://www.azheimage.top/markdown-img-paste-20190611140256840.png)
5. 选择Datacenter（带GUI）
![](https://www.azheimage.top/markdown-img-paste-20190611141001437.png)
![](https://www.azheimage.top/markdown-img-paste-20190611141126246.png)
6. 选择自定义
![](https://www.azheimage.top/markdown-img-paste-20190611141352623.png)
7. 默认识别不了硬件，点击加载驱动程序 
![](https://www.azheimage.top/markdown-img-paste-20190611141525649.png)
8. 确定
![](https://www.azheimage.top/markdown-img-paste-20190611141604353.png)
9. 看到有很多驱动程序，通过浏览选择对应版本的驱动
![](https://www.azheimage.top/markdown-img-paste-20190611142011642.png)
10. 选择对应版本，此次是用的win2012R2镜像安装，所以选择Win2012R2
![](https://www.azheimage.top/markdown-img-paste-2019061114220867.png)
11. 点击下一步
![](https://www.azheimage.top/markdown-img-paste-20190611142820558.png)
12. 下一步，准备安装
![](https://www.azheimage.top/markdown-img-paste-20190611142910902.png)
![](https://www.azheimage.top/markdown-img-paste-20190611143923508.png)
13. 设置用户名密码
![](https://www.azheimage.top/markdown-img-paste-20190611144119766.png)
14. 发送Ctrl+Alt+delete
![](https://www.azheimage.top/markdown-img-paste-20190611144313877.png)
15. 输入设置的密码登录
![](https://www.azheimage.top/markdown-img-paste-20190611144222786.png)
16. 登录成功
![](https://www.azheimage.top/markdown-img-paste-20190611144418452.png)
17. 打开设备管理器，查看磁盘驱动正确
其他设备中有两个驱动需要更新安装
进入“设备管理器” - “系统设备”，安装“以太网控制器”，选择浏览计算机上的设备，在CD中选择对应的windows版本
18. 进入“设备管理器” - “系统设备”，安装“以太网控制器”，选择浏览计算机上的设备，在CD中选择对应的windows版本
![](https://www.azheimage.top/markdown-img-paste-20190612113440429.png)
19. 进入“设备管理器” - “系统设备”，安装“PCI设备”为“Virtio Balloon Driver”
![](https://www.azheimage.top/markdown-img-paste-20190612113453116.png)
![](https://www.azheimage.top/markdown-img-paste-20190612113506315.png)
20. virtio-balloon驱动安装后balloon服务并未安装，需要手动安装：
将virtio-win光驱中的WIN7/X86目录中的blnsvr.exe文件拷贝到“c:/”(系统盘的任意目录)
以管理员身份使用cmd命令行进入上述目录
执行“BLNSVR.exe -i”用以安装BLNSVR服务
![](https://www.azheimage.top/markdown-img-paste-20190612113538580.png)
![](https://www.azheimage.top/markdown-img-paste-20190612113549375.png)
21. 此时查看balloon服务正常运行，且自启动
![](https://www.azheimage.top/markdown-img-paste-20190612113610594.png)
22. 关闭防火墙
![](https://www.azheimage.top/markdown-img-paste-20190612113825687.png)
23. 开启远程连接
![](https://www.azheimage.top/markdown-img-paste-2019061211374509.png)
24. 正常关机保存设置
查看磁盘文件格式并进行格式转换
qemu-img info win2012.qcow2
qemu-img convert -f qcow2 -O qcow2 win2012.qcow2  windowns2012.qcow2
#### 6. 上传制作好的镜像并激活
1. OpenStack界面操作上传镜像好的镜像
2. 创建实例
3. 下载windowns2012激活工具激活
在新建的实例中下载工具并激活，下载地址：http://www.itmop.com/downinfo/168095.html
4. 保存快照
5. 将快照变成镜像
glance image-create --name "windows_server_2012_1" --file 8eb12b73-95ed-404f-89ce-939ff474569f --disk-format qcow2 --container-format bare --protected False --progress  --property visibility="public"











