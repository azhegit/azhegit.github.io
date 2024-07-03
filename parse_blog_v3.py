# coding:utf-8

import time, datetime
import os
import yaml, random
import importlib, sys

importlib.reload(sys)

image_urls = set()


def read_urls(filename):
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            for line in f.readlines():
                image_urls.add(line.rstrip("\n"))


def read_yaml(openfile, categ, tag, filename):
    md_context = read_md(openfile)
    # result = ''.join(md_context[0])
    try:
        data = (
            {}
            if len(md_context[0]) == 0
            else yaml.safe_load("".join(md_context[0][1:-1]))
        )
    except:
        print(openfile + "打开失败！")
    # data = {}
    # print(filename)
    # print(filename.replace('.md', ''))
    data["title"] = filename.replace(".md", "")
    # categories = [] if not data.has_key('categories') else data['categories']
    tags = [] if not "tags" in data else data["tags"]

    # if categ not in categories:

    if tag not in tags and tag != "":
        # if tag != '':
        tags.append(tag)

    if "thumbnailImage" in data:
        image_urls.add(data["thumbnailImage"])
    elif len(image_urls) > 0:
        data["thumbnailImage"] = "".join(random.sample(image_urls, 1))

    if not "date" in data:
        data["date"] = time.strftime(
            "%Y-%m-%d %H:%M:%S+08:00", time.localtime(os.stat(openfile).st_birthtime)
        )
    elif tag == "welcome":
        data["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+08:00")

    data["categories"] = categ
    if tags:
        data["tags"] = tags

    # print(yaml.safe_dump(data))

    content = add_more(md_context[1])

    with open(openfile, "w") as f:
        context = yaml.dump(data, allow_unicode=True)
        f.write("---\n" + context + "---\n" + content)


def add_more(content):
    if "<!--more-->" in content:
        return content
    else:
        return (
            "\n".join(content.split("\n")[0:2])
            + "\n<!--more-->\n"
            + "\n".join(content.split("\n")[2:-1])
        )


def read_md(openfile):
    with open(openfile, "r") as f:
        text_lines = f.readlines()
        regex = "---\n"
        # return text_lines[1:7],text_lines[8:]
        if regex in text_lines and text_lines.index(regex) == 0:
            index = text_lines.index(regex, 1)
        else:
            index = -1
            # return text_lines[0:0], ''.join(text_lines[0:])

        return text_lines[0 : index + 1], "".join(text_lines[index + 1 :])


def read(dir):
    update_files = []
    for root, dirs, files in os.walk(dir):
        if files:
            for file in files:
                if file.endswith(".md"):
                    path = root.replace(dir, "")
                    update_file = root + "/" + file
                    if "/" not in path:
                        categorie = [path]
                        tag = ""
                    else:
                        categorie = path.split("/")[0:-1]
                        tag = path.split("/")[-1]

                    read_yaml(update_file, categorie, tag, file)
                    print("已修改:" + update_file)
                    update_files.append(file)

    print("共修改 " + str(len(update_files)) + " 个文件")


def write_urls(filename):
    with open(filename, "w") as f:
        f.write("\n".join(image_urls))


if __name__ == "__main__":
    image_file = "image_urls.txt"
    read_urls(image_file)
    read("content/post/")

    # read('/Users/azhe/BlogGitee/content/post/技术/大数据/test')
    # read('/Users/azhe/BlogGitee/content/post/')
    write_urls(image_file)
