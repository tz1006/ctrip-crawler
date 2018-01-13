#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: ctrip/tools.py

import requests
import yaml
from datetime import datetime, timedelta

s = requests.session()
s.keep_alive = False

def code(city):
    url = 'http://flights.ctrip.com/international/tools/poi.ashx?charset=utf-8&key=%s&channel=1&mode=1&f=1&v=2' % city
    r = s.get(url)
    data = r.text.split('=')[1]
    res = yaml.load(data)
    code = res['Data'][0]['Code']
    return code

def date_list(start_date, end_date):
    start_date = start_date.split('-')
    start_year = start_date[0]
    start_month = start_date[1]
    start_day = start_date[2]
    start_time = datetime.strptime('%s-%s-%s 09:25:00' % (start_year, start_month, start_day), "%Y-%m-%d %H:%M:%S")
    end_date = end_date.split('-')
    end_year = end_date[0]
    end_month = end_date[1]
    end_day = end_date[2]
    end_time = datetime.strptime('%s-%s-%s 09:25:00' % (end_year, end_month, end_day), "%Y-%m-%d %H:%M:%S")
    delta_days = (end_time.date() - start_time.date()).days
    li = []
    for i in range(delta_days+1):
        date = (start_time.date() + timedelta(days=i)).strftime("%Y-%m-%d")
        li.append(date)
    return li



def help():
    print('''
    tools
    code(city)
    date_list(start_date, end_date)
    ''')

help()


