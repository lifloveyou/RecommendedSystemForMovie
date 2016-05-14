# -*- coding: utf-8 -*-
import urllib2

from bs4 import BeautifulSoup


if __name__ == "__main__":
    # 爬虫程序部分
    with open("CrawlDouBanMovie.txt", "w") as fp:
        source_url = "https://movie.douban.com/tag/"
        response_content = urllib2.urlopen(source_url).read()
        soup = BeautifulSoup(response_content, "lxml", from_encoding="utf-8")
        tag_col = soup.find_all(name="table", attrs={"class": "tagCol"})[0]
        for tag in tag_col.find_all(name="a", attrs={"class": "tag"}):
            sub_url = ("https://movie.douban.com" + tag["href"]).encode("utf-8")
            sub_response_content = urllib2.urlopen(sub_url).read()
            sub_soup = BeautifulSoup(sub_response_content, "lxml", from_encoding="utf-8")
            for link_wrapper in sub_soup.find_all(name="div", attrs={"class": "pl2"}):
                title = link_wrapper.find(name="a").get_text().split("/")[0].strip()
                fp.write(title.encode("utf-8")+"\n")
