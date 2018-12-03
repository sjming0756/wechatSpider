# -*- coding:utf-8 -*-

from pymysql import *
import requests
import urllib3
import time
from bs4 import BeautifulSoup

'''
微信公众号文章内容抓取，抓取的是公众号中文章的文字内容
'''

def loadLink(url):
    headers = {
        'Host': 'mp.weixin.qq.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'pgv_pvid=5509325691; tvfe_boss_uuid=bfc851573f53c21e; pt2gguin=o2721185782; RK=NZgsqA21s7; ptcz=7a3b7631ab91fbf7954e40da437b2723945378a19127e5a008a5c19eb0a3046c; o_cookie=2721185782; eas_sid=n1U5x4t2r8H033L3s1U5u7y6J9; pgv_pvi=9528235008; pac_uid=1_2721185782; ptui_loginuin=2721185782; rewardsn=; wxtokenkey=777If-Modified-Since: Mon, 3 Dec 2018 15:41:57 +0800'
    }

    body = requests.get(url, headers=headers, timeout=5).text
    urllib3.disable_warnings()
    time.sleep(0.1)
   
    response = BeautifulSoup(body,'lxml')
    soup = response.find_all('div',{'id':'js_content'})
    soup = soup[0]

    pattern = BeautifulSoup(str(soup),'lxml')
    soup2 = pattern.get_text()
    soup2 = str(soup2)
    soup2 = soup2.strip()
    print(soup2)

    return soup2

if __name__ == "__main__":
    db = connect(host="localhost", port=3306, db="Spider", user="root", password="secret", charset="utf8")
    cursor = db.cursor()

    try:
        sql = 'SELECT id, msg_link,content FROM wechatPage'
        MainUrl = cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    for i in range(2131,len(data)):
        id = data[i][0]
        print(id)
        msg_link = data[i][1]
        print(msg_link)
        content = data[i][2]

        page = loadLink(msg_link)
        #time.sleep(1000)

        n = id
        n = str(n)
        params = [page, n]
        try:
            sql = """update wechatPage set content=%s WHERE id=%s"""
            cursor.execute(sql, params)
            db.commit()
        except:
            db.rollback()
            time.sleep(1)

    db.close()
