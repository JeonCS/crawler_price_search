#-*- coding: utf-8 -*-

import pandas as pd
# from datalab_search_api import datalab_search_api
from naver_price_crawler import PriceCrawler

if __name__ == "__main__":
    c_pd = pd.read_csv('./data.csv', error_bad_lines=False)
    c_name = c_pd['기업명'].dropna().drop_duplicates().values
    # datalab_search_api(c_name)
    crawler = PriceCrawler("20190925" ,"20160101", c_name)
    crawler.crawl()


