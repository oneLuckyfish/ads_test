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

token = 'qQUR0hOBQI4exzCbPqynFtoSjgBN3st1xZQluldp'


def query_counts(keywords, query, year, acknowledgements=False):
    if acknowledgements:
        query = 'ack:' + query
    modifiers = ' '.join([f'year:{year}'])
    full_query = ' '.join([f"abs:('{query}')", modifiers])
    # print(modifiers)
    # print(full_query)
    filter_query = ['database:astronomy',
                    'property:refereed',
                    'doctype:(article OR eprint OR inbook OR inproceedings)']
    papers = ads.SearchQuery(q=full_query, fq=filter_query, token=token, rows=2000, sort="citation_count")
    papers.execute()
    results_count = int(papers.response.numFound)
    # print(count)
    citation_count_num = 0
    # print(papers.articles[0].citation_count)
    if results_count <= 2000:
        for n in papers.articles:
            citation_count_num += n.citation_count
    else:
        rows_1 = 0
        while rows_1 < results_count:
            papers_per_page = ads.SearchQuery(q=full_query, fq=filter_query, token=token, rows=2000, start=rows_1, sort="citation_count")
            for n in papers_per_page:
                citation_count_num += n.citation_count
            rows_1 += 2000
    print(modifiers, full_query, results_count, citation_count_num)
    return dict(keywords=keywords, query=query, year=year, count=results_count, citation_count_num=citation_count_num)


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
for y in range(1994, 2023):
    years.append(str(y))
years.append('1994-2022')
# print(years)
if not os.path.exists(filename):
    results = pd.DataFrame([query_counts(keywords, query, year)
                            for keywords, queries in DATA.items()
                            for query in queries
                            for year in years])
    results.to_csv(filename, index=False)

# results = pd.read_csv("ADS_results.csv")
# results = results.groupby(['keywords', 'year']).sum().reset_index()
#
# matplotlib.rc('axes', edgecolor='C7')
# fig, ax = plt.subplots()
#
# for name, group in results.groupby('name'):
#     if name in ['LAMOST', 'SDSS', 'SDSS_Official', 'SDSS Spectrum']:
#         continue
#     group.plot.line(x='year', y='pct', ax=ax, label=name, linewidth=3)
#
# ax.set(xlabel='Year of Publication',
#        ylabel='Percent of Publications')
#
# # text annotations
# leg = plt.legend(loc=2, fontsize=16)
# leg.get_frame().set_alpha(0)
# for i, text in enumerate(leg.get_texts()):
#     text.set_color("C" + str(i))
# plt.xlabel("Year of publication", color="C7", size=16)
# plt.ylabel("Percent of publications", color="C7", size=16)
#
# # final layout options
# plt.xticks(np.arange(1995, 2025, 5), color="C7")
# plt.yticks(np.arange(0.0, 0.05, 0.01), color="C7")
# plt.gca().set_xticks(np.arange(1995, 2020, 1), minor=True)
# plt.gca().set_yticks(np.arange(0.0, 0.05, 0.002), minor=True)
# plt.tick_params(which='minor', length=5, color="C7")
# plt.tick_params(which='major', length=10, color="C7")
# plt.gca().xaxis.set_ticks_position("both")
# plt.gca().yaxis.set_ticks_position("both")
# plt.grid(linestyle="dashed", linewidth=0.5)
# plt.ylim(0.00, 0.03)
# plt.tight_layout()
# fig.savefig('ads-languages.png', transparent=True, dpi=300)