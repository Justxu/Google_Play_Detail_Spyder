# -*- coding: utf-8 -*-
"""
Created on Thu May  3 13:59:54 2018

@author: Lee
"""

import urllib.request as request
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import re
import random
#import config

proxie = { 
        'http' : "http://127.0.0.1:1080",
        'https': "http://127.0.0.1:1080"
    }  

def get_page(package,country=None):
    if country == None:
        url = 'https://play.google.com/store/apps/details?id='+package
    else:
        url = 'https://play.google.com/store/apps/details?id='+package+'&hl='+country
    time = 0
    while time < 10:
        try:
            #if config.get('proxy_address', None) is not None:
                #response = requests.get(url, proxy= config.get('proxy_address', None))
            #else:,proxies="http://127.0.0.1:1080"
            response = requests.get(url,proxies={"http":"socks5://127.0.0.1:1080","https":"socks5://127.0.0.1:1080"}, timeout=30)
            soup=BeautifulSoup(response.text,'html.parser')
            return soup
        except Exception as e:
            print(e)
            sleep(random.uniform(5,10))
            #print(package+' not found!')
        time += 1
        
def get_title(soup):
    title = soup.find('h1',class_='AHFaub').string
    return str(title)
    
def get_short_des(soup):
    for i in soup.find_all('script'):
        if not i.string == None:
            if 'ds:3' in i.string:
                tag = str(i)
    tags = re.findall('\[null\,\".*?\"\]',tag)
    short_des = tags[1].split('\"')[1]
    return short_des

def get_long_des(soup):
    i = soup.find('meta',{'name': 'description'})
    long_des = i['content']
    return long_des

def get_ratings(soup):
    a = soup.find('span',class_='AYi5wd TBRnV')
    rating = a.span.string
    return rating

def get_star(soup):
    b = soup.find('div',class_='pf5lIe')
    string = b.div['aria-label']
    #还要分隔一下字符串
    return string

def get_installs(soup):
    ins = soup.find('div',class_='xyOfqd')
    for i in ins:
        if i.div.string == 'Installs':
            install = i.span.string
    return install

def get_Updated(soup):
    update = soup.find('div',class_='xyOfqd')
    for i in update:
        if i.div.string == 'Updated':
            Updated = i.span.string
    return Updated

def get_Size(soup):
    sizes = soup.find('div',class_='xyOfqd')
    for i in sizes:
        if i.div.string == 'Size':
            Size = i.span.string
    return Size

def get_Current_Version(soup):
    versions = soup.find('div',class_='xyOfqd')
    for i in versions:
        if i.div.string == 'Current Version':
            version = i.span.string
    return version

def get_developer(soup):
    deve = soup.find('span',class_='T32cc UAO9ie')
    developer_name = deve.string
    return developer_name

