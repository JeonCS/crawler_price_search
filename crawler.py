#-*- coding: utf-8 -*-

import os
import pandas as pd
from multiprocessing import Process
import sys

# 1. read company_list.txt
# 
class Crawler(object):
    # ddir = os.path.dirname(__file__) + "/../data/"
    companies = []
    # with open(os.path.dirname(__file__) + '/../company_list.txt') as f:
    #     companies = f.read().splitlines()

    def __init__(self, sdate, edate):
        self.sdate = sdate
        self.edate = edate

    def update_data(self, mode):
        pass

    def name_to_code(self, crawl_list):
        """
        Args:
        1. company_list: a list of company which needs corresponding codes
        Return: a list of given companies' trading codes
        """
        # print(crawl_list)
        code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
        code_df.종목코드 = code_df.종목코드.map("{:06d}".format)
        code_df = code_df[['회사명','종목코드']]
        code_list = [[company, code_df.loc[code_df['회사명'] == company].종목코드.values[0]] for company in crawl_list if len(code_df.loc[code_df['회사명'] == company].종목코드) > 0]
        return code_list
        
    # def get_crawl_list(self, dtype):
    #     # check if news/price data exist given the dtype and period
    #     crawl_list = [company for company in Crawler.companies if not os.path.exists(self.get_filename(dtype, company))]
    #     return crawl_list

    # def get_filename(self, dtype, company):
    #     # "{ddir}{dtype}_{company}_{sdate}_{edate}.csv"
    #     return Crawler.ddir + dtype + '/' + dtype + '_' + company + '_' + self.sdate + '_' + self.edate + '.csv'
    