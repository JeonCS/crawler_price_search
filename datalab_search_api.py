"""
Documentation ->
https://developers.naver.com/docs/datalab/search/#%EB%84%A4%EC%9D%B4%EB%B2%84-%ED%86%B5%ED%95%A9-%EA%B2%80%EC%83%89%EC%96%B4-%ED%8A%B8%EB%A0%8C%EB%93%9C-%EC%A1%B0%ED%9A%8C
"""

#-*- coding: utf-8 -*-
import os
import sys
import requests
import json
import pandas as pd

def datalab_search_api(c_name):
    client_id = "client_id"
    client_secret = "secret"
    url = "https://openapi.naver.com/v1/datalab/search"
    start_date = "2016-01-01"
    end_date = "2019-09-25"
    time_unit = "date"

    res = []
    period = pd.date_range(start_date, end_date, name='period')
    for comp in c_name[:4]:
        keyword_groups = [{
            "groupName" : comp,
            "keywords" : [comp]
        }]

        d = {
            "startDate":start_date,
            "endDate":end_date,
            "timeUnit":time_unit,
            "keywordGroups":keyword_groups
        }

        headers = {
            'X-Naver-Client-Id': client_id,
            'X-Naver-Client-Secret' : client_secret,
            'Content-Type' : 'application/json'
        }

        response = requests.post(
            url=url,
            headers=headers,
            json=d
        )
        res_code = response.status_code
        if res_code == 200:
            print("Collecting data of {}".format(comp))
            comp_df = pd.DataFrame(data=response.json()['results'][0]['data'][comp])
            comp_df.rename(columns={"ratio": comp}, inplace=True)
            res.append(comp_df)
        else:
            print("Error {}: at {}".format(res_code, comp))
            print(response.json())
            break

    res = pd.concat([res, period], axis=1)
    res.set_index('period', inplace=True)
    # res.to_csv("search_data.csv")

# c_pd = pd.read_csv('./data.csv', error_bad_lines=False)
# c_name = c_pd['기업명'].dropna().drop_duplicates().values

# datalab_search_api(c_name[:4])
