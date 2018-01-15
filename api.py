#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: ctrip/api.py

import requests
from bs4 import BeautifulSoup
from ghost import Ghost, Session
import threading
import time
from datetime import datetime

##################################################

# 测试并加入ip_list
def add_task(type, ip, port):
    a = threading.Thread(target=test_ip, args=(type, ip, port,))
    threads.append(a)
    a.start()

def test_ip(type, ip, port):
    myip_url = 'http://api.ipaddress.com/myip'
    test_url = 'http://ip.cn'
    myip = s.get(myip_url).text
    proxy = {type: "%s://%s:%s" %(type, ip, port)}
    count = 0
    for i in range(3):
        try:
            r = s.get(test_url, proxies=proxy, timeout=3)
            r_ip = BeautifulSoup(r.content, "html.parser").code.text
            if r_ip == myip:
                #print('透明代理%s' % ip)
                break
        except:
            #print('%s无法连接！' % ip)
            break
        else:
            count += 1
    if count == 3:
        if r.status_code == 200:
            #print('%s加入列表！' % ip)
            ip_list.append((type, ip, port))

##########################################
# spys.one
def get_spys():
    url = 'http://spys.one/en/http-proxy-list'
    se.open(url)
    se.evaluate("document.getElementById('xpp').value=5")
    se.evaluate("document.getElementById('xf1').value=1")
    se.evaluate("document.getElementById('xf5').value=1")
    se.call('#xpp', 'onchange', expect_loading=True)
    html = se.content
    soup = BeautifulSoup(html, "html.parser")
    source = soup.select('tr.spy1xx')
    source1 = soup.select('tr.spy1x')
    source1.remove(source1[0])
    source = source + source1
    #print(len(source))
    for i in source:
        ip_info = spys_info(i)
        add_task(ip_info[0], ip_info[1], ip_info[2])

def spys_info(source):
    ip = source.select('font.spy14')[0].text.split('d',1)[0]
    port = source.select('font.spy14')[0].text.split(':')[-1]
    type = 'http'
    return(type, ip, port)

##########################################
UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
header = {'User-Agent':UA,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate'
}
s = requests.session()
s.keep_alive = False
se = Session(Ghost(), user_agent=UA, wait_timeout=30, wait_callback=None, display=False, viewport_size=(800, 680), download_images=False)

#################################
# hidemy
def get_hidemy():
    url = 'https://hidemy.name/en/proxy-list/?country=US&type=h&anon=4#list'
    se.open(url)
    se.wait_for_selector('table.proxy__t')
    html = se.content
    soup = BeautifulSoup(html, "html.parser")
    sources = soup.select('tbody > tr')
    for i in sources:
        ip_info = hidemy_info(i)
        add_task(ip_info[0], ip_info[1], ip_info[2])

def hidemy_info(source):
    ip = source.select('td')[0].text
    port = source.select('td')[1].text
    type = 'http'
    return(type, ip, port)

#################################
def load_proxy():
    global proxypool
    proxypool = list(ip_list)
    if len(proxypool) < 5:
        print('代理数量不足，还剩%s个代理' % len(proxypool))
    else:
        print('proxypool已更新%s个代理' % len(proxypool))

#################################
# sslproxies
def get_sslproxies():
    url = 'https://www.sslproxies.org/'
    r = s.get(url)
    html = r.content
    soup = BeautifulSoup(html, "html.parser")
    sources = soup.select('tbody > tr')
    for i in sources:
        ip_info = sslproxies_info(i)
        add_task(ip_info[0], ip_info[1], ip_info[2])

def sslproxies_info(source):
    ip = source.select('td')[0].text
    port = source.select('td')[1].text
    type = 'http'
    return(type, ip, port)

#################################

def get_proxy_m():
    global threads
    global ip_list
    threads = []
    ip_list = []
    #get_hidemy()
    get_spys()
    get_sslproxies()
    for t in threads:
        t.join()
    threads.clear()
    load_proxy()


def get_proxy_p():
    global ip_list
    while True:
        time.sleep(600)
        ip_list = []
        #get_hidemy()
        get_proxy_m()

def get_proxy():
    print('正在载入代理 proxypool')
    start_time = datetime.now()
    get_proxy_m()
    threading.Thread(target=get_proxy_p, args=()).start()
    end_time = datetime.now()
    timedelsta = (end_time - start_time).seconds
    print('耗时%s秒' % timedelsta)

get_proxy()
#########################
# API
from flask import Flask, Response, jsonify
#from flask import jsonify, Response
app = Flask(__name__)

@app.route("/")
def hello_world():
    result = proxypool
    return jsonify(result)

app.run(host='0.0.0.0',port=6666)


