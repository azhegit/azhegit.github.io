---
categories:
- 技术
- 大数据
date: '2022-01-15 23:56:27+08:00'
tags:
- 业务
thumbnailImage: //www.azheimage.top/markdown-img-paste-20181113165255716.png
title: 智能物流业务流程图及useCase
---

# 如何理解智能物流？
<!--more-->

智能物流就是在物流单事前、事中、事后三个关键节点，期间通过大数据分析处理研发多个应用场景，为客户带来更加易用且智能的物流闭环。

## 业务模型图

![](https://www.azheimage.top/markdown-img-paste-20220114142510929.png)

## 业务流程图

### 智能推荐(优先级低)

use case：
问题：KA 客户对物流匹配规则配置复杂，并且无法及时校验规则配置对成本及时效的影响。
优化：用户对运费简单配置，由推荐算法自动推荐不同模式的快递
![](https://www.azheimage.top/markdown-img-paste-20220114144823911.png)

### 物流预警优化(优先级高)

use case：
问题：目前物流预警看板没有主动推送，需要用户主动查看
优化：

1. 优化结果看板的交互
2. 预警订单处理优先级得分
3. 根据风险等级及风险策略主动推送消息，提升用户对看板的粘性
   ![](https://www.azheimage.top/markdown-img-paste-20220114144705999.png)

### 轨迹点查(优先级高)

use case：
问题：目前供应链业务，对物流单轨迹详情查询对接快递 100 第三方查询，存在结果不准确，服务不稳定等
优化：

1. 通过轨迹订阅表实时落库
2. 串联物流轨迹，提供点查
   ![](https://www.azheimage.top/markdown-img-paste-20220114144801639.png)

### 运费成本分析(优先级中)

use case：
问题：GP 快递运费 H+1、部分商家 T+1 产出结果
优化：
离线分析快递运费，分析人员触发计算
![](https://www.azheimage.top/markdown-img-paste-20220114144846557.png)