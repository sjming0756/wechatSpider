# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from pymysql import *
import json
import time
from lxml import etree
import random

def get_gsdata(style):
    headers = {
        'Host': 'www.gsdata.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #'Referer': 'http://www.gsdata.cn/custom/comrankdetails?gid=62',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'bdshare_firstime=1533621881395; _csrf-frontend=0ccd38018ce5a0a20e9723dcf5357c942bd673a3c403fe075314093a58663956a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%228yArDvVeeuSMEs3ujtI_n1b1n6z8ydaY%22%3B%7D; Hm_lvt_293b2731d4897253b117bb45d9bb7023=1534904863,1535437297; PHPSESSID=kcncs886ceu0kndp75e1kt76s1; _identity-frontend=fd6180faa2f51bc554c85ea26bbc63a58c2c704b715acd89dd1bd8768c7626d7a%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22_identity-frontend%22%3Bi%3A1%3Bs%3A27%3A%22%5B154434%2C%22test+key%22%2C2592000%5D%22%3B%7D; _gsdataCL=WyIxNTQ0MzQiLCIxNzMzNTg5MzE2NSIsIjIwMTgwOTEwMTAxNTA4IiwiNTY0MjdlMDI3OTU0NzhkODJjMGQ3ZWViMDBhNDU5OTUiLDEzNDg3N10%3D; acw_tc=AQAAALNCLyptmQcAh4AuG+wrqmVL/zCN; Hm_lpvt_293b2731d4897253b117bb45d9bb7023=1536546004'
    }

    url = 'http://www.gsdata.cn/query/wx?q=' + style
    body = requests.get(url,headers=headers).text
    #print(body)
    time.sleep(2)


    response = BeautifulSoup(body,'lxml')
    data_list = response.find_all('li',{'class','clearfix list_query'})
    #print(data_list)
    n = len(data_list)
    time.sleep(2)

    if n == 0:
        return 0

    for data in data_list:
        data = str(data)

        #微信名
        try:
            pattern = re.compile('class="color-pink">[^\s]*</span>[^\s]*</a>')
            soup= re.findall(pattern,data)
            soup = soup[0]
            name = soup.replace('class="color-pink">','').replace('</span>','').replace('</a>','')
            name.strip()
            print(name)
        except:
            name = 'None'

        #微信id
        try:
            pattern2 = re.compile('>[^\s]*</span>')
            soup2 = re.findall(pattern2,data)
            id = soup2[1][1:-7]
            print(id)
        except:
            id = 'None'

        #微信biz
        try:
            pattern3 = re.compile('biz=[^\s]*')
            soup3 = re.findall(pattern3,data)
            biz = soup3[0][4:20]
            print(biz)

            items = {
                'user_name': name,
                'user_id': id,
                'biz': biz
            }

            save_biz(items)
        except:
            pass

    return n

def save_biz(items):
    sql = """insert into gsdata_wechat02(user_name,user_id,biz) values(%s,%s,%s)"""
    try:
        cursor.execute(sql, (
            items["user_name"], items["user_id"], items["biz"]))
        db.commit()
        print("success")
    except:
        db.rollback()

def get_gsdata2(style,i):
    headers = {
        'Host': 'www.gsdata.cn',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        #'Referer': 'http://www.gsdata.cn/custom/comrankdetails?gid=62',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'bdshare_firstime=1533621881395; _csrf-frontend=0ccd38018ce5a0a20e9723dcf5357c942bd673a3c403fe075314093a58663956a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%228yArDvVeeuSMEs3ujtI_n1b1n6z8ydaY%22%3B%7D; Hm_lvt_293b2731d4897253b117bb45d9bb7023=1534904863,1535437297; PHPSESSID=kcncs886ceu0kndp75e1kt76s1; _identity-frontend=fd6180faa2f51bc554c85ea26bbc63a58c2c704b715acd89dd1bd8768c7626d7a%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22_identity-frontend%22%3Bi%3A1%3Bs%3A27%3A%22%5B154434%2C%22test+key%22%2C2592000%5D%22%3B%7D; _gsdataCL=WyIxNTQ0MzQiLCIxNzMzNTg5MzE2NSIsIjIwMTgwOTEwMTAxNTA4IiwiNTY0MjdlMDI3OTU0NzhkODJjMGQ3ZWViMDBhNDU5OTUiLDEzNDg3N10%3D; acw_tc=781bad0915365464499285943e516b5511148f2d9cc26f6a0d074ca1d4f81f; Hm_lpvt_293b2731d4897253b117bb45d9bb7023=1536546450'
    }

    url = 'http://www.gsdata.cn/query/ajax_wx?q=' + style + '&page=' + str(i) + '&types=all&industry=all&proName='
    body = requests.get(url, headers=headers).text
    #print(body)
    time.sleep(1)

    try:
        response = json.loads(body)
        #print(response)
        soup = response['data']
        time.sleep(1)
    except:
        return


    response = BeautifulSoup(soup, 'lxml')
    data_list = response.find_all('div', {'class', 'word'})
    #print(data_list)
    time.sleep(1)

    n = len(data_list)

    for data in data_list:
        data = str(data)

        # 微信名
        try:
            pattern = re.compile('target="_blank">[^\s]*<span class="color-pink">[^\s]*</span>[^\s]*</a>')
            soup = re.findall(pattern, data)
            body = soup[0]
            body = body.replace('target="_blank">','').replace('<span class="color-pink">','').replace('</span>','').replace('</a>','')
            name = body.strip()
            print(name)
        except:
            name = 'None'

        # 微信id
        try:
            pattern2 = re.compile('>[^\s]*</span>')
            soup2 = re.findall(pattern2, data)
            id = soup2[1]
            id = id[1:-7]
            print(id)
        except:
            id = 'None'

        # 微信biz
        try:
            pattern3 = re.compile('biz=[^\s]*')
            soup3 = re.findall(pattern3,data)
            biz = soup3[0]
            biz = biz[4:20]
            print(biz)

            items = {
                    'user_name': name,
                    'user_id': id,
                    'biz': biz
            }

            save_biz(items)
        except:
            pass

    return n

if __name__ == "__main__":
    db = connect(host="localhost", port=3306, db="spider", user="root", password="secret", charset="utf8")
    cursor = db.cursor()

    try:
        sql = """select id,word from keywords01"""
        cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    for i in range(len(data)):
        id = data[i][0]
        word = data[i][1]
        style = str(word)
        n = get_gsdata(style)
        time.sleep(10)
        for i in range(2,9):
            if n == 25:
                n = get_gsdata2(style,i)
                time.sleep(10)
        time_list = [15,16,17,18,19,20]
        t = random.choice(time_list)
        time.sleep(t)
        if i%10 == 0:
            time.sleep(30)
    db.close()
