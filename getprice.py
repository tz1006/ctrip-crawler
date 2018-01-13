#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: ctrip/getprice.py

from tools import *
from ghost import Ghost, Session
from bs4 import BeautifulSoup
from ualist import ua_list
from random import choice
from datetime import datetime
from pytz import timezone
from proxy import proxypool

#gh = Ghost()

#se = Session(gh, user_agent=ua, wait_timeout=20, wait_callback=None, display=True, viewport_size=(800, 680), download_images=True)

#DepartCity = '洛杉矶'
#ReturnCity = '上海'
#departDate = '2018-03-01'
#returnDate = '2018-03-11'


def round_trip(DepartCity, ReturnCity, departDate, returnDate, debug=0):
    #global se
    start_time = datetime.now()
    url = 'http://flights.ctrip.com/international/round-%s-%s-%s-%s?%s&%s&y_s' % (DepartCity, ReturnCity, code(DepartCity), code(ReturnCity), departDate, returnDate)
    print(url)
    ctrip_access = False
    while ctrip_access == False:
        se = Session(Ghost(), wait_timeout=30, wait_callback=None, display=True, viewport_size=(800, 680), download_images=False)
        se.delete_cookies()
        proxy = choice(proxypool)
        se.set_proxy(proxy[0], proxy[1], int(proxy[2]))
        try:
            se.open(url, user_agent=choice(ua_list))
            #print('已打开 %s' % url)
        except:
            se.hide()
            del se
            proxypool.remove(proxy)
            print("blacklist %s" % proxy[1])
            continue
        ctrip_access = se.exists('li:nth-child(5) > span')
        if ctrip_access == False:
            se.hide()
            del se
            proxypool.remove(proxy)
            print("blacklist %s" % proxy[1])
    se.click('#sortControls > ul > li:nth-child(5) > span')
    if se.exists('i.icon-reverse') == True:
        se.click('#sortControls > ul > li:nth-child(5) > span')
    se.wait_while_selector('#FI_progBar', timeout=20)
    print('Loading finished!')
    se.sleep(0.2)
    html = se.content
    soup = BeautifulSoup(html, "html.parser")
    source = soup.select('#flightList > div')
    if debug == 1:
        return source
    lowest = source[0].select('span.price2')[0].text
    end_time = datetime.now()
    timedelsta = (end_time - start_time).seconds
    print('%s-%s往返 %s去 %s回 最低价%s 搜索耗时%s秒' %(DepartCity, ReturnCity, departDate, returnDate, lowest, timedelsta))
    se.hide()
    del se
    return lowest


def help():
    print('''
    round_trip(DepartCity, ReturnCity, departDate, returnDate)
    ''')

help()

#import code
#code.interact(banner = "", local = locals())
