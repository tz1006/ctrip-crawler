#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: ctrip/tools.py

import requests
import yaml
import sqlite3
from datetime import datetime, timedelta
import os

s = requests.session()
s.keep_alive = False

def code(city, debug=0):
    url = 'http://flights.ctrip.com/international/tools/poi.ashx?charset=utf-8&key=%s&channel=1&mode=1&f=1&v=2' % city
    r = s.get(url)
    if debug == 1:
        return r
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


def insert_price(departCity, arrivalCity, departDate, returnDate, price):
    if os.path.exists('database') == False:
        os.makedirs('database')
    table_name = '\'%s-%s\'' % (code(departCity), code(arrivalCity))
    departDate = '\'%d月%d日\'' % (int(departDate.split('-')[1]), int(departDate.split('-')[2]))
    returnDate = '\'%d月%d日\'' % (int(returnDate.split('-')[1]), int(returnDate.split('-')[2]))
    conn = sqlite3.connect('database/ctrip.db')
    cursor = conn.cursor()
    # 尝试新建表
    cursor.execute("CREATE TABLE IF NOT EXISTS %s (departDate TEXT UNIQUE);" % table_name)
    # 尝试添加列
    try:
        cursor.execute("ALTER TABLE %s ADD COLUMN %s INT" % (table_name, returnDate))
    except:
        pass
    # 尝试添加行
    try:
        cursor.execute("INSERT INTO %s ('departDate') VALUES (%s)" % (table_name, departDate))
    except:
        pass
    # 添加数据
    try:
        cursor.execute("UPDATE %s set %s=%s WHERE departDate=%s" % (table_name, returnDate, price, departDate))
        print('已添加数据%s,%s ¥%s到表%s' %(departDate, returnDate, price, table_name))
    except:
        pass
    conn.commit()
    conn.close()

def help():
    print('''
    tools
    code(city)
    date_list(start_date, end_date)
    ''')

help()



