# @Time    : 2022/11/10 14:33
# @Author  : shaowj
# @File    : ads_test_2.py

import ads
import os
import datetime as dt
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

token = 'qQUR0hOBQI4exzCbPqynFtoSjgBN3st1xZQluldp'  # ads上获取的token，每个用户每天搜索次数有限制


def query_counts(keywords, query, year, acknowledgements=False):
    if acknowledgements:
        query = 'ack:' + query
    modifiers = ' '.join([f'year:{year}'])
    full_query = ' '.join([f"abs:('{query}')", modifiers])
    # print(modifiers)
    # print(full_query)
    filter_query = ['database:astronomy',
                    'property:refereed',
                    'doctype:(article OR eprint OR inbook OR inproceedings)']  # 加限制条件的地方，doctype有点坑，要写全
    papers = ads.SearchQuery(q=full_query, fq=filter_query, token=token, rows=2000, sort="citation_count")
    papers.execute()
    results_count = int(papers.response.numFound)  # 先获取文章数量
    # print(count)
    citation_count_num = 0  # 文章总引用量初始化为0
    # print(papers.articles[0].citation_count)

    # ads一次请求rows最大返回2000，所以要做区分，不能忽略2000以外的文章引用量
    if results_count <= 2000:
        for n in papers.articles:
            citation_count_num += n.citation_count
    else:
        rows_1 = 0
        while rows_1 < results_count:
            papers_per_page = ads.SearchQuery(q=full_query, fq=filter_query, token=token, rows=2000, start=rows_1,
                                              sort="citation_count")
            for n in papers_per_page:
                citation_count_num += n.citation_count
            rows_1 += 2000
    print(modifiers, full_query, results_count, citation_count_num)
    return dict(keywords=keywords, query=query, year=year, count=results_count, citation_count_num=citation_count_num)


#  示例 'LAMOST': ['LAMOST', 'lamost', 'Lamost'],好在ads不区分大小写（应该是）
DATA = {
    'LAMOST': ['LAMOST'],
    'SDSS': ['SDSS'],
    'SDSS_Official': ['"BOSS" OR "APOGEE" OR "eBOSS" OR "MARVELS" OR "MANGA" OR "SDSS" OR ("Sloan" AND "Survey")) OR  '
                      'title:("BOSS" OR "APOGEE" OR "eBOSS" OR "MARVELS" OR "MANGA" OR "SDSS" OR ("Sloan" AND '
                      '"Survey")'],
    'SDSS Spectrum': ['SDSS Spectrum'],
}

filename = 'ADS_results2.csv'
years = []
[years.append(str(y)) for y in range(1994, 2023)]
years.append('1994-2022')
# print(years)
if not os.path.exists(filename):
    results = pd.DataFrame([query_counts(keywords, query, year)
                            for keywords, queries in DATA.items()
                            for query in queries
                            for year in years])
    results.to_csv(filename, index=False)

#  绘制
plt.figure(figsize=(10, 6), dpi=100)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False
# 读文件
data = pd.read_csv('ADS_results2.csv')
# print(data.loc['SDSS'])
# 读取指定列
xdata = data.loc[:28, 'year']  # 横坐标 时间是列名
# print(xdata)
# y1data = (data.loc[data['keywords'] == 'SDSS', ['count']])[:-1]  # 多条曲线的y值 参数名为csv的列名
y3data = (data.loc[data['keywords'] == 'SDSS_Official', ['count']])[:-1]  # 多条曲线的y值 参数名为csv的列名
y2data = (data.loc[data['keywords'] == 'SDSS Spectrum', ['count']])[:-1]  # 多条曲线的y值 参数名为csv的列名
y4data = (data.loc[data['keywords'] == 'LAMOST', ['count']])[:-1]  # 多条曲线的y值 参数名为csv的列名

# color可自定义折线颜色，marker可自定义点形状，label为折线标注
# plt.subplot(2, 1, 1)
# plt.plot(xdata, y1data, color='r', mec='r', mfc='w', label=u'SDSS ALL')
plt.plot(xdata, y3data, color='r', mec='r', mfc='w', label=u'SDSS ALL')
plt.plot(xdata, y2data, color='#7B68EE', mec='r', mfc='w', label=u'SDSS Spectrum')
plt.plot(xdata, y4data, color='c', mec='r', mfc='w', label=u'LAMOST')
plt.title(u"论文数趋势图", size=10)
# 其中参数loc用于设置legend的位置，bbox_to_anchor用于在bbox_transform坐标（默认轴坐标）中为图例指定任意位置。
plt.legend(loc=1, bbox_to_anchor=(0.2, 0.95), borderaxespad=0, frameon=False)
plt.xlabel(u'年份', size=10)
# 设置x轴标签旋转角度和字体大小
plt.xticks(rotation=60, fontsize=8)
plt.ylabel(u'论文数', size=10)

# # y11data = (data.loc[data['keywords'] == 'SDSS', ['citation_count_num']])[:-1]  # 多条曲线的y值 参数名为csv的列名
# y33data = (data.loc[data['keywords'] == 'SDSS_Official', ['citation_count_num']])[:-1]  # 多条曲线的y值 参数名为csv的列名
# y22data = (data.loc[data['keywords'] == 'SDSS Spectrum', ['citation_count_num']])[:-1]  # 多条曲线的y值 参数名为csv的列名
# y44data = (data.loc[data['keywords'] == 'LAMOST', ['citation_count_num']])[:-1]  # 多条曲线的y值 参数名为csv的列名
# #
# # color可自定义折线颜色，marker可自定义点形状，label为折线标注
# # plt.subplot(2, 1, 2)
# # plt.plot(xdata, y11data, color='r', mec='r', mfc='w', label=u'SDSS ALL')
# plt.plot(xdata, y33data, color='r', mec='r', mfc='w', label=u'SDSS ALL')
# plt.plot(xdata, y22data, color='#7B68EE', mec='r', mfc='w', label=u'SDSS Spectrum')
# plt.plot(xdata, y44data, color='c', mec='r', mfc='w', label=u'LAMOST')
# plt.title(u"引用数趋势图", size=10)
# # 其中参数loc用于设置legend的位置，bbox_to_anchor用于在bbox_transform坐标（默认轴坐标）中为图例指定任意位置。
# plt.legend(loc=1, bbox_to_anchor=(0.2, 0.95), borderaxespad=0, frameon=False)
# plt.xlabel(u'年份', size=10)
# # 设置x轴标签旋转角度和字体大小
# plt.xticks(rotation=60, fontsize=8)
# plt.ylabel(u'引用数', size=10)

# plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)  # 调整两张子图的距离 不然容易重叠

plt.show()

