---
categories:
- 技术
- 数据库
date: '2018-11-04 13:26:09+08:00'
tags:
- HugeGraph
thumbnailImage: //www.azheimage.top/markdown-img-paste-2018111316554474.png
title: "HUgeGraph-loader\b测试"
---

HugeGraph-Loader 是 Hugegragh 的数据导入组件，负责将普通文本数据转化为图形的顶点和边并批量导入到图形数据库中。

<!--more-->

## HugeGraph-Loader 测试

HugeGraph-Loader 是 Hugegragh 的数据导入组件，负责将普通文本数据转化为图形的顶点和边并批量导入到图形数据库中。

当要批量插入的图数据（包括顶点和边）条数为十亿级别及以下，或者总数据量小于 TB 时，可以采用[HugeGraph-Loader](../quickstart/hugegraph-loader.md)工具持续、高速导入图数据

---

[toc]

### 使用流程

使用 HugeGraph-Loader 的基本流程分为以下几步：

- 编写图模型（schema）
- 准备数据文件
- 编写输入源映射（source）
- 执行导入过程

#### 1 编写图模型（schema）

这一步是一个建模的过程，用户需要对自己已有的数据和想要创建的图模型有一个清晰的构想，然后编写 schema 建立图模型。

#### schema.groovy

```java
// Define schema
schema.propertyKey("id").asLong().ifNotExist().create();
schema.propertyKey("idn").asLong().ifNotExist().create();
schema.propertyKey("node").asText().ifNotExist().create();
schema.propertyKey("nodeType").asInt().ifNotExist().create();
schema.propertyKey("nodeText").asText().ifNotExist().create();
schema.propertyKey("nodeIsBlack").asInt().ifNotExist().create();
schema.propertyKey("nodeScore").asDouble().ifNotExist().create();
schema.propertyKey("groupNum").asLong().ifNotExist().create();
schema.propertyKey("nodeDegree").asInt().ifNotExist().create();
schema.propertyKey("gmtCreated").asText().ifNotExist().create();
schema.propertyKey("gmtModified").asText().ifNotExist().create();
schema.propertyKey("nodeIsWash").asInt().ifNotExist().create();

schema.propertyKey("start_id").asLong().ifNotExist().create();
schema.propertyKey("end_id").asLong().ifNotExist().create();
schema.propertyKey("linkText").asText().ifNotExist().create();
schema.propertyKey("lineage").asText().ifNotExist().create();
schema.propertyKey("linkType").asText().ifNotExist().create();
schema.propertyKey("eventOccurtime").asText().ifNotExist().create();
schema.propertyKey("sourceId").asLong().ifNotExist().create();
schema.propertyKey("targetId").asLong().ifNotExist().create();


schema.vertexLabel("RealNode")
.useCustomizeNumberId()
.properties("id","node", "nodeType", "nodeText", "nodeIsBlack", "nodeScore", "groupNum", "nodeDegree", "gmtCreated", "gmtModified", "nodeIsWash")
.ifNotExist()
.create();


schema.edgeLabel("Relation")
.sourceLabel("RealNode")
.targetLabel("RealNode")
.properties("linkText","gmtCreated","lineage","linkType","eventOccurtime","sourceId","targetId")
.ifNotExist()
.create();
```

#### 2 准备数据文件

目前 HugeGraph-Loader 仅支持本地文件作为数据源，支持的文件格式包括 CSV、TEXT 和 JSON，数据每行的结构需保持一致。

##### 2.1 vertex.csv(顶点数据文件)

```cs
idn,id,node,nodeType,nodeText,nodeIsBlack,nodeScore,groupNum,nodeDegree,gmtCreated,gmtModified,nodeIsWash
0,0,110110199911211700,1,身份证,0,0.0,0,0,2012-01-03 23:50:05,2018-11-19 17:20:04.141,0
1,1,15600007667,4,手机号,0,0.0,1,0,2012-01-03 23:50:05,2018-11-19 17:20:04.141,0
2,2,大沽街70号-3,7,联系地址,0,0.0,2,0,2012-01-03 23:50:05,2018-11-19 17:20:04.141,0
3,3,海口街85号-17,8,工作单位,0,0.0,3,0,2012-01-03 23:50:05,2018-11-19 17:20:04.141,0
4,4,3ht55@yahoo.com,11,email地址,0,0.0,4,0,2012-01-03 23:50:05,2018-11-19 17:20:04.141,0
5,5,62287607050027493,2,付款账号,0,0.0,5,0,2012-01-03 23:50:05,2018-11-19 17:20:04.141,0
6,6,110110199005176300,1,身份证,0,0.0,6,0,2012-01-12 04:26:59,2018-11-19 17:20:04.141,0
7,7,13400005844,4,手机号,0,0.0,7,0,2012-01-12 04:26:59,2018-11-19 17:20:04.141,0
8,8,东海西路130号-11,7,联系地址,0,0.0,8,0,2012-01-12 04:26:59,2018-11-19 17:20:04.141,0
```

