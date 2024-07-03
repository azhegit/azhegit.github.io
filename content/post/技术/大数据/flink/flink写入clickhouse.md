---
categories:
- 技术
- 大数据
date: '2021-03-11 20:41:31+08:00'
tags:
- flink
thumbnailImage: //www.azheimage.top/markdown-img-paste-2018111316510833.png
title: flink写入clickhouse
---
flink写入clickhouse

flink及clickhouse官方都是没有提供flink写clickhouse的SQL API
<!--more-->
## Flink 写入clickhouse

### ClickHouse 建表
```sql
DROP TABLE IF EXISTS dev.person_score;

CREATE TABLE IF NOT EXISTS dev.person_score
(
    `pid` UInt8, 
    `name` String, 
    `age` UInt8,
    `score` UInt8,
    `create_time` datetime DEFAULT now()
)
ENGINE = TinyLog();

insert into person_score(`pid`,`name`,`age`,`score`) VALUES(0,'test',66,100)

select * from person_score;
```

#### SQL-Client DataGen建表语句
```sql
-- 删除表定义
drop table if exists person_score_datagen;

-- 创建表定义
CREATE TABLE if not exists person_score_datagen (
	id INT, 
	name STRING, 
	age INT,
	score INT,
	ts AS LOCALTIMESTAMP, 
	WATERMARK FOR ts AS ts ) 
WITH (
	'connector' = 'datagen',
-- 	每秒生成的行数：2
	'rows-per-second' = '2',
-- 	字段id选用序列生成器
	'fields.id.kind' = 'sequence',
	'fields.id.start' = '1',
	'fields.id.end' = '20',
-- 	随机生成器生成字符的长度：6
	'fields.name.length' = '6',
	'fields.age.min' = '20',
	'fields.age.max' = '30',
-- 	随机生成器的最小值：1
	'fields.score.min' = '60',
-- 	随机生成器的最大值：100
	'fields.score.max' = '100'
);

select * from person_score_datagen;
```

### Flink sql-client
```sql
drop table if exists person_score_ck;

CREATE TABLE if not exists person_score_ck (
    pid INT,
    name VARCHAR,
    age INT,
    score INT
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:clickhouse://hadoop-dev-3:8123/dev',
    'table-name' = 'person_score',
    'driver' = 'ru.yandex.clickhouse.ClickHouseDriver',
    'username' = 'default',
    'password' = 'ck_pwd',
    'lookup.cache.max-rows' = '5',
    'lookup.cache.ttl' = '10s'
);


```

### Flink SQL 支持 写 ClickHouse
flink及clickhouse官方都是没有提供flink写clickhouse的SQL API，对于DataStream API是可以通过clickhouse-jdbc，自定义SourceFunction、RichSinkFunction去读写clickhouse，相对比较简单。

#### DataStream API
- SourceFunction
自己实现了一个数据模拟生成器的SourceFunction
```java
import java.util.List;
import org.apache.flink.streaming.api.functions.source.SourceFunction;

/**
 * Created by azhe on 2021-03-09 15:42
 */
public class CustomerSource implements SourceFunction<DefaultEntity> {

  private List list;

  public CustomerSource(int recordSize) {
    this.list = MockEntitys.mockDefault(recordSize);
  }

  int index = 0;
  Boolean isRunning = true;

  @Override
  public void run(SourceContext<DefaultEntity> ctx) throws Exception {

    while (isRunning&&index<list.size()) {
      DefaultEntity obj = (DefaultEntity)list.get(index);
      ctx.collect(obj);
      index += 1;
      Thread.sleep(1000);
    }
  }

  @Override
  public void cancel() {

    isRunning = false;
  }
}
```
- RichSinkFunction
实现SinkFunction将DataStream数据输出到clickhouse，数据格式没有做通用的，需要根据数据格式定制化编写，不够灵活。
```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;

/**
 * Created by azhe on 2021-03-09 17:40
 */
public class ClickHouseSink extends RichSinkFunction<DefaultEntity> {
  Connection connection = null;

  String sql;

  public ClickHouseSink(String sql) {
    this.sql = sql;
  }

  @Override
  public void open(Configuration parameters) throws Exception {
    super.open(parameters);
    connection = ClickHouseUtil.getConn();
  }

  @Override
  public void close() throws Exception {
    super.close();
    if (connection != null) {
      connection.close();
    }
  }

  @Override
  public void invoke(DefaultEntity defaultEntity, Context context) throws Exception {
    PreparedStatement preparedStatement = connection.prepareStatement(sql);
    preparedStatement.setLong(1, defaultEntity.getId());
    preparedStatement.setString(2, defaultEntity.getName());
    preparedStatement.addBatch();

    long startTime = System.currentTimeMillis();
    int[] ints = preparedStatement.executeBatch();
    connection.commit();
    long endTime = System.currentTimeMillis();
    System.out.println("批量插入完毕用时：" + (endTime - startTime) + " -- 插入数据 = " + ints.length);
  }
}
```

