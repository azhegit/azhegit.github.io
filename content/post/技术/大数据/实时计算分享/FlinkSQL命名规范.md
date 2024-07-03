---
categories:
- 技术
- 大数据
date: '2022-06-03 23:44:17+08:00'
tags:
- 实时计算分享
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725103847120.png
title: FlinkSQL命名规范
---

ODS
<!--more-->

ods*{业务线名}*{源库名}\_{源表名}[_incre]

rt（realtime）主要是区别于离线数仓，[_incre]可选，增量表标识

DIM

dim*{业务线名}*{源库名}\_{源表名}

dim 是指维度表，交易域表时用 trade 标识

DWD

dwd*{业务线名}*{域名}\_{业务过程名}[_incre]

业务过程是指业务

DWS

dws*{业务线名}*{域名}_{业务描述}_{周期限定}[_incre]

统计周期是指聚合颗粒度，比如 m、d、h、mis 等

ADS

ads*{数据产品名}*[业务线名]_{域名}_{业务过程描述}\_{统计周期}[_incre]