##### 2.2 edge.csv(边数据文件)

```cs
start_id,end_id,linkText,gmtCreated,lineage,linkType,eventOccurtime,sourceId,targetId
0,1,2770.00,2018-11-19 17:20:12.043,1->4,poscon,2012-01-03 23:50:05,0,1
6,7,1444.00,2018-11-19 17:20:12.043,1->4,poscon,2012-01-12 04:26:59,6,7
```

#### 3 编写输入源映射（source）

输入源映射文件是`Json`格式，其内容是由多个`VertexSource`和`EdgeSource`块组成，`VertexSource`和`EdgeSource`分别对应某类顶点/边的输入源映射。

##### struct.json

```Json
{
  "vertices": [
{
  "label": "RealNode",
  "input": {
"type": "file",
"path": "vertex.csv",
"format": "CSV",
"charset": "UTF-8"
  },
  "id":"idn"
}
  ],
  "edges": [
{
  "label": "Relation",
  "source": [
"start_id"
  ],
  "target": [
"end_id"
  ],
  "input": {
"type": "file",
"path": "edge.csv",
"format": "CSV",
"charset": "UTF-8"
  }
}
  ]
}
```

`VertexSource`的节点包括：

| 映射文件节点名 | 说明                                       | 是否必填                                                               |
| -------------- | ------------------------------------------ | ---------------------------------------------------------------------- |
| label          | 待导入的顶点数据的`label`                  | 是                                                                     |
| input          | 顶点数据源的信息，当前版本就是源文件的信息 | 是                                                                     |
| id             | 指定文件中的某一列作为顶点的 Id 列         | 当 Id 策略为`CUSTOMIZE`时，必填；当 Id 策略为`PRIMARY_KEY`时，必须为空 |
| mapping        | 将文件列的列名映射为顶点的属性名           | 否                                                                     |

`EdgeSource`的节点包括：

| 映射文件节点名 | 说明                                       | 是否必填                                                                                                                                                                                                          |
| -------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| label          | 待导入的边数据的`label`                    | 是                                                                                                                                                                                                                |
| input          | 顶点数据源的信息，当前版本就是源文件的信息 | 是                                                                                                                                                                                                                |
| source         | 指定文件中的某几列作为顶点的 id 列         | 当源/目标顶点的 Id 策略为 `CUSTOMIZE`时，必须指定文件中的某一列作为顶点的 id 列；当源/目标顶点的 Id 策略为 `PRIMARY_KEY`时，必须指定文件的一列或多列用于拼接生成顶点的 id，也就是说，不管是哪种 Id 策略，此项必填 |
| target         | 选择边的目标顶点的 id 列                   | 与 source 类似，不再赘述                                                                                                                                                                                          |
| mapping        | 将文件列的列名映射为顶点的属性名           | 否                                                                                                                                                                                                                |

> 注意：`VertexSource`的 id 和`EdgeSource`的 source 和 target 填写的都是文件的中原列名，不是 mapping 后的属性名。

当前 HugeGraph-Loader 仅支持本地文件的导入，所以 `input` 只能是 `file` 这一种类型，此时的 `InputSource` 其实就是 `FileSource`。

`FileSource`的节点包括：

| 映射文件节点名 | 说明               | 是否必填 | 默认值或可选值                                                                         | 补充                                                                                                                                     |
| -------------- | ------------------ | -------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| type           | 输入源类型         | 是       | 必须填 file 或 FILE                                                                    |
| path           | 本地文件的绝对路径 | 是       |                                                                                        | 绝对路径                                                                                                                                 |
| format         | 本地文件的格式     | 是       | 可选值为 CSV、TEXT 及 JSON                                                             | 必须大写                                                                                                                                 |
| header         | 文件各列的列名     | 否       |                                                                                        | 如不指定则会以数据文件第一行作为 header；当文件本身有标题且又指定了 header，文件的第一行会被当作普通的数据行；JSON 文件不需要指定 header |
| delimiter      | 文件行的列分隔符   | 否       | `TEXT`文件默认以制表符`"\t"`作为分隔符；`CSV`文件不需要指定，默认以逗号`","`作为分隔符 | `JSON`文件不需要指定                                                                                                                     |
| charset        | 文件的编码字符集   | 否       | 默认`UTF-8`                                                                            |

