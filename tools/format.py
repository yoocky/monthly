#!/usr/bin/env python
#-*-coding:utf-8 -*-
import csv
import argparse


parser = argparse.ArgumentParser(description='csv表格转md')
parser.add_argument('--file', '-f', help='csv文件名，必要参数', required=True)
parser.add_argument('--out', '-o', help='输出文件名，必要参数', required=True)
args = parser.parse_args()


# 处理\xef\xbb\xbf 问题
with open(args.file, 'rb') as csvfile:
    content = csvfile.read()
    csvfile.close()

with open(args.file, 'wb') as csvfile:
    csvfile.write(content.replace('\xef\xbb\xbf', ''))
    csvfile.close()

# csv 转成 markdown text
with open(args.file, 'rU') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    markdown = ""
    temp =""
    for row in reader:
        title = row['文章标题']
        desc = row['内容摘要']
        url = row['推荐内容链接']
        filetype = row['类型']
        author = row['推荐人']
        if title:
            # 分类标题
            if filetype in temp:
                print("已有分类")
            else:
                if temp:
                    markdown = markdown + "\n\n --- \n\n"
                markdown = markdown + "> ### %s" %(filetype)
                temp = temp + filetype
            markdown = markdown + "\n\n #### [%s](%s)" %(title, url)
            markdown = markdown + "\n\n %s" %(desc)
            markdown = markdown + "\n\n _推荐人：%s_ \n\n" %(author)
    # print(markdown)
    
# markdown text  输出成文件
filename = args.out
with open(filename, "w") as file:
    file.write(markdown)