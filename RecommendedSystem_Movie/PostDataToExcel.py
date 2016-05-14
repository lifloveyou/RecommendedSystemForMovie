# -*- coding: utf-8 -*-
import random
import xlwt


if __name__ == '__main__':
    excel = xlwt.Workbook()
    sheet = excel.add_sheet('DataSheet', cell_overwrite_ok=True)
    fp = open("CrawlName.txt", "r")
    name_list = [name.strip() for name in fp.readlines()]
    total_name = len(name_list)
    fp.close()
    for j in range(total_name):
        sheet.write(0, j+1, name_list[j].decode("utf-8"))
    fp = open("CrawlDouBanMovie.txt", "r")
    movie_list = [movie.strip() for movie in fp.readlines()]
    movie_list = list(set(movie_list))
    total_movie = len(movie_list)
    fp.close()
    for j in range(total_movie):
        sheet.write(j+1, 0, movie_list[j].decode("utf-8"))
    for m in range(total_movie):
        for n in range(total_name):
            # 为每个用户随机分配对一部电影的评分，0代表没看过该部电影，评分在1-5之间，取一位小数
            sheet.write(m+1, n+1, random.randrange(2)*round(random.uniform(1, 5), 1))
    excel.save("MovieScore.xls")
