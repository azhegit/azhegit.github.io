---
categories:
- 技术
- 图计算
date: 2018-08-14 19:18:38+08:00
tags:
- neo4j
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180831191146955.png
title: neo4j-数据导入例子
---
Northwind Graph演示了如何从关系数据库迁移到Neo4j。 转换是迭代和有意识的，强调从关系表到图的节点和关系的概念转变。
<!--more-->

本指南将向您展示如何：
1. 加载：从外部CSV文件创建数据
2. 索引：基于标签的索引节点
3. 相关：将外键引用转换为数据关系
4. 提升：将记录转换为关系

 
### 1. 打开样例
:play northwind-graph

##### 导入商品，品类，供应商
![](https://www.azheimage.top/markdown-img-paste-20180814103043168.png)


### 2. 从网络导入csv格式数据，创建Product标签
```sql
LOAD CSV WITH HEADERS FROM "http://data.neo4j.com/northwind/products.csv" AS row
CREATE (n:Product)
SET n = row,
  n.unitPrice = toFloat(row.unitPrice),
  n.unitsInStock = toInteger(row.unitsInStock), n.unitsOnOrder = toInteger(row.unitsOnOrder),
  n.reorderLevel = toInteger(row.reorderLevel), n.discontinued = (row.discontinued <> "0")
```
##### 商品数据样例：
![](https://www.azheimage.top/markdown-img-paste-20180814102642146.png)

#### 查询product相关的数据，并且以商品id正序返回结果
match (p:Product) return p order by p.productID

### 3. 导入品类数据
```sql
LOAD CSV WITH HEADERS FROM "http://data.neo4j.com/northwind/categories.csv" AS row
CREATE (n:Category)
SET n = row
```

##### 品类数据样例:
![](https://www.azheimage.top/markdown-img-paste-20180814103338144.png)

### 4. 导入供应商数据
```sql
LOAD CSV WITH HEADERS FROM "http://data.neo4j.com/northwind/suppliers.csv" AS row
CREATE (n:Supplier)
SET n = row
```

##### 供应商数据类型：
![](https://www.azheimage.top/markdown-img-paste-20180814103746887.png)

### 5. 创建索引
```sql
CREATE INDEX ON :Product(productID)
CREATE INDEX ON :Category(categoryID)
CREATE INDEX ON :Supplier(supplierID)
```
*索引删除`drop INDEX ON :Product(productID)`*

### 6. 产品目录图
产品，类别和供应商都是通过外键关联，让我们来创建他们之间的关系（relationships），并且构成图
![](https://www.azheimage.top/markdown-img-paste-20180814104321571.png)
```sql
MATCH (p:Product),(c:Category)
WHERE p.categoryID = c.categoryID //创建商品跟品类的关系
CREATE (p)-[:PART_OF]->(c)
```
查看PART_OF的关系：
```sql
MATCH p=()-[r:PART_OF]->() RETURN p
```
![](https://www.azheimage.top/markdown-img-paste-20180814110934213.png)

```sql
MATCH (p:Product),(s:Supplier)
WHERE p.supplierID = s.supplierID //创建商品跟供应商的关系
CREATE (s)-[:SUPPLIES]->(p)
```
查询SUPPLIES的关系:
```sql
MATCH p=()-[r:SUPPLIES]->() RETURN p
```
![](https://www.azheimage.top/markdown-img-paste-20180814111423317.png)

### 7. 查询产品目录图
列出每个供应商提供的产品类别
```sql
MATCH (s:Supplier)-->(:Product)-->(c:Category)
RETURN s.companyName as Company, collect(distinct c.categoryName) as Categories
```
![](https://www.azheimage.top/markdown-img-paste-20180814181635203.png)
找到农产品供应商
```sql
MATCH (c:Category {categoryName:"Produce"})<--(:Product)<--(s:Supplier)
RETURN DISTINCT s.companyName as ProduceSuppliers
```
![](https://www.azheimage.top/markdown-img-paste-20180814181623418.png)

### 8. 导入客户、订单
![](https://www.azheimage.top/markdown-img-paste-20180814181903723.png)
```sql
LOAD CSV WITH HEADERS FROM "http://data.neo4j.com/northwind/customers.csv" AS row
CREATE (n:Customer)
SET n = row
```
![](https://www.azheimage.top/markdown-img-paste-20180814182325166.png)
```sql
LOAD CSV WITH HEADERS FROM "http://data.neo4j.com/northwind/orders.csv" AS row
CREATE (n:Order)
SET n = row
```
![](https://www.azheimage.top/markdown-img-paste-20180814182446902.png)
```sql
//创建索引
CREATE INDEX ON :Customer(customerID)
CREATE INDEX ON :Order(orderID)
//创建数据关系

MATCH (c:Customer),(o:Order) WHERE c.customerID = o.customerID CREATE (c)-[:PURCHASED]->(o)
//请注意，首次创建关系时，您只需要比较这样的属性值
```
### 9. 客户订单图
请注意，订单明细始终是订单的一部分，并且它们将订单与产品相关联 - 它们是连接表。 连接表始终是数据关系的标志，表示两个其他记录之间的共享信息。
在这里，我们将直接将每个OrderDetail记录提升为图中的关系
![](https://www.azheimage.top/markdown-img-paste-20180814182822713.png)
### 10. 建立关系
```sql
LOAD CSV WITH HEADERS FROM "http://data.neo4j.com/northwind/order-details.csv" AS row
MATCH (p:Product), (o:Order)
WHERE p.productID = row.productID AND o.orderID = row.orderID
CREATE (o)-[details:ORDERS]->(p)
SET details = row,
  details.quantity = toInteger(row.quantity)
```
![](https://www.azheimage.top/markdown-img-paste-20180814182947370.png)
### 11. 使用模式查询
```sql
MATCH (cust:Customer)-[:PURCHASED]->(:Order)-[o:ORDERS]->(p:Product),
      (p)-[:PART_OF]->(c:Category {categoryName:"Produce"})
RETURN DISTINCT cust.contactName as CustomerName, SUM(o.quantity) AS TotalProductsPurchased
```
![](https://www.azheimage.top/markdown-img-paste-20180814183140281.png)


**本偏是根据neo4j官方的例子导入数据测试**
