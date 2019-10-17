#-*- coding: utf-8 -*-

from datetime import datetime
from crawler import Crawler
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool, current_process
from datetime import datetime, timedelta
import pandas as pd
import requests
import re
import os

cpu_count = os.cpu_count() -1

class PriceCrawler(Crawler):
    dtype = 'price'
    source = 'https://finance.naver.com/item/sise_day.nhn'

    def __init__(self, sdate, edate, crawl_list):
        super().__init__(sdate, edate)
        self.crawl_list = crawl_list
        self.code_list = super().name_to_code(crawl_list)

    def _crawl(self, code):
        print("Crawling: {}".format(code[1].encode('utf-8')))
        # get last page number
        pg_url = PriceCrawler.source + "?code=" + str(code[1])
        res = requests.get(pg_url)
        print(res)
        soup = bs(res.text, 'lxml')
        last_page = int(soup.find("table", class_="Nnavi")
                            .find("td", class_="pgRR")
                            .a
                            .get('href')
                            .rsplit('&')[1]
                            .split('=')[1])

        df = pd.DataFrame()
        page = 1
        while True:
            print("Comp: {} Page: {}".format(code[1].encode('utf-8'), page))
            url = pg_url + "&page=" + str(page)
            df_html = pd.read_html(url, header=0)[0]

            # if page with the end date/ last page is found, stop the loop
            if df_html['날짜'].isin([self.edate]).any() or page >= last_page:
                df = df.append(df_html, ignore_index=True)
                break

            df = df.append(df_html, ignore_index=True)
            page += 1
    
        df = df.dropna()[::-1]
        df['날짜'] = pd.to_datetime(df['날짜'], format='%Y.%m.%d')
        dates = pd.date_range(self.edate, self.sdate, name='날짜')
        df = df.set_index('날짜').reindex(dates, method="ffill").reset_index()

        filepath = code[1]
        df.to_csv("./price/"+filepath+".csv", index=False)
        
        print("{} - {}: {} Price".format(self.edate, self.sdate, code[1]))
    
    def crawl(self):
        # function for multiprocessing
        # for code in self.code_list:
        #     self._crawl(code)
        for i in range(0, len(self.code_list), cpu_count):
            with Pool(cpu_count) as p:
                p.map(self._crawl, self.code_list[i: i+cpu_count])
        print("="*50)
        print("Done Crawling: {}".format(PriceCrawler.dtype))  

c_pd = pd.read_csv('./data.csv', error_bad_lines=False)
c_name = c_pd['기업명'].dropna().drop_duplicates().values
crawler = PriceCrawler("20190925" ,"20160101", c_name)
crawler.crawl()