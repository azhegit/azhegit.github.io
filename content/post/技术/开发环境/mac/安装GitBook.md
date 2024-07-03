---
categories:
- 技术
- 开发环境
date: 2018-06-08 13:30:51+08:00
tags:
- mac
thumbnailImage: //www.azheimage.top/markdown-img-paste-2019011014402315.png
title: 安装GitBook
---
1. 查看本机node环境：`node -v`
> localhost:~ azhe$ node -v
v10.5.0
2. 安装gitbook:`sudo npm install gitbook-cli -g`
![](https://www.azheimage.top/markdown-img-paste-20190131164113325.png)
3. 查看gitbook版本:`gitbook -V`
>localhost:~ azhe$ gitbook -V
CLI version: 2.3.2
GitBook version: 3.2.3
4. 初始化gitbook目录:`gitbook init`
![](https://www.azheimage.top/markdown-img-paste-20190131164429473.png)
5. 启动:`gitbook serve -p 8080`
