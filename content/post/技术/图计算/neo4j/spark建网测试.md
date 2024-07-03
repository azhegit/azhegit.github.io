---
categories:
- 技术
- 图计算
date: '2019-01-10 10:37:49+08:00'
tags:
- neo4j
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180831191146955.png
title: spark建网测试
---
neo4j初始化建网，通过MySQL，sparkSQL进行清洗，生成初始化neo4j需要库
<!--more-->

# 初始化建网测试流程
[toc]
### 测试目标
原始数据100万，1000万，1亿建网性能测试

### 测试流程
#### 1. 数据生成：
  MockData模拟生成测试数据
  ##### 数据格式
  ```
  name,cardId,tel,road,companyAddr,email,date,fromBankCard,toBankCard,money
  张龙天,110110198611240000,13100006196,台西纬五路60号-2,吴兴大厦65号-13,g1ot@ask.com,2016-09-10 13:11:12,6228760705002779059,6228760705002776468,9206.00
  漆婷,110110198503300000,15600004433,鱼山广场102号-18,鱼山支街89号-11,4c@ask.com,2017-12-18 04:30:04,6228760705002777167,6228760705002771293,5025.00
  郭策中,110110199703190000,15100009007,沈阳支大厦114号-6,天台路123号-7,6nubl@263.net,2017-10-17 17:36:13,6228760705002776099,6228760705002776797,6093.00
  阳荣琼,110110198206200000,13600008908,宁国二支路107号-20,观海二广场83号-4,ap@sohu.com,2012-09-21 23:46:02,6228760705002772779,6228760705002776934,4466.00
  刘和,110110198902240000,15000004908,福建广场41号-3,湖北街105号-15,nrfz@0355.net,2013-11-09 17:03:12,6228760705002771812,6228760705002771578,5766.00
  ```
#### 2. 数据清洗：
  对生成的数据进行数据清洗，生成node跟link的数据(csv格式)
```sql
-- 建网关系整理：
-- 节点：
--   6种节点 1-身份证号:cardId、4-手机号:tel、7-居住地址(road)、8-单位名称(companyAddr)、9-email，2-fromBankCard
-- 关系整理：
--   5种关系：身份证-手机号，身份证-->居住地址，身份证-->单位名称，身份证-->邮箱，身份证-->付款卡号
```
##### 两种清洗方式
###### 1. 利用MySQL，执行sql语句处理
> ① 100万csv数据导入mysql，导入时间：5分钟
  ② 执行节点清洗的sql，执行时间5分钟
  ![](https://www.azheimage.top/markdown-img-paste-20181016173225147.png)
  ③ 执行关系清洗的sql，执行时间5分钟
  ![](https://www.azheimage.top/markdown-img-paste-20181016173501305.png)
  ④ 节点，关系表数据导出成csv，4943344节点(16.30 sec)，4999998关系(16.30 sec)
**100万数据处理需要15分钟**
###### 2. 编写spark程序，用SparkSQL处理
> ① 上传csv文件到hdfs
  ② spark加载csv文件
  ③ 清洗节点与关系
  ④ 结果数据保存csv文件到hdfs
**1千万数据，spark执行时间：7分1秒213毫秒**
**1亿数据，spark执行时间：执行时间：54分32秒262毫秒**

数据量|数据大小|Spark资源|Spark处理|初始化库时间|Node.csv|link.csv|初始化库
-|-|-|-|-|-|-|-
1千万|1.6G|24Core 80G|7分1秒|5m 12s|1.3G (940万节点)|8.5G (499万关系)|16G (2940万属性)
1亿|16G|27Core 126G|54分32秒|38m 33s|6G (4665万节点)|77G (4.48亿关系)|129G (5.6亿属性)

***比较两种数据处理方式：***
  1. mysql方式不需要依赖其组件，不需要编写程序来执行，可以写SQL进行数据探测，适合**小批量**数据量，但是处理时间**较长**
  2. spark方式依赖大数据组件（hdfs，spark），处理性能对比mysql大幅度提升，推测用spark处理方式可以提升性能**20倍**左右，但是需要编写程序，适合相对稳定的处理逻辑

#### 3. 初始化NEO4J库：
  把csv文件导入到neo4j，建立节点，关系，初始化图数据库
##### 100万数据：
>IMPORT DONE in 1m 48s 893ms.
Imported:
  2451960 nodes
  4992534 relationships
  29423520 properties
Peak memory usage: 1.05 GB
##### 1000万数据：
>IMPORT DONE in 5m 12s 86ms.
Imported:
  9418779 nodes
  49281340 relationships
  113025348 properties
Peak memory usage: 1.12 GB
##### 1亿数据：
>IMPORT DONE in 38m 33s 714ms.
Imported:
  46651360 nodes
  448118100 relationships
  559816320 properties
Peak memory usage: 1.57 GB

spark计算1亿条数据处理资源消耗截图
![](https://www.azheimage.top/markdown-img-paste-20181016152003665.png)
![](https://www.azheimage.top/markdown-img-paste-20181016151740368.png)
![](https://www.azheimage.top/markdown-img-paste-20181016152104739.png)









