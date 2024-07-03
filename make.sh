#!/bin/bash


function echo_red() {
  echo -e "\033[1;31m[ $* ]\033[0m"
}

theme=`cat config.toml| grep disqusShortname |cut -d = -f 2 | sed 's/\"//g' |sed 's/\ //g'`

if [ ! -d "themes/$theme" ];then
  case $theme in
      "hugo-tranquilpeak-theme")
	  echo_red "$theme 不存在，准备下载"
      git clone https://github.com/kakawait/hugo-tranquilpeak-theme.git themes/hugo-tranquilpeak-theme
          ;;
      *)
      echo "未知主题"
      ;;
  esac
fi

python3 parse_blog.py

hugo --theme=hugo-tranquilpeak-theme
hugo server
