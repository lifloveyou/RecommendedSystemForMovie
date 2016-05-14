# -*- coding: utf-8 -*-
import random
import re
import xlrd

from math import *


# 计算皮尔逊相关系数
def similarity_compute(user_movie_list_except_zero_list, system_user_movie_list_except_zero_dict):
    similarity_dict = {}
    total_similarity = 0
    for key, value in system_user_movie_list_except_zero_dict.items():
        sum1, sum2, sum1sq, sum2sq, psum, count = 0, 0, 0, 0, 0, 0
        value_name_temp = []
        for k, v in value.items():
            value_name_temp.append(k)
        for item in user_movie_list_except_zero_list:
            if item[0] in value_name_temp:
                count += 1
                # 求和
                sum1 += item[1]
                sum2 += value[item[0]]
                # 求平方和
                sum1sq += pow(item[1], 2)
                sum2sq += pow(value[item[0]], 2)
                # 求乘积和
                psum += item[1] * value[item[0]]
        if count != 0:
            # 计算皮尔逊评价值
            num = psum - (sum1*sum2/n)
            den = sqrt((sum1sq - pow(sum1, 2)/count)*(sum2sq - pow(sum2, 2)/count))
            if den == 0:
                similarity_dict[key] = 0
            else:
                similarity_dict[key] = num/den
                total_similarity += num/den
    return similarity_dict, total_similarity


if __name__ == "__main__":
    print "*************************"
    print u"*欢迎使用个性化电影推荐系统*"
    print "*************************"
    print u"为了模拟用户真实操作，系统将为您随机分配用户名、为您随机得给系统中的每部电影打分(0代表您未曾看过该影片)"
    print "*************************"
    print u"用户名：王尼玛"
    print "*************************"
    print u"您为系统中的每部电影的打分"
    user_movie_list = []
    user_movie_list_except_zero = []
    user_movie_list_zero = []
    system_user_movie_list_except_zero = {}
    excel = xlrd.open_workbook("MovieScore.xls")
    table = excel.sheet_by_name("DataSheet")
    rows = table.nrows
    cols = table.ncols
    for i in range(rows-1):
        name_pattern = str(table.cell(i+1, 0))
        name = re.findall("'(.*?)'", name_pattern)[0]
        user_movie_list.append((name, random.randrange(2)*round(random.uniform(1, 5), 1)))
    for movie in user_movie_list:
        if movie[1] > 0.0:
            user_movie_list_except_zero.append((movie[0], movie[1]))
        else:
            user_movie_list_zero.append(movie[0])
    for movie in user_movie_list_except_zero:
        print movie[0].decode("raw_unicode_escape"), movie[1]
    print "*************************"
    for m in range(cols-1):
        user_pattern = str(table.cell(0, m+1))
        user = re.findall("'(.*?)'", user_pattern)[0]
        system_user_movie_list_except_zero[user] = {}
        for n in range(rows-1):
            rank_pattern = str(table.cell(n+1, m+1))
            rank = float(rank_pattern.split(":")[1])
            if rank > 0.0:
                name_pattern = str(table.cell(n+1, 0))
                name = re.findall("'(.*?)'", name_pattern)[0]
                system_user_movie_list_except_zero[user][name] = rank
    user_similarity, total_similarity_value = similarity_compute(user_movie_list_except_zero, system_user_movie_list_except_zero)
    synthesize_score = {}
    for m in range(cols-1):
        name_pattern = str(table.cell(m+1, 0))
        name = re.findall("'(.*?)'", name_pattern)[0]
        if name in user_movie_list_zero:
            score_sum = 0
            for n in range(rows-1):
                user_pattern = str(table.cell(0, m+1))
                user = re.findall("'(.*?)'", user_pattern)[0]
                rank_pattern = str(table.cell(n+1, m+1))
                rank = float(rank_pattern.split(":")[1])
                score_sum += user_similarity[user]*rank
            synthesize_score[name] = score_sum/total_similarity_value
    recommended_movie = sorted(synthesize_score.iteritems(), key=lambda x: x[1], reverse=True)[:3]
    print u"系统为您推荐的影片为：%s" % recommended_movie[0][0].decode("raw_unicode_escape")
    print u"推荐度系数为：%.2f" % recommended_movie[0][1]
    print u"系统为您推荐的影片为：%s" % recommended_movie[1][0].decode("raw_unicode_escape")
    print u"推荐度系数为：%.2f" % recommended_movie[1][1]
    print u"系统为您推荐的影片为：%s" % recommended_movie[2][0].decode("raw_unicode_escape")
    print u"推荐度系数为：%.2f" % recommended_movie[2][1]
