# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from pymysql import *
import json
import time
from lxml import etree

'''
爬取清博大数据微信公众号号主信息biz：http://www.gsdata.cn/
爬取的是各分类榜单，即科技、娱乐、时尚、游戏、财经等
'''

def get_gsdata(gid):
    headers = {
        'Host': 'www.gsdata.cn',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://www.gsdata.cn/custom/comrankdetails?gid=62',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'bdshare_firstime=1533621881395; _csrf-frontend=0ccd38018ce5a0a20e9723dcf5357c942bd673a3c403fe075314093a58663956a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%228yArDvVeeuSMEs3ujtI_n1b1n6z8ydaY%22%3B%7D; Hm_lvt_293b2731d4897253b117bb45d9bb7023=1533781797,1534904863,1535437297; PHPSESSID=7v11igrci24oit3a783uc08si2; _identity-frontend=fd6180faa2f51bc554c85ea26bbc63a58c2c704b715acd89dd1bd8768c7626d7a%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22_identity-frontend%22%3Bi%3A1%3Bs%3A27%3A%22%5B154434%2C%22test+key%22%2C2592000%5D%22%3B%7D; _gsdataCL=WyIxNTQ0MzQiLCIxNzMzNTg5MzE2NSIsIjIwMTgwOTA2MTc0OTEzIiwiYmE0MDZmZWY0NDQzMDUwOGE4OGM4YTQ1MjQ3OGZhNWQiLDEzNDg3N10%3D; acw_tc=AQAAAC90JD3l3AwAMTvyPVaJdZ0E14E9; Hm_lpvt_293b2731d4897253b117bb45d9bb7023=1536292912'
    }

    url = 'http://www.gsdata.cn/custom/comrankdetails?gid=' + gid
    body = requests.get(url,headers=headers).text
    print(body)
    time.sleep(1)

    response = BeautifulSoup(body,'lxml')
    data_list = response.find_all('a',{'class','mg0'})
    print(data_list)

    for data in data_list:
        data = str(data)
        pattern = re.compile('wxname=[^\s]*')
        soup = re.findall(pattern,data)
        wxname = soup[0][7:-1]
        print(wxname)

        #微信名
        pattern2 = re.compile('<h1>[^\s]*')
        soup2 = re.findall(pattern2,data)
        name = soup2[0][4:-5]
        print(name)

        #微信id
        pattern3 = re.compile('>[^\s]*</span>')
        soup3 = re.findall(pattern3,data)
        id = soup3[0][1:-7]
        print(id)

        #微信biz
        biz = get_biz(wxname,id)

        items = {
            'user_name': name,
            'user_id': id,
            'biz': biz
        }

        save_biz(items)

def get_biz(wxname,id):
    headers = {
        'Host': 'www.gsdata.cn',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        #'Referer': 'http://www.gsdata.cn/custom/comrankdetails?gid=62',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'bdshare_firstime=1533621881395; _csrf-frontend=0ccd38018ce5a0a20e9723dcf5357c942bd673a3c403fe075314093a58663956a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%228yArDvVeeuSMEs3ujtI_n1b1n6z8ydaY%22%3B%7D; Hm_lvt_293b2731d4897253b117bb45d9bb7023=1533781797,1534904863,1535437297; PHPSESSID=7v11igrci24oit3a783uc08si2; _identity-frontend=fd6180faa2f51bc554c85ea26bbc63a58c2c704b715acd89dd1bd8768c7626d7a%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22_identity-frontend%22%3Bi%3A1%3Bs%3A27%3A%22%5B154434%2C%22test+key%22%2C2592000%5D%22%3B%7D; _gsdataCL=WyIxNTQ0MzQiLCIxNzMzNTg5MzE2NSIsIjIwMTgwOTA2MTc0OTEzIiwiYmE0MDZmZWY0NDQzMDUwOGE4OGM4YTQ1MjQ3OGZhNWQiLDEzNDg3N10%3D; acw_tc=AQAAAC90JD3l3AwAMTvyPVaJdZ0E14E9; Hm_lpvt_293b2731d4897253b117bb45d9bb7023=1536292912'
    }
    url = 'http://www.gsdata.cn/rank/wxdetail?wxname=' + wxname
    body = requests.get(url,headers=headers).text
    #print(body)
    time.sleep(2)

    pattern = re.compile('biz=[^\s]*')
    soup = re.findall(pattern,str(body))
    print(soup)

    data = soup[0]
    biz = data[4:20]
    print(biz)

    '''
    url = 'http://www.gsdata.cn/rank/toparc?wxname=' + wxname + '&wx=' + id + '&sort=-1'
    data = {
        'wxname':wxname,
        'wx':id,
        'sort': '-1'
    }
    body = requests.get(url,data=data,headers=headers).text
    time.sleep(3)
    response = json.loads(body)
    print(response)

    data = response['data'][0]
    link = data['url']

    pattern = re.compile('biz=[^\s]*')
    soup = re.findall(pattern,str(link))
    biz = soup[0][4:20]
    print(biz)
    '''
    return biz

