# -*- coding: utf-8 -*-
import re

'''
name.txt数据来自互联网
本程序文件从name.txt中提取出姓名数据
'''


if __name__ == "__main__":
    fp = open("name.txt", "r")
    lines = fp.readlines()
    with open("CrawlName.txt", "w") as f:
        for line in lines:
            name = re.findall(u"[\u4e00-\u9fa5]+", line.decode("utf-8"))[0]
            f.write(name.encode("utf-8")+"\n")
