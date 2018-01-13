#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: ctrip/proxy.py

import requests
import yaml

s = requests.session()
s.keep_alive = False

url = 'http://127.0.0.1:5000/'
r = s.get(url)
proxypool = r.json()
