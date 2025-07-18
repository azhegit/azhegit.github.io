---
categories:
- 技术
- 大数据
date: '2023-07-15 19:59:58+08:00'
tags:
- aws
- airflow
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725101125909.png
title: airflow
---

pip 依赖安装
pip install apache-airflow -i https://pypi.douban.com/simple

<!--more-->

pip install apache-airflow-providers-amazon

airflow 数据库初始化
初始化的 Airflow 元数据数据库（如果您的 DAG 使用 XCom 等元数据数据库的元素）。Airflow 元数据数据库是在 Airflow 首次在环境中运行时创建的。您可以使用 检查它是否存在 airflow db check 并使用 初始化新数据库 airflow db init。
airflow db init

Airflow 本机安装
https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

1. 安装 docker（省略）
2. 在安装目录下载 Airflow 使用的 docker-compose 配置文件
   curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.3/docker-compose.yaml'
3. 在安装目录创建目录
   mkdir -p ./dags ./logs ./plugins ./config
4. 创建 uid 文件，手动修改为 AIRFLOW_UID=50000
   echo -e "AIRFLOW_UID=$(id -u)" > .env
5. 初始化 Airflow
   docker compose up airflow-init
6. 启动 Airflow
   docker compose up
7. 查看 Airflow 情况命令
   docker compose run airflow-worker airflow info
8. 也可以下载执行脚本
   curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.3/airflow.sh'
   chmod +x airflow.sh
9. 然后可以使用脚本相关命令
   ./airflow.sh info
   ./airflow.sh bash
   ./airflow.sh python

下载：pip install apache-airflow-providers-amazon

https://docs.aws.amazon.com/zh_tw/mwaa/latest/userguide/connections-packages.html#connections-packages-table-243
https://github.com/aws/aws-mwaa-local-runner/blob/v2.4.3/docker/config/mwaa-base-providers-requirements.txt
https://airflow.apache.org/docs/apache-airflow-providers-amazon/6.0.0/
https://pypi.org/project/apache-airflow-providers-amazon/6.0.0/
mwaa2.4.1 版本 pip 依赖

```
apache-airflow-providers-amazon==6.0.0
apache-airflow-providers-celery==3.0.0
apache-airflow-providers-common-sql==1.2.0
apache-airflow-providers-ftp==3.1.0
apache-airflow-providers-http==4.0.0
apache-airflow-providers-imap==3.0.0
apache-airflow-providers-postgres==5.2.2
apache-airflow-providers-sqlite==3.2.1
```
