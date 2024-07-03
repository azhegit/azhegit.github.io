---
categories:
- 技术
- 大数据
date: '2018-08-13 15:34:13+08:00'
tags:
- cdh
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725100954649.png
title: 如何正确下线CDH机器
---
### 背景
CDH集群有2台机器因为底层存储损坏，无法恢复，机器脱离cdh的管理，数据也没办法再找回来。
![](https://www.azheimage.top/markdown-img-paste-20200813114344408.png)
所以需要在CDH管理剔除。

------------

1. 登录cdh管理平台，主机列表。
2. 执行停止主机上的角色，由于机器宕机，此处跳过
3. 选中要删除的主机，进入维护模式
<!-- 七牛云图片设置大小 -->
![](https://www.azheimage.top/markdown-img-paste-2020081311222625.png?imageView2/2/w/400)
4. 保持默认选项
![](https://www.azheimage.top/markdown-img-paste-20200813115321164.png)
5. 点击进入维护模式，会解除授权
![](https://www.azheimage.top/markdown-img-paste-20200813115126895.png)
6. 此步骤应该是停止cdh-agent，但是由于机器已经宕机，所以此处跳过
7. 选择主机，从cloudera manager删除
![](https://www.azheimage.top/markdown-img-paste-20200813115909789.png?imageView2/2/w/400)

>另一种方式：
停止主机上的角色->从集群中删除->关闭agent->remove from cloudera manager
![](https://www.azheimage.top/markdown-img-paste-20200813120206959.png?imageView2/2/w/400)

