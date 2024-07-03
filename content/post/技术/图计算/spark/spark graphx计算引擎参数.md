---
categories:
- 技术
- 图计算
date: '2019-04-04 14:18:54+08:00'
tags:
- spark
thumbnailImage: //www.azheimage.top/markdown-img-paste-2018111316510833.png
title: spark graphx计算引擎参数
---
为图挖掘及相关的图应用场景提供图算法及模型，用Spark生态圈分布式计算提供OLAP服务
<!--more-->
## 复杂网络计算引擎

### 简介
为图挖掘及相关的图应用场景提供图算法及模型，用Spark生态圈分布式计算提供OLAP服务

### 计算引擎模块：
- 基础模型：度数
- 核心模型：社区分割、风险传播
- 业务模型：关联TopN、异常关联
- 特征图模型：正金字塔、倒金字塔、环形

### 参数传递
##### 参数传递采用命令行方式传参，方便通过执行脚本手动传参执行计算任务，同时也支持后台调用脚本传参的方式执行
###### 目前执行引擎任务提交采用spark-submit方式提交，通过执行指定的提交脚本，往模型入口传递参数。

```bash
EngineParams: 计算引擎模型参数
Usage: EngineParams [options]


基础的数据源参数：
  -S <value> | --srcLabel <value>
        数据源设定开始节点Label，默认值为'RelaNode'
  -L <value> | --linkLabel <value>
        数据源设定关系Label，默认值为'RelaLink'
  -T <value> | --tarLabel <value>
        数据源设定结束节点Label，默认值为'RelaNode'
  -s <value> | --srcNodeType <value>
        数据源设定开始节点属性NodeType，默认值为空
  -l <value> | --linkType <value>
        数据源设定关系属性linkType，默认值为空
  -t <value> | --tarNodeType <value>
        数据源设定结束节点NodeType，默认值为空
  -p <value> | --projectId <value>
        数据源设定项目id，默认值为'-1'
  -r <value> | --rulesId <value>
        数据源设定规则id，默认值为'-2'

节点发散与汇集的参数：
  -d <value> | --minDegree <value>
        数据源设定 金字塔模型 二层最小度数minDegree,默认值为'2'
  -c <value> | --minCount <value>
        数据源设定 金字塔模型 二层最小数量minCount，默认值为'2'

环形算法参数：
  -i <value> | --maxIteratoions <value>
        数据源设定 找环模型 设置最大迭代次数maxIteratoions，默认值为'3'
  --help
        参数格式帮助

```
