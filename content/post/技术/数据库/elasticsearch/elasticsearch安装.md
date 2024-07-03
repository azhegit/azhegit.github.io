---
categories:
- 技术
- 数据库
date: 2018-07-13 15:18:38+08:00
tags:
- databases
- elasticsearch
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716210809882.png
title: elasticsearch安装
---
Elasticsearch 是一个分布式的 RESTful 风格的搜索和数据分析引擎，能够解决不断涌现出的各种用例。作为 Elastic Stack 的核心，它集中存储您的数据，帮助您发现意料之中以及意料之外的情况。

ES Logo：
![](https://www.azheimage.top/markdown-img-paste-20180713202251257.png)
<!--more-->
elasticsearch下载地址：
https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.2.tar.gz



## 解压

修改vim config/elasticsearch.yml

```
cluster.name: my-application
node.name: node-1
path.data: /data01/elasticsearch-5.6.2/data
path.logs: /data01/elasticsearch-5.6.2/logs
```

前台启动bin/elasticsearch，后台启动：bin/elasticsearch -d
![](https://www.azheimage.top/markdown-img-paste-20180713204040741.png)
`curl -XGET localhost:9200`
![](https://www.azheimage.top/markdown-img-paste-20180713204111197.png)
