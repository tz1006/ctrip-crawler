#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: ctrip/main.py

from getprice import round_trip
from multiprocessing import Process
from tools import *

DepartCity = '洛杉矶'
ReturnCity = '上海'
#departDate = '2018-03-01'
#returnDate = '2018-03-11'

depart = date_list('2018-04-10', '2018-04-11')
arrive = date_list('2018-07-10', '2018-07-11')

def test():
    for i in depart:
        for l in arrive:
            if int(i.split('-')[0]) <= int(l.split('-')[0]):
                if int(i.split('-')[1]) < int(l.split('-')[1]):
                    Process(target=round_trip,args=(DepartCity, ReturnCity, i, l)).start()
                elif int(i.split('-')[1]) == int(l.split('-')[1]):
                    if int(i.split('-')[2]) < int(l.split('-')[2]):
                        Process(target=round_trip,args=(DepartCity, ReturnCity, i, l)).start()

def help():
    print('''
    round_trip(DepartCity, ReturnCity, departDate, returnDate)

    test()
    ''')

help()


import code
code.interact(banner = "", local = locals())


