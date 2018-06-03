# -*- coding: utf-8 -*-
"""
Created on Thu May  3 13:57:51 2018

@author: Lee
"""

import GPbasicAPI as GP
import pandas as pd
import re
import random
from time import sleep
import json


#

faillist = []
copy = dict()
def get_copy_dict(package,langs):
    copys = {}
    for lan in langs:
        pack_dict = {}
        soup = GP.get_page(package,lan)
        if soup == None:
            sleep(random.uniform(10,30))
            soup = GP.get_page(package,lan)
            if soup == None:
                faillist.append([package,lan])
                continue
        pack_dict['title'] = GP.get_title(soup)
        pack_dict['long_des'] = GP.get_long_des(soup)
        pack_dict['short_des'] = GP.get_short_des(soup)
        copys[lan] = pack_dict
    return copys

def get_info_dict(package):
    infos = {}
    soup = GP.get_page(package)
    if soup == None:
        sleep(random.uniform(10,30))
        soup = GP.get_page(package)
        if soup == None:
            return infos
    infos['developer'] = GP.get_developer(soup)
    infos['ratings'] = GP.get_ratings(soup)
    infos['installs'] = GP.get_installs(soup)
    infos['update'] = GP.get_Updated(soup)
    infos['size'] = GP.get_Size(soup)
    infos['version'] = GP.get_Current_Version(soup)
    return infos

def get_whole_to_dict(packages,langs):
    result = {}
    num = 0 
    for pack in packages:
        result = {}
        try:
            result[pack] = get_info(pack)
            result[pack]['copy'] = get_copy(pack,langs)
            result = str(result)
            with open('./test1/'+pack+'.txt','w',encoding="utf-8") as f:
                f.write(result)
        except Exception as e:
            print(e)
            continue
        num += 1
        print(str(num)+'/'+str(len(packages)))
    return result

def constructor(soup,pack):
    columns = ['developer','title','short_des','long_des','ratings','installs','update','size','current_version']
    df = pd.DataFrame(index=[pack],columns=columns)
    if not soup.title.string == 'Not Found':
        df['developer'] = GP.get_developer(soup)
        df['title'] = GP.get_title(soup)
        df['short_des'] = GP.get_short_des(soup)
        df['long_des'] = GP.get_long_des(soup)
        df['ratings'] = GP.get_ratings(soup)
        df['installs'] = GP.get_installs(soup)
        df['update'] = GP.get_Updated(soup)
        df['size'] = GP.get_Size(soup)
        df['current_version'] = GP.get_Current_Version(soup)
        return df
    else:
        return df
    
def get_all_infos(packages):
    columns = ['developer','title','short_des','long_des','ratings','installs','update','size','current_version']
    df = pd.DataFrame(columns=columns)
    line = 0
    for pack in packages:
        soup = GP.get_page(pack)
        if not soup == None:
            df = df.append(constructor(soup,pack))
        line += 1
        print(line,'/',len(packages))
    return df
            
#执行
df = pd.read_csv('./packages.csv',index_col = 0)
df2 = get_all_infos(df.index)
df2.to_csv('./result.csv')