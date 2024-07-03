---
categories:
- 技术
- 图计算
date: '2019-01-22 10:25:21+08:00'
tags:
- spark
thumbnailImage: //www.azheimage.top/markdown-img-paste-2018111316510833.png
title: spark初始化建网测试报告
---
spark 初始化建网及图计算算法测试
<!--more-->
# 初始化建网测试流程
---------------------
[toc]
-----------------
### 测试目标
原始数据100万、500万、3000万、1亿建网性能测试。
##### 性能测试范围：
1. 数据处理
2. 数据初始化导入图库
3. 社区分割算法
##### 性能测试指标：
- CPU使用占比
- Memory使用量
- 磁盘I/O读写

### 测试流程
#### 1. 数据生成：
测试数据生成以之前给的100万交易数据为基础，根据行方需求复制产生3个级别（500万、3000万、1亿）的数据。
##### 数据格式
|CARD_CLASS|CARD_ATTR|ACPT_INS_ID_CD|MSG_FWD_INS_ID_CD|MSG_RCV_INS_ID_CD|ISS_INS_ID_CD|TFR_IN_CARD_NO|SYS_TRA_NO|ACPT_RESP_CD|TRANS_ID|TRANS_CHNL|CARD_MEDIA|SETTLE_DT|TRANS_AT|TRANS_CURR_CD|CARD_BIN|TFR_DT_TM|LOC_TRANS_TM|LOC_TRANS_DT|MCHNT_TP|POS_ENTRY_MD_CD|RETRI_REF_NO|TERM_ID|MCHNT_CD|TO_TS|TFR_OUT_CARD_NO
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
0|1|1|88020005|49992|1050001|1053410|19623668****1859|929825|0|S31|7|2|20181128|1000|156|19623668147|1128195836|195835|1128|6761|12|7.1916E+11|10000001|1.9801E+12|2018-11-28-19.59.36.505975|19623501****0687
1|1|1|88020005|49992|14411200|14411200|19621021****2714|935322|0|S31|7|2|20181128|200|156|19621021|1128195836|195835|1128|6761|12|7.19159E+11|10000001|1.9801E+12|2018-11-28-19.59.36.535966|19622858****3356
2|1|2|88020005|49992|61000000|61000000|16625919****7|970824|0|S31|7|2|20181128|87914|156|16625919|1128195836|195712|1128|6761|12|7.1916E+11|10000001|1.9801E+12|2018-11-28-19.59.36.155559|19621799****7045
3|1|1|3101022|49992|14293410|14293410|19622858****3356|968320|0|S31|7|1|20181128|100|156|1962285808|1128195836|195828|1128|6761|12|7.19089E+11|469002|3.10102E+14|2018-11-28-19.59.36.731965|19621058****9812

#### 2. 数据处理：
##### 对100万基础数据以及生成的数据进行数据处理，生成银行卡节点及交易关系数据，用于初始化导入。
数据量|原始数据大小|生成节点数据大小|生成关系数据大小|数据处理时间|CPU|Memory(G)|I/O(read/write)
-|-|-|-|-|-|-|-
100万|203M|34M(488,156)|76M(1,799,154)|16秒|11%|1.2|26M/s、10M/s
500万|1015M|34M(488,156)|380M(5,710,129)|51秒|13%|1.8|26M/s、10M/s
3千万|6G|34M(488,156)|2.6G(30,313,040)|4分33秒|12%|2.1|30M/s、11M/s
1亿|20G|34M(488,156)|7.6G(98,604,929)|14分30秒|14.8%|8|32M/s、13M/s

##### 1亿数据处理机器性能图表展示
CPU性能展示：
![](https://www.azheimage.top/markdown-img-paste-20190121132650207.png)
Memory剩余：
![](https://www.azheimage.top/markdown-img-paste-2019012113334923.png)
I/O读：
![](https://www.azheimage.top/markdown-img-paste-20190121133649169.png)
I/O写：
![](https://www.azheimage.top/markdown-img-paste-20190121133733392.png)


#### 3. 初始化图库：
##### 把生成的节点数据、关系数据导入到图数据库，建立节点，关系，初始化图数据库

数据量|图库数据大小|数据处理时间|CPU|Memory(G)|I/O(write)
-|-|-|-|-|-|-|-
100万|203M|6秒|23%|0.8|3M/s
500万|1015M|10秒|32%|3|30M/s
3千万|6G|38秒|63%|4.1|230M/s
1亿|20G|1分秒58秒|85%|8|240M/s

##### 1亿数据导入图库日志：
```bash
IMPORT DONE in 1m 58s 261ms.
Imported:
  487865 nodes
  98604829 relationships
  2439325 properties
Peak memory usage: 1.04 GB
```
##### 1亿数据处理机器性能图表展示
CPU性能展示：
![](https://www.azheimage.top/markdown-img-paste-20190121134922541.png)
Memory剩余：
![](https://www.azheimage.top/markdown-img-paste-20190121135000727.png)
I/O读：
![](https://www.azheimage.top/markdown-img-paste-20190121135053505.png)
I/O写：
![](https://www.azheimage.top/markdown-img-paste-20190121135119969.png)


#### 4. 社区分割算法
数据量|聚类分群处理时间|连通图分群处理时间|CPU|Memory(G)|I/O(write)
-|-|-|-|-|-|-|-
100万|17分2秒|1分10秒|23%|8|5M/s
500万|18分|1分18秒|32%|8|5M/s
3千万|19分15秒|1分17秒|63%|8|5M/s
1亿|20分|1分20秒|85%|8|5M/s
##### 1亿数据处理机器性能图表展示
CPU性能展示：
![](https://www.azheimage.top/markdown-img-paste-20190121135855973.png)
Memory剩余：
![](https://www.azheimage.top/markdown-img-paste-20190121135942501.png)
I/O读：
![](https://www.azheimage.top/markdown-img-paste-2019012114002912.png)
I/O写：
![](https://www.azheimage.top/markdown-img-paste-20190121140127462.png)

##### spark计算1亿条数据处理资源消耗截图
![](https://www.azheimage.top/markdown-img-paste-20190121140410368.png)
![](https://www.azheimage.top/markdown-img-paste-20181016152003665.png)