#### SQL API
根据官方提供的JDBC连接器改造，修改源码，支持Clickhouse，目前是根据flink_2.11-1.12.0版本重新编译
- ClickHouseDialect
```java
package org.apache.flink.connector.jdbc.dialect;

import org.apache.flink.connector.jdbc.internal.converter.ClickHouseRowConverter;
import org.apache.flink.connector.jdbc.internal.converter.JdbcRowConverter;
import org.apache.flink.table.types.logical.LogicalTypeRoot;
import org.apache.flink.table.types.logical.RowType;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

/** JDBC dialect for ClickHouse Created by azhe on 2021-03-10 20:43 . */
public class ClickHouseDialect extends AbstractDialect {

    private static final long serialVersionUID = 1L;

    // Define MAX/MIN precision of TIMESTAMP type according to Mysql docs:
    // https://dev.mysql.com/doc/refman/8.0/en/fractional-seconds.html
    private static final int MAX_TIMESTAMP_PRECISION = 6;
    private static final int MIN_TIMESTAMP_PRECISION = 1;

    // Define MAX/MIN precision of DECIMAL type according to Mysql docs:
    // https://dev.mysql.com/doc/refman/8.0/en/fixed-point-types.html
    private static final int MAX_DECIMAL_PRECISION = 65;
    private static final int MIN_DECIMAL_PRECISION = 1;

    @Override
    public int maxDecimalPrecision() {
        return MAX_DECIMAL_PRECISION;
    }

    @Override
    public int minDecimalPrecision() {
        return MIN_DECIMAL_PRECISION;
    }

    @Override
    public int maxTimestampPrecision() {
        return MAX_TIMESTAMP_PRECISION;
    }

    @Override
    public int minTimestampPrecision() {
        return MIN_TIMESTAMP_PRECISION;
    }

    @Override
    public String dialectName() {
        return "ClickHouse";
    }

    @Override
    public boolean canHandle(String url) {
        return url.startsWith("jdbc:clickhouse:");
    }

    @Override
    public JdbcRowConverter getRowConverter(RowType rowType) {
        return new ClickHouseRowConverter(rowType);
    }

    @Override
    public Optional<String> defaultDriverName() {
        return Optional.of("ru.yandex.clickhouse.ClickHouseDriver");
    }

    @Override
    public String quoteIdentifier(String identifier) {
        return "`" + identifier + "`";
    }

    @Override
    public Optional<String> getUpsertStatement(
            String tableName, String[] fieldNames, String[] uniqueKeyFields) {
        return Optional.of(getInsertIntoStatement(tableName, fieldNames));
    }

    @Override
    public List<LogicalTypeRoot> unsupportedTypes() {
        // The data types used in Mysql are list at:
        // https://dev.mysql.com/doc/refman/8.0/en/data-types.html

        // TODO: We can't convert BINARY data type to
        //  PrimitiveArrayTypeInfo.BYTE_PRIMITIVE_ARRAY_TYPE_INFO in
        // LegacyTypeInfoDataTypeConverter.
        return Arrays.asList(
                LogicalTypeRoot.BINARY,
                LogicalTypeRoot.TIMESTAMP_WITH_LOCAL_TIME_ZONE,
                LogicalTypeRoot.TIMESTAMP_WITH_TIME_ZONE,
                LogicalTypeRoot.INTERVAL_YEAR_MONTH,
                LogicalTypeRoot.INTERVAL_DAY_TIME,
                LogicalTypeRoot.ARRAY,
                LogicalTypeRoot.MULTISET,
                LogicalTypeRoot.MAP,
                LogicalTypeRoot.ROW,
                LogicalTypeRoot.DISTINCT_TYPE,
                LogicalTypeRoot.STRUCTURED_TYPE,
                LogicalTypeRoot.NULL,
                LogicalTypeRoot.RAW,
                LogicalTypeRoot.SYMBOL,
                LogicalTypeRoot.UNRESOLVED);
    }
}
```
- JdbcDialects
```java
package org.apache.flink.connector.jdbc.dialect;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

/** Default JDBC dialects. */
public final class JdbcDialects {

    private static final List<JdbcDialect> DIALECTS =
            Arrays.asList(
                    new DerbyDialect(),
                    new MySQLDialect(),
                    new PostgresDialect(),
                    //  增加ClickHouseDialect
                    new ClickHouseDialect());

    /** Fetch the JdbcDialect class corresponding to a given database url. */
    public static Optional<JdbcDialect> get(String url) {
        for (JdbcDialect dialect : DIALECTS) {
            if (dialect.canHandle(url)) {
                return Optional.of(dialect);
            }
        }
        return Optional.empty();
    }
}
```
- ClickHouseRowConverter
```java
package org.apache.flink.connector.jdbc.internal.converter;

import org.apache.flink.table.types.logical.RowType;

/** Created by azhe on 2021-03-10 21:04 . */
public class ClickHouseRowConverter extends AbstractJdbcRowConverter {

    private static final long serialVersionUID = 1L;

    @Override
    public String converterName() {
        return "ClickHouse";
    }

    public ClickHouseRowConverter(RowType rowType) {
        super(rowType);
    }
}
```
然后就是编译运行。

### SQL-Client 插入数据到ClickHouse
```sql

INSERT INTO person_score_ck SELECT 2,'test2',30,80;

insert into person_score_ck
SELECT id as pid, name, age, score FROM person_score_datagen;
```










