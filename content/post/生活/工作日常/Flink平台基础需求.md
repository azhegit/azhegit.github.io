---
categories:
- 生活
date: '2022-10-03 22:57:55+08:00'
tags:
- 工作日常
thumbnailImage: //www.azheimage.top/markdown-img-paste-2019011014402315.png
title: Flink平台基础需求
---

Flink 平台基础需求

<!--more-->

1. 支持 SQL 作业、Jar 包作业编辑、历史版本
2. 支持任务运行 Flink UI 入口
3. 支持运维日志查看，包括启动日志，运行日志，任务历史日志
4. 支持手动 Savepoint，并且从指定 savepoint 恢复作业
5. 支持从历史 checkpoint 恢复作业
6. 支持监控信息查看 Jobmanager JMV、Taskmanager、任务级别、状态存储监控项

- 集群资源
  - 资源消耗情况
  - 任务数
- 任务级别：
  - Jobmanager JMV/CPU/Threads/GC
  - Taskmanager JMV/CPU/Threads/GC
  - JobInstance watermark、checkpoint、原生 metric 等
- 状态后端 状态 key 个数、状态 size

7. 支持告警配置