def save_biz(items):
    sql = """insert into gsdata_wechat(user_name,user_id,biz) values(%s,%s,%s)"""
    try:
        cursor.execute(sql, (
            items["user_name"], items["user_id"], items["biz"]))
        db.commit()
        print("success")
    except:
        db.rollback()

def get_gsdata2(gid,i):
    headers = {
        'Host': 'www.gsdata.cn',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://www.gsdata.cn/custom/comrankdetails?gid=62',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'bdshare_firstime=1533621881395; _csrf-frontend=0ccd38018ce5a0a20e9723dcf5357c942bd673a3c403fe075314093a58663956a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%228yArDvVeeuSMEs3ujtI_n1b1n6z8ydaY%22%3B%7D; Hm_lvt_293b2731d4897253b117bb45d9bb7023=1533781797,1534904863,1535437297; PHPSESSID=7v11igrci24oit3a783uc08si2; _identity-frontend=fd6180faa2f51bc554c85ea26bbc63a58c2c704b715acd89dd1bd8768c7626d7a%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22_identity-frontend%22%3Bi%3A1%3Bs%3A27%3A%22%5B154434%2C%22test+key%22%2C2592000%5D%22%3B%7D; _gsdataCL=WyIxNTQ0MzQiLCIxNzMzNTg5MzE2NSIsIjIwMTgwOTA2MTc0OTEzIiwiYmE0MDZmZWY0NDQzMDUwOGE4OGM4YTQ1MjQ3OGZhNWQiLDEzNDg3N10%3D; acw_tc=AQAAAC90JD3l3AwAMTvyPVaJdZ0E14E9; Hm_lpvt_293b2731d4897253b117bb45d9bb7023=1536292912'
    }

    url = 'http://www.gsdata.cn/custom/ajax_comrankdetails?type=day&date=2018-03-05&gid=' +gid + '&keyword=&page=' + str(i)
    body = requests.get(url, headers=headers).text
    print(body)
    time.sleep(1)

    response = json.loads(body)
    print(response)
    soup = response['data']
    time.sleep(1)

    response = BeautifulSoup(soup, 'lxml')
    data_list = response.find_all('a', {'class', 'mg0'})
    print(data_list)

    if i >= 1:
        for data in data_list:
            data = str(data)
            pattern = re.compile('wxname=[^\s]*')
            soup = re.findall(pattern, data)
            wxname = soup[0][7:-1]
            print(wxname)

            # 微信名
            pattern2 = re.compile('<h1>[^\s]*')
            soup2 = re.findall(pattern2, data)
            name = soup2[0][4:-5]
            print(name)

            # 微信id
            pattern3 = re.compile('>[^\s]*</span>')
            soup3 = re.findall(pattern3, data)
            id = soup3[0][1:-7]
            print(id)

            # 微信biz
            try:
                biz = get_biz(wxname, id)

                items = {
                            'user_name': name,
                            'user_id': id,
                            'biz': biz
                }

                save_biz(items)
            except:
                break

if __name__ == "__main__":
    db = connect(host="localhost", port=3306, db="spider", user="root", password="secret", charset="utf8")
    cursor = db.cursor()
    gid_list = ['9202','10409','10413','11559','13553','13810','14254','15234','15617','15620']
    for i in gid_list:
        #gid = '4482'
        gid = i
        get_gsdata(gid)
        print(gid)

        for i in range(2,9):
            get_gsdata2(gid,i)
            time.sleep(2)

    db.close()
