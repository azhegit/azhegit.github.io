---
categories:
- 技术
- 开发环境
date: '2021-08-03 23:50:06+08:00'
tags:
- git
thumbnailImage: //d1u9biwaxjngwg.cloudfront.net/welcome-to-tranquilpeak/city-750.jpg
title: git仓库文件太大
---

git 仓库删除历史大文件

<!--more-->

#### git 项目添加.gitignore 文件很重要

在 git 中增加了一个很大的文件，而且被保存在历史提交记录中，每次拉取代码都很大，速度很慢。而且用删除
提交历史记录的方式不是很实际。

以下分几个步骤介绍如何减小.git 文件夹

#### 以`worklog-realtime`工程为例:

1. 显示 3 个最大的文件 id 列表
   `git rev-list --all | xargs -L1 git ls-tree -r --long | sort -uk3 | sort -rnk4 | head -3`

```bash
100644 blob b3c134b79695d76e25088428158c6b9144fc9dda 154790547	target/worklog-1.0-SNAPSHOT-jar-with-dependencies.jar
100644 blob fec5a75f4093a9d936697a3bbec077d862fe4673 1784190	doc/work_log_realtime_spec.xlsx
100644 blob 5b472a60c2b9c0063d8930a9bc68cb32dd9aeabf 1742210	doc/work_log_realtime_spec.xlsx
```

2. 很明显`target/worklog-1.0-SNAPSHOT-jar-with-dependencies.jar`占用比较大空间
3. 移除大文件
   `git log --pretty=oneline --branches -- target/worklog-1.0-SNAPSHOT-jar-with-dependencies.jar`
4. 删除文件的历史记录
   `git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch  target/worklog-1.0-SNAPSHOT-jar-with-dependencies.jar' -- --all`
5. 提交
   `git push --force --all`
6. 回收空间

```bash
rm -Rf .git/refs/original
rm -Rf .git/logs/
git gc --prune=now
git gc --aggressive --prune=now
```

7. 推送远端
   `git push origin --force --all`
