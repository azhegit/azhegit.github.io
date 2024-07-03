---
categories:
- 技术
- 开发环境
date: 2019-01-10 15:25:51+08:00
tags:
- hugo
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110153448285.png
title: gitee+hugo方式搭建网站http改为https
---
最近博客经常再打开的时候出现错乱。困扰了很久，终于找到解决的办法了。
<!--more-->
#### 通过hugo生成静态页面文件，push到gitee上之后，访问博客地址,出现页面布局错乱，情况是这样的：

![](https://www.azheimage.top/markdown-img-paste-20190110151349872.png)

#### 并且出现Chrome浏览器提示
![](https://www.azheimage.top/markdown-img-paste-20190110151522714.png)
#### 必须在手动点击加载不安全脚本之后才可以恢复全貌，可是发现图片也会有加载不出来。
原因也是因为我自己使用的七牛云的图床免费的空间，临时域名也不支持https，后来自己注册了一个域名，发现七牛云添加域名必须备案，而备案又需要购买至少三个月的服务器，无奈又去阿里云买了3个月的服务器，域名注册成功之后，七牛云添加了自己的域名，明企鹅开通了https，图片才得以成功显示。
后来发现图片https支持了，可是依然出现不安全的警告
#### 很不舒服。。
通过查看源代码，css样式文件的地址填写还是http，但是文件已经push到gitee上了，已经是https协议了。
![](https://www.azheimage.top/markdown-img-paste-20190110152225932.png)

发现了原因，就是hugo在生成静态文件html中对静态文件的引用地址还是http,而不是https.
罪魁祸首也彻底找到了，去查看hugo的配置文件：config.toml
发现有个参数：baseURL，就是配置静态文件地址，并且有http前缀。改完之后是这样的。
![](https://www.azheimage.top/markdown-img-paste-20190110152826798.png)
重新make。总算生成的页面对静态文件的引用头部改成了上了https
![](https://www.azheimage.top/markdown-img-paste-20190110153027199.png)
### 终于大功告成了，问题解决了
小红锁不见了，警告不存在了，出现的是小绿锁了，页面中的静态文件引用，以及自己的图床也用了自己的域名，换成了https协议
![](https://www.azheimage.top/markdown-img-paste-20190110153206432.png)

#### 页面可以正常访问了，开心，又可以开心的写博客上传了。
![](https://www.azheimage.top/markdown-img-paste-20190110151609843.png)
