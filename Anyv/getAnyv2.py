# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from pymysql import *
import time

'''
抓取爱妮微网站的热门微信号号主信息：http://top.anyv.net/
按类别进行抓取：科技、游戏、财经、时尚等
'''

def getUser(n):
    headers = {
        'Host': 'top.anyv.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.90 Safari/537.36 2345Explorer/9.3.2.17331',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://www.anyv.net/index.php/category-81',
    }
    #财经
    #url = 'http://www.anyv.net/index.php/category-51-page-' + n + '/'
    #科技
    #url = 'http://www.anyv.net/index.php/category-19-page-' + n + '/'
    #游戏
    #url = 'http://www.anyv.net/index.php/category-261-page-' + n + '/'
    #时尚
    url = 'http://www.anyv.net/index.php/category-22-page-' + n + '/'
    body = requests.get(url, headers=headers).text

    response = BeautifulSoup(body,'lxml')

    data = response.select('ul')[5].get_text()
    data = data.split('\n')

    user = []
    for i in range(len(data)):
        if data[i] == '':
            pass
        else:
            user.append(data[i])

    return user

if __name__ == "__main__":
    db = connect(host="localhost", port=3306, db="spider", user="root", password="123456", charset="utf8")
    conn = db.cursor()

    for i in range(1,59):
        print(i)
        n = str(i)
        user = getUser(n)
        time.sleep(1)

        for i in range(len(user)):
            user_name = user[i]
            print(user_name)
            user_id = 'None'
            biz = 'None'

            sql = """insert into wechat_fashion(user_name,user_id,biz) value(%s,%s,%s)"""
            try:
                conn.execute(sql, (user_name,user_id,biz))
                db.commit()
            except:
                db.rollback()

    db.close()