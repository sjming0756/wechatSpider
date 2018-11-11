# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from pymysql import *

'''
抓取爱妮微网站首页的热门微信号号主信息：
官网地址：http://top.anyv.net/
'''

def getUser():
    headers = {
        'Host': 'top.anyv.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.90 Safari/537.36 2345Explorer/9.3.2.17331',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://www.anyv.net/index.php/category-81',
    }
    url = 'http://top.anyv.net/'
    body = requests.get(url,headers=headers).text
    response = BeautifulSoup(body,'lxml')

    data = response.select('ul')[3].get_text()
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

    user = getUser()
    
    #号主去重
    user_set = set(user)
    user_list_1 = list(user_set)
    #去重后按照原来的顺序进行入库
    user_list_1.sort(key=user.index) 
    print(len(user_list_1))

    for i in range(len(user_list_1)):
        user_name = user_list_1[i]
        print(user_name)
        user_id = 'None'
        biz = 'None'

        sql = """insert into wechat(user_name,user_id,biz) value(%s,%s,%s)"""
        try:
            conn.execute(sql, (user_name,user_id,biz))
            db.commit()
        except:
            db.rollback()

    db.close()
