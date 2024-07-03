---
categories:
- 技术
- 大数据
date: '2024-07-03 19:59:56+08:00'
tags:
- aws
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180716211711809.png
title: Airflow本机开发环境
---
1. 安装docker
2. 安装docker-compose
3. 下载docker-compose文件
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.2/docker-compose.yaml'
4. 创建文件夹
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=50000" > .env
5. 初始化数据库
docker compose up airflow-init
6. 环境清理（清除环境才需要）
docker-compose down --volumes --remove-orphansdocker-compose.yaml
7. 启动环境
docker compose up
8. 数据库初始化
airflow db init
9. 连接aws密钥创建，需要把.aws文件夹拷贝到docker容器中，并且权限改为Airflow

10. 