#!/usr/bin/env bash
# Linux platform bash file
ssh-add -K ~/.ssh/id_rsa_gitee
echo "正在添加文件..."

if [ $# -gt 0 ]; then
  comment=$1
else
  comment=`date '+%Y-%m-%d %H:%M:%S'`
fi

git add .
git commit -m "$comment"
echo "正在开始提交代码..."
git push origin master
echo "代码提交成功，正在关闭..."
