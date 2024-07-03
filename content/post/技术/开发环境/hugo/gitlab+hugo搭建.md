---
categories:
- 技术
- 开发环境
date: 2018-06-12 13:45:51+08:00
tags:
- hugo
thumbnailImage: //www.azheimage.top/markdown-img-paste-20181113165255716.png
title: gitlab+hugo搭建
---
gitab+hugo搭建
<!--more-->

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [gitlab+hugo搭建博客](#gitlabhugo搭建博客)
	- [fork examples](#fork-examples)
		- [1. hugo example：https://gitlab.com/pages/hugo](#1-hugo-examplehttpsgitlabcompageshugo)
		- [2. fork](#2-fork)
		- [3. 删除fork链接：Settings-->General-->Advanced settings-->Remove fork relationship](#3-删除fork链接settings-general-advanced-settings-remove-fork-relationship)
		- [4. 修改仓库名称：Settings-->General-->Advanced settings-->Rename repository](#4-修改仓库名称settings-general-advanced-settings-rename-repository)
		- [5. 在线修改一个文件：hugo/content/post/2017-03-20-photoswipe-gallery-sample.md](#5-在线修改一个文件hugocontentpost2017-03-20-photoswipe-gallery-samplemd)
		- [6. 见证奇迹的时候到了，Gitlab CI会自动部署修改的md文件，生成静态页面并且部署](#6-见证奇迹的时候到了gitlab-ci会自动部署修改的md文件生成静态页面并且部署)
		- [7. 查看生成的pages位置：Settings-->pages](#7-查看生成的pages位置settings-pages)
		- [8. 查看页面：https://azhegit.gitlab.io/hugo](#8-查看页面httpsazhegitgitlabiohugo)
		- [9. 修改访问路径成：https://azhegit.gitlab.io](#9-修改访问路径成httpsazhegitgitlabio)
		- [10. 访问：https://azhegit.gitlab.io/](#10-访问httpsazhegitgitlabio)

<!-- /TOC -->
------
# gitlab+hugo搭建博客
## fork examples
### 1. hugo example：https://gitlab.com/pages/hugo
<!--more-->
### 2. fork
![fork](https://www.azheimage.top/dfc52f2e8e7e053b640a2ea83d81cd09.png)
选择fork位置
![fork into](https://www.azheimage.top/9502a5b220e88180c8268888d679bb03.png)
### 3. 删除fork链接：Settings-->General-->Advanced settings-->Remove fork relationship
![remove fork relationship](https://www.azheimage.top/abfa694fd1fdff3cc2d3aa10b33f519b.png)
### 4. 修改仓库名称：Settings-->General-->Advanced settings-->Rename repository
![rename repository](https://www.azheimage.top/71f1b001d460c7343d43ff47fdf9a8fc.png)
### 5. 在线修改一个文件：hugo/content/post/2017-03-20-photoswipe-gallery-sample.md
![update 2017-03-20-photoswipe-gallery-sample.md](https://www.azheimage.top/623b22b997f927dc1b224b68f20048e2.png)
### 6. 见证奇迹的时候到了，Gitlab CI会自动部署修改的md文件，生成静态页面并且部署
正在执行任务
![ci](https://www.azheimage.top/9429651de6d03091147120e388b79a14.png)
docker镜像执行过程
![make pages](https://www.azheimage.top/70c127de528d9fe226fd39718413348c.png)
### 7. 查看生成的pages位置：Settings-->pages
![pages](https://www.azheimage.top/54678af67c0347e5cb701e752729d713.png)
### 8. 查看页面：https://azhegit.gitlab.io/hugo
![修改页面](https://www.azheimage.top/771e039f1b0214694c8918296b4fedb5.png)
### 9. 修改访问路径成：https://azhegit.gitlab.io
![rename path](https://www.azheimage.top/62f7f188d0b9b496d35b9d55122e93a8.png)
### 10. 访问：https://azhegit.gitlab.io/
![](https://www.azheimage.top/94dfde229b81801450e4d36a5e84d2be.png)






![](https://www.azheimage.top/markdown-img-paste-20181114111421841.png)
