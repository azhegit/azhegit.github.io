---
categories:
- 技术
- 大数据
date: '2021-03-08 16:21:31+08:00'
tags:
- clickhouse
thumbnailImage: //www.azheimage.top/markdown-img-paste-20190110144117219.png
title: clickhouse部署
---
clickhouse 离线安装

单机版及集群版

<!--more-->

## Clickhouse 离线安装

### 安装环境
已有zookeeper集群
- hadoop-dev-1
- hadoop-dev-2
- hadoop-dev-3

目标机器
- hadoop-dev-3
- hadoop-dev-4
- hadoop-dev-5


### 离线安装包
[官方文档](https://clickhouse.tech/docs/zh/getting-started/install/#from-rpm-packages)
[rpm下载地址](https://repo.yandex.ru/clickhouse/rpm/stable/x86_64/)

下载安装包
- [clickhouse-common-static-21.2.2.8-2.x86_64.rpm](https://repo.yandex.ru/clickhouse/rpm/stable/x86_64/clickhouse-common-static-21.2.2.8-2.x86_64.rpm)
- [clickhouse-server-21.2.2.8-2.noarch.rpm](https://repo.yandex.ru/clickhouse/rpm/stable/x86_64/clickhouse-server-21.2.2.8-2.noarch.rpm)
- [clickhouse-client-21.2.2.8-2.noarch.rpm](https://repo.yandex.ru/clickhouse/rpm/stable/x86_64/clickhouse-client-21.2.2.8-2.noarch.rpm)

### 安装
sudo rpm -ivh clickhouse-common-static-21.2.2.8-2.x86_64.rpm
sudo rpm -ivh clickhouse-server-21.2.2.8-2.noarch.rpm
sudo rpm -ivh clickhouse-client-21.2.2.8-2.noarch.rpm

安装后主要目录分布如下表：
- /etc/clickhouse-server ：clickhouse 服务端配置文件目录
- /etc/clickhouse-client ：clickhouse 客户端配置文件目录
- /var/lib/clickhouse ：clickhouse 默认数据目录
- /var/log/clickhouse-server ：clickhouse 默认日志目录
- /etc/init.d/clickhouse-server ：clickhouse 服务端启动脚本

### 启动
sudo clickhouse start
```bash
[admin@hadoop-dev-3 ck-rpms]$ clickhouse-client
ClickHouse client version 21.2.2.8 (official build).
Connecting to localhost:9000 as user default.
Connected to ClickHouse server version 21.2.2 revision 54447.

hadoop-dev-3 :) show databases;

SHOW DATABASES

Query id: 9cb14185-eeda-4e77-b934-fb33885696b6

┌─name────┐
│ default │
│ system  │
└─────────┘

2 rows in set. Elapsed: 0.009 sec.

hadoop-dev-3 :) exit
Happy Chinese new year. 春节快乐!
```

```bash
sudo vim /etc/clickhouse-server/config.xml
放开注释
<!-- <listen_host>::</listen_host> -->
```

### 操作

1. 建表
```sql
CREATE TABLE code_province( \
    state_province        String, \
    province_name         String, \
    create_date           date \
) ENGINE = MergeTree(create_date, (state_province), 8192);
```
2. 创建文件
```bash
cat > code_province.csv << EOF
WA,WA_NAME,2017-12-25
CA,CA_NAME,2017-12-25
OR,OR_NAME,2017-12-25
EOF
```
3. 导入
```bash
clickhouse-client -q "INSERT INTO default.code_province FORMAT CSV" < code_province.csv
```
4. 查询
```shell
hadoop-dev-3 :) select * from code_province

SELECT *
FROM code_province

Query id: c5e1991b-d217-4da7-b638-d0312d5eb7ee
┌─state_province─┬─province_name─┬─create_date─┐
│ CA             │ CA_NAME       │  2017-12-25 │
│ OR             │ OR_NAME       │  2017-12-25 │
│ WA             │ WA_NAME       │  2017-12-25 │
└────────────────┴───────────────┴─────────────┘
3 rows in set. Elapsed: 0.013 sec.
```

### 示例
1. 下载并提取表数据 
curl https://datasets.clickhouse.tech/hits/tsv/hits_v1.tsv.xz | unxz --threads=`nproc` > hits_v1.tsv
curl https://datasets.clickhouse.tech/visits/tsv/visits_v1.tsv.xz | unxz --threads=`nproc` > visits_v1.tsv
提取的文件大小约为10GB。
2. 创建表 
与大多数数据库管理系统一样，ClickHouse在逻辑上将表分组为数据库。包含一个default数据库，但我们将创建一个新的数据库tutorial:

`clickhouse-client --query "CREATE DATABASE IF NOT EXISTS tutorial"`

```sql
CREATE TABLE tutorial.hits_v1
(
    `WatchID` UInt64,
    `JavaEnable` UInt8,
    `Title` String,
    `GoodEvent` Int16,
    `EventTime` DateTime,
    `EventDate` Date,
    `CounterID` UInt32,
    `ClientIP` UInt32,
    `ClientIP6` FixedString(16),
    `RegionID` UInt32,
    `UserID` UInt64,
    `CounterClass` Int8,
    `OS` UInt8,
    `UserAgent` UInt8,
    `URL` String,
    `Referer` String,
    `URLDomain` String,
    `RefererDomain` String,
    `Refresh` UInt8,
    `IsRobot` UInt8,
    `RefererCategories` Array(UInt16),
    `URLCategories` Array(UInt16),
    `URLRegions` Array(UInt32),
    `RefererRegions` Array(UInt32),
    `ResolutionWidth` UInt16,
    `ResolutionHeight` UInt16,
    `ResolutionDepth` UInt8,
    `FlashMajor` UInt8,
    `FlashMinor` UInt8,
    `FlashMinor2` String,
    `NetMajor` UInt8,
    `NetMinor` UInt8,
    `UserAgentMajor` UInt16,
    `UserAgentMinor` FixedString(2),
    `CookieEnable` UInt8,
    `JavascriptEnable` UInt8,
    `IsMobile` UInt8,
    `MobilePhone` UInt8,
    `MobilePhoneModel` String,
    `Params` String,
    `IPNetworkID` UInt32,
    `TraficSourceID` Int8,
    `SearchEngineID` UInt16,
    `SearchPhrase` String,
    `AdvEngineID` UInt8,
    `IsArtifical` UInt8,
    `WindowClientWidth` UInt16,
    `WindowClientHeight` UInt16,
    `ClientTimeZone` Int16,
    `ClientEventTime` DateTime,
    `SilverlightVersion1` UInt8,
    `SilverlightVersion2` UInt8,
    `SilverlightVersion3` UInt32,
    `SilverlightVersion4` UInt16,
    `PageCharset` String,
    `CodeVersion` UInt32,
    `IsLink` UInt8,
    `IsDownload` UInt8,
    `IsNotBounce` UInt8,
    `FUniqID` UInt64,
    `HID` UInt32,
    `IsOldCounter` UInt8,
    `IsEvent` UInt8,
    `IsParameter` UInt8,
    `DontCountHits` UInt8,
    `WithHash` UInt8,
    `HitColor` FixedString(1),
    `UTCEventTime` DateTime,
    `Age` UInt8,
    `Sex` UInt8,
    `Income` UInt8,
    `Interests` UInt16,
    `Robotness` UInt8,
    `GeneralInterests` Array(UInt16),
    `RemoteIP` UInt32,
    `RemoteIP6` FixedString(16),
    `WindowName` Int32,
    `OpenerName` Int32,
    `HistoryLength` Int16,
    `BrowserLanguage` FixedString(2),
    `BrowserCountry` FixedString(2),
    `SocialNetwork` String,
    `SocialAction` String,
    `HTTPError` UInt16,
    `SendTiming` Int32,
    `DNSTiming` Int32,
    `ConnectTiming` Int32,
    `ResponseStartTiming` Int32,
    `ResponseEndTiming` Int32,
    `FetchTiming` Int32,
    `RedirectTiming` Int32,
    `DOMInteractiveTiming` Int32,
    `DOMContentLoadedTiming` Int32,
    `DOMCompleteTiming` Int32,
    `LoadEventStartTiming` Int32,
    `LoadEventEndTiming` Int32,
    `NSToDOMContentLoadedTiming` Int32,
    `FirstPaintTiming` Int32,
    `RedirectCount` Int8,
    `SocialSourceNetworkID` UInt8,
    `SocialSourcePage` String,
    `ParamPrice` Int64,
    `ParamOrderID` String,
    `ParamCurrency` FixedString(3),
    `ParamCurrencyID` UInt16,
    `GoalsReached` Array(UInt32),
    `OpenstatServiceName` String,
    `OpenstatCampaignID` String,
    `OpenstatAdID` String,
    `OpenstatSourceID` String,
    `UTMSource` String,
    `UTMMedium` String,
    `UTMCampaign` String,
    `UTMContent` String,
    `UTMTerm` String,
    `FromTag` String,
    `HasGCLID` UInt8,
    `RefererHash` UInt64,
    `URLHash` UInt64,
    `CLID` UInt32,
    `YCLID` UInt64,
    `ShareService` String,
    `ShareURL` String,
    `ShareTitle` String,
    `ParsedParams` Nested(
        Key1 String,
        Key2 String,
        Key3 String,
        Key4 String,
        Key5 String,
        ValueDouble Float64),
    `IslandID` FixedString(16),
    `RequestNum` UInt32,
    `RequestTry` UInt8
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(EventDate)
ORDER BY (CounterID, EventDate, intHash32(UserID))
SAMPLE BY intHash32(UserID);

CREATE TABLE tutorial.visits_v1
(
    `CounterID` UInt32,
    `StartDate` Date,
    `Sign` Int8,
    `IsNew` UInt8,
    `VisitID` UInt64,
    `UserID` UInt64,
    `StartTime` DateTime,
    `Duration` UInt32,
    `UTCStartTime` DateTime,
    `PageViews` Int32,
    `Hits` Int32,
    `IsBounce` UInt8,
    `Referer` String,
    `StartURL` String,
    `RefererDomain` String,
    `StartURLDomain` String,
    `EndURL` String,
    `LinkURL` String,
    `IsDownload` UInt8,
    `TraficSourceID` Int8,
    `SearchEngineID` UInt16,
    `SearchPhrase` String,
    `AdvEngineID` UInt8,
    `PlaceID` Int32,
    `RefererCategories` Array(UInt16),
    `URLCategories` Array(UInt16),
    `URLRegions` Array(UInt32),
    `RefererRegions` Array(UInt32),
    `IsYandex` UInt8,
    `GoalReachesDepth` Int32,
    `GoalReachesURL` Int32,
    `GoalReachesAny` Int32,
    `SocialSourceNetworkID` UInt8,
    `SocialSourcePage` String,
    `MobilePhoneModel` String,
    `ClientEventTime` DateTime,
    `RegionID` UInt32,
    `ClientIP` UInt32,
    `ClientIP6` FixedString(16),
    `RemoteIP` UInt32,
    `RemoteIP6` FixedString(16),
    `IPNetworkID` UInt32,
    `SilverlightVersion3` UInt32,
    `CodeVersion` UInt32,
    `ResolutionWidth` UInt16,
    `ResolutionHeight` UInt16,
    `UserAgentMajor` UInt16,
    `UserAgentMinor` UInt16,
    `WindowClientWidth` UInt16,
    `WindowClientHeight` UInt16,
    `SilverlightVersion2` UInt8,
    `SilverlightVersion4` UInt16,
    `FlashVersion3` UInt16,
    `FlashVersion4` UInt16,
    `ClientTimeZone` Int16,
    `OS` UInt8,
    `UserAgent` UInt8,
    `ResolutionDepth` UInt8,
    `FlashMajor` UInt8,
    `FlashMinor` UInt8,
    `NetMajor` UInt8,
    `NetMinor` UInt8,
    `MobilePhone` UInt8,
    `SilverlightVersion1` UInt8,
    `Age` UInt8,
    `Sex` UInt8,
    `Income` UInt8,
    `JavaEnable` UInt8,
    `CookieEnable` UInt8,
    `JavascriptEnable` UInt8,
    `IsMobile` UInt8,
    `BrowserLanguage` UInt16,
    `BrowserCountry` UInt16,
    `Interests` UInt16,
    `Robotness` UInt8,
    `GeneralInterests` Array(UInt16),
    `Params` Array(String),
    `Goals` Nested(
        ID UInt32,
        Serial UInt32,
        EventTime DateTime,
        Price Int64,
        OrderID String,
        CurrencyID UInt32),
    `WatchIDs` Array(UInt64),
    `ParamSumPrice` Int64,
    `ParamCurrency` FixedString(3),
    `ParamCurrencyID` UInt16,
    `ClickLogID` UInt64,
    `ClickEventID` Int32,
    `ClickGoodEvent` Int32,
    `ClickEventTime` DateTime,
    `ClickPriorityID` Int32,
    `ClickPhraseID` Int32,
    `ClickPageID` Int32,
    `ClickPlaceID` Int32,
    `ClickTypeID` Int32,
    `ClickResourceID` Int32,
    `ClickCost` UInt32,
    `ClickClientIP` UInt32,
    `ClickDomainID` UInt32,
    `ClickURL` String,
    `ClickAttempt` UInt8,
    `ClickOrderID` UInt32,
    `ClickBannerID` UInt32,
    `ClickMarketCategoryID` UInt32,
    `ClickMarketPP` UInt32,
    `ClickMarketCategoryName` String,
    `ClickMarketPPName` String,
    `ClickAWAPSCampaignName` String,
    `ClickPageName` String,
    `ClickTargetType` UInt16,
    `ClickTargetPhraseID` UInt64,
    `ClickContextType` UInt8,
    `ClickSelectType` Int8,
    `ClickOptions` String,
    `ClickGroupBannerID` Int32,
    `OpenstatServiceName` String,
    `OpenstatCampaignID` String,
    `OpenstatAdID` String,
    `OpenstatSourceID` String,
    `UTMSource` String,
    `UTMMedium` String,
    `UTMCampaign` String,
    `UTMContent` String,
    `UTMTerm` String,
    `FromTag` String,
    `HasGCLID` UInt8,
    `FirstVisit` DateTime,
    `PredLastVisit` Date,
    `LastVisit` Date,
    `TotalVisits` UInt32,
    `TraficSource` Nested(
        ID Int8,
        SearchEngineID UInt16,
        AdvEngineID UInt8,
        PlaceID UInt16,
        SocialSourceNetworkID UInt8,
        Domain String,
        SearchPhrase String,
        SocialSourcePage String),
    `Attendance` FixedString(16),
    `CLID` UInt32,
    `YCLID` UInt64,
    `NormalizedRefererHash` UInt64,
    `SearchPhraseHash` UInt64,
    `RefererDomainHash` UInt64,
    `NormalizedStartURLHash` UInt64,
    `StartURLDomainHash` UInt64,
    `NormalizedEndURLHash` UInt64,
    `TopLevelDomain` UInt64,
    `URLScheme` UInt64,
    `OpenstatServiceNameHash` UInt64,
    `OpenstatCampaignIDHash` UInt64,
    `OpenstatAdIDHash` UInt64,
    `OpenstatSourceIDHash` UInt64,
    `UTMSourceHash` UInt64,
    `UTMMediumHash` UInt64,
    `UTMCampaignHash` UInt64,
    `UTMContentHash` UInt64,
    `UTMTermHash` UInt64,
    `FromHash` UInt64,
    `WebVisorEnabled` UInt8,
    `WebVisorActivity` UInt32,
    `ParsedParams` Nested(
        Key1 String,
        Key2 String,
        Key3 String,
        Key4 String,
        Key5 String,
        ValueDouble Float64),
    `Market` Nested(
        Type UInt8,
        GoalID UInt32,
        OrderID String,
        OrderPrice Int64,
        PP UInt32,
        DirectPlaceID UInt32,
        DirectOrderID UInt32,
        DirectBannerID UInt32,
        GoodID String,
        GoodName String,
        GoodQuantity Int32,
        GoodPrice Int64),
    `IslandID` FixedString(16)
)
ENGINE = CollapsingMergeTree(Sign)
PARTITION BY toYYYYMM(StartDate)
ORDER BY (CounterID, StartDate, intHash32(UserID), VisitID)
SAMPLE BY intHash32(UserID);
```

3. 导入数据

```bash
clickhouse-client --query "INSERT INTO tutorial.hits_v1 FORMAT TSV" --max_insert_block_size=100000 < hits_v1.tsv
clickhouse-client --query "INSERT INTO tutorial.visits_v1 FORMAT TSV" --max_insert_block_size=100000 < visits_v1.tsv
```
现在我们可以检查表导入是否成功:

clickhouse-client --query "SELECT COUNT(*) FROM tutorial.hits_v1"
clickhouse-client --query "SELECT COUNT(*) FROM tutorial.visits_v1"

4. 查询示例 
```sql
SELECT
    StartURL AS URL,
    AVG(Duration) AS AvgDuration
FROM tutorial.visits_v1
WHERE StartDate BETWEEN '2014-03-23' AND '2014-03-30'
GROUP BY URL
ORDER BY AvgDuration DESC
LIMIT 10;

SELECT
    sum(Sign) AS visits,
    sumIf(Sign, has(Goals.ID, 1105530)) AS goal_visits,
    (100. * goal_visits) / visits AS goal_percent
FROM tutorial.visits_v1
WHERE (CounterID = 912887) AND (toYYYYMM(StartDate) = 201403) AND (domain(StartURL) = 'yandex.ru')
```

### ui界面
免安装版本：
http://ui.tabix.io/
输入连接地址
![](https://www.azheimage.top/markdown-img-paste-20210226161601437.png)
查询
![](https://www.azheimage.top/markdown-img-paste-20210226162736785.png)

### 集群安装
三节点配置
```xml
<!-- /etc/clickhouse-server/config.xml -->

<remote_servers>
  <gmall_cluster>
    <!-- 集群名称-->
    <shard>
      <!--集群的第一个分片-->
      <internal_replication>true</internal_replication>
      <replica>
        <!-- 该分片的第一个副本 -->
        <host>hadoop-dev-3</host>
        <port>9000</port>
      </replica>
      <replica>
        <!-- 该分片的第二个副本 -->
        <host>hadoop-dev-4</host>
        <port>9000</port>
      </replica>
    </shard>

    <shard>
      <!--集群的第二个分片-->
      <internal_replication>true</internal_replication>
      <replica>
        <!-- 该分片的第一个副本 -->
        <host>hadoop-dev-5</host>
        <port>9000</port>
      </replica>
    </shard>
  </gmall_cluster>
</remote_servers>

<zookeeper>
  <node index="1">
    <host>hadoop-dev-1</host>
    <port>2181</port>
  </node>

  <node index="2">
    <host>hadoop-dev-2</host>
    <port>2181</port>
  </node>
  <node index="3">
    <host>hadoop-dev-3</host>
    <port>2181</port>
  </node>
</zookeeper>


<macros>
  <shard>01</shard>
  <!-- 不同机器放的分片数不一样 -->
  <replica>rep_1_1</replica>
  <!-- 不同机器放的副本数不一样 -->
</macros>
```

### 设置明文密码
```xml
<!-- /etc/clickhouse-server/users.xml -->

<users>
    <!-- If user name was not specified, 'default' user is used. -->
    <default>
        <password>ck_pwd</password>
    </default>
</users>

```
启动：
clickhouse-client -u default --password ck_pwd

### 设置SHA256密文密码
echo -n "ck_pwd" | openssl dgst -sha256

```xml
<!-- /etc/clickhouse-server/users.xml -->

<users>
    <!-- If user name was not specified, 'default' user is used. -->
    <default>
        <password_sha256_hex>4a9061e2b23bd77c804bab11d1c5fa4940f75c89f0d08ba03c7bac30591e9600</password_sha256_hex>
    </default>
</users>

```


### 卸载
![](https://www.azheimage.top/markdown-img-paste-20210226155520850.png)

```bash
yum makecache fast
yum list installed | grep clickhouse

sudo yum remove -y clickhouse-common-static.x86_64
sudo yum remove -y clickhouse-server.noarch
sudo yum remove -y clickhouse-client.noarch

sudo clickhouse stop
sudo find / -name "*clickhouse*"

/var/log/clickhouse-server
/var/log/clickhouse-server/clickhouse-server.log
/var/log/clickhouse-server/clickhouse-server.err.log
/var/lib/clickhouse
/usr/bin/clickhouse-git-import
/etc/clickhouse-client
/etc/systemd/system/multi-user.target.wants/clickhouse-server.service
/etc/clickhouse-server
/home/admin/.clickhouse-client-history
```

```bash
sudo rm -rf /var/log/clickhouse-server
sudo rm -rf /var/log/clickhouse-server/clickhouse-server.log
sudo rm -rf /var/log/clickhouse-server/clickhouse-server.err.log
sudo rm -rf /var/lib/clickhouse
sudo rm -rf /usr/bin/clickhouse-git-import
sudo rm -rf /etc/clickhouse-client
sudo rm -rf /etc/systemd/system/multi-user.target.wants/clickhouse-server.service
sudo rm -rf /etc/clickhouse-server
sudo rm -rf /home/admin/.clickhouse-client-history

```











