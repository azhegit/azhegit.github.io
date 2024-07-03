---
categories:
- 技术
- 开发环境
date: 2018-07-05 16:35:38+08:00
tags:
- git
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110143649189.png
title: 多个git配置
---
一个客户端多个git账号
<!--more-->
## 1. 同样的邮箱生成不一样的rsa
`ssh-keygen -t rsa -C "azheemail@163.com"`
用ssh-keygen命令生成一组新的id_rsa_gitee和id_rsa_gitee.pub
![](https://www.azheimage.top/markdown-img-paste-20180705164353929.png)
## 2.执行ssh-agent让ssh识别新的私钥
因为默认只读取id_rsa，为了让SSH识别新的私钥，需将其添加到SSH agent中：
`ssh-add ~/.ssh/id_rsa_gitee.pub`
![ssh](ssh_id)
如果出现Could not open a connection to your authentication agent的错误，就试着用以下命令：
```
ssh-agent bash
ssh-add ~/.ssh/id_rsa_gitee
```
## 3. 然后配置~/.ssh/config文件（如果没有的话请重新创建一个）
`vim ~/.ssh/config`
```
# 该文件用于配置私钥对应的服务器
# Default github user(azheemail@163.com)
Host gitee
 HostName gitee.com
 User azhegit
 IdentityFile ~/.ssh/id_rsa_gitee

 # second user(zheqing.wang@tongdun.cn)
 # 建一个github别名，新建的帐号使用这个别名做克隆和更新
#gitab server
Host gitlab
 Hostname gitlab.fraudmetrix.cn
 User zheqing.wang
 IdentityFile ~/.ssh/id_rsa

```
## 4. 添加公钥到对应的网站

## 5. 测试
敲命令测试下
```
ssh -T git@gitee
#如果配置正确会提示
Welcome to Gitee.com, 阿哲!

ssh -T git@gitlab
#如果配置正确会提示
Welcome to GitLab, wangzheqing!　
```
#### 如果添加之后还是下载不来代码：`ssh-add -K ~/.ssh/id_rsa_gitee`
#### 或者用局部配置，如果没有局部配置，默认用全局配置否则优先使用局部配置
> cd ~/workspace/github_two/
   git init
   git config  user.name "Your name"
   git config  user.email your_email@gmail.com

## 6. 初始化项目并上传
  1. git init
  2. git remote add origin git@gitee.com:azhegit/SparkDemo.git
  3. git add .
  4. git commit -m 'init'
  5. git push orign master -f