#### 4 执行导入

准备好图模型、数据文件以及输入源映射关系文件后，接下来就可以将数据文件导入到图数据库中。

### RocksDB:

#### rest-server.properties:

> batch.max_write_ratio=100
> #batch.max_write_threads=16
> batch.max_edges_per_batch=5000
> batch.max_vertices_per_batch=5000

#### hugegraph.properties:

> backend=rocksdb
> serializer=binary
> vertex.tx_capacity=50000
> edge.tx_capacity=50000

```java
Vertices has been imported: 3092934
Edges has been imported: 4999992
-------------------------------------------------
Vertex Results:
	Parse failure vertices   :	0
	Insert failure vertices  :	0
	Insert success vertices  :	3092934
-------------------------------------------------
Edge Results:
	Parse failure edges      :	0
	Insert failure edges     :	0
	Insert success edges     :	4999992
-------------------------------------------------
Time Results:
	Vertex loading time      :	87
	Edge loading time        :	116
	Total loading time       :	204

导入速率：点--3.5W/s 边--4.3W/s
```

### cassandra 单机版:

#### hugegraph.properties:

> backend=cassandra
> serializer=cassandra
> vertex.tx_capacity=50000
> edge.tx_capacity=80000

```java
Vertices has been imported: 3092934
Edges has been imported: 4999992
-------------------------------------------------
Vertex Results:
	Parse failure vertices   :	0
	Insert failure vertices  :	0
	Insert success vertices  :	3092934
-------------------------------------------------
Edge Results:
	Parse failure edges      :	0
	Insert failure edges     :	0
	Insert success edges     :	4999992
-------------------------------------------------
Time Results:
	Vertex loading time      :	296
	Edge loading time        :	1034
	Total loading time       :	1331

导入速率：点--1.1W/s 边--0.5W/s
```

### cassandra 集群版（3 台）:

```java
Vertices has been imported: 3092934
Edges has been imported: 4999992
-------------------------------------------------
Vertex Results:
	Parse failure vertices   :	0
	Insert failure vertices  :	0
	Insert success vertices  :	3092934
-------------------------------------------------
Edge Results:
	Parse failure edges      :	0
	Insert failure edges     :	0
	Insert success edges     :	4999992
-------------------------------------------------
Time Results:
	Vertex loading time      :	321
	Edge loading time        :	365
	Total loading time       :	686

导入速率：点--1.0W/s 边--1.3W/s
```

导入过程由用户提交的命令控制，用户可以通过不同的参数控制执行的具体流程。

##### 参数说明

| 参数                | 默认值        | 是否必传 | 描述信息                                       |
| ------------------- | ------------- | -------- | ---------------------------------------------- |
| -f &#124; --file    |               | Y        | 配置脚本的路径                                 |
| -g &#124; --graph   |               | Y        | 图形数据库空间                                 |
| -s &#124; --schema  |               | Y        | schema 文件路径                                |
| -h &#124; --host    | localhost     |          | HugeGraphServer 的地址                         |
| -p &#124; --port    | 8080          |          | HugeGraphServer 的端口号                       |
| --num-threads       | cpus \* 2 - 1 |          | 导入过程中线程池大小                           |
| --batch-size        | 500           |          | 导入数据时每个批次包含的数据条数               |
| --max-parse-errors  | 1             |          | 最多允许多少行数据解析错误，达到该值则程序退出 |
| --max-insert-errors | 500           |          | 最多允许多少行数据插入错误，达到该值则程序退出 |
| --timeout           | 100           |          | 插入结果返回的超时时间（秒）                   |
| --shutdown-timeout  | 10            |          | 多线程停止的等待时间（秒）                     |
| --retry-times       | 10            |          | 发生特定异常时的重试次数                       |
| --retry-interval    | 10            |          | 重试之前的间隔时间（秒）                       |
| --check-vertex      | false         |          | 插入边时是否检查边所连接的顶点是否存在         |
