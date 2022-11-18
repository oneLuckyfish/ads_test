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

token = '******'


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
