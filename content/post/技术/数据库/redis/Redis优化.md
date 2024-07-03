---
categories:
- 技术
- 数据库
date: '2021-09-14 11:13:04+08:00'
tags:
- redis
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725100954649.png
title: Redis优化
---
Redis优化

1. key设置ttl并且调整删除策略为volatile-ttl
set maxmemory_policy allkeys-lru :volatile-ttl
<!--more-->

- noeviction: 不删除策略, 达到最大内存限制时, 如果需要更多内存, 直接返回错误信息。 大多数写命令都会导致占- 用更多的内存(有极少数会例外, 如 DEL )。
- allkeys-lru: 所有key通用; 优先删除最近最少使用(less recently used ,LRU) 的 key。
- volatile-lru: 只限于设置了 expire 的部分; 优先删除最近最少使用(less recently used ,LRU) 的 key。
- allkeys-random: 所有key通用; 随机删除一部分 key。
- volatile-random: 只限于设置了 expire 的部分; 随机删除一部分 key。
- volatile-ttl: 只限于设置了 expire 的部分; 优先删除剩余时间(time to live,TTL) 短的key。

2. 不保存rdb，设置save ""
3. 设置密码，requirepass jst123
4. 设置最大内存，maxmemory 53687091200
5. redis6支持多线程，不过是socket网络层面，设置CPU的80%，io-threads 20
6. 只当做内存存储，不同步数据，appendfsync no
7. 碎片清理：config set  activedefrag yes
8. 手动清理碎片：memory purge
9. 配置写回文件：config rewrite