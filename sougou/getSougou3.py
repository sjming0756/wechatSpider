# -*- coding:utf-8 -*-

import requests
from fake_useragent import UserAgent
from lxml import etree
import time
from pymysql import *
from get_img import *
import random

'''
通过搜狗微信获取微信公众号唯一标识biz,当出现验证码时，需要手动输入
'''

def sougou_weixin(style):
    ua = UserAgent()
    headers = {
        #"User-Agent":ua.random,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
        "Host": "weixin.sogou.com",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "pgv_pvi=1314040832; uin=o2114246631; skey=@mlLi0WM9X; pt2gguin=o2114246631; ptisp=ctc; RK=bugJ/K1kY3; ptcz=90aa445321656f54222207397bf929800a8a572635aa2b3bb1dc74f29a42faf3; pgv_info=ssid=s7521773861; pgv_pvid=7532008008; o_cookie=2114246631"
    }

    for i in range(1,11):
        url = 'https://weixin.sogou.com/weixin?query='+ style + '&_sug_type_=&s_from=input&_sug_=n&type=1&page=' + str(i) + '&ie=utf8'
        body = requests.get(url,headers=headers,verify=False).text
        print(body)

        response = etree.HTML(body)

        #最近文章链接
        url_list = response.xpath('//*[@id]/dl[3]/dd/a/@href')
        print(url_list)
        for url in url_list:
            link = url
            print(link)
            items = get_biz(link)
            save_biz(items)
            time.sleep(5)

        link_list = response.xpath('//*[@id]/div/div[2]/p[1]/a/@href')
        if len(link_list) < 10:
            return

def save_biz(items):
    sql = """insert into sogou_wechat_game(user_name,user_id,biz) values(%s,%s,%s)"""
    try:
        cursor.execute(sql, (
            items["user_name"], items["user_id"], items["biz"]))
        db.commit()
        print("success")
    except:
        db.rollback()

def get_biz(url):
    ua = UserAgent()
    headers = {
        #"User-Agent": ua.random,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
        "Host": "mp.weixin.qq.com",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "http://weixin.sogou.com/",
        "Cookie": "pgv_pvi=1314040832; uin=o2114246631; skey=@mlLi0WM9X; pt2gguin=o2114246631; ptisp=ctc; RK=bugJ/K1kY3; ptcz=90aa445321656f54222207397bf929800a8a572635aa2b3bb1dc74f29a42faf3; pgv_info=ssid=s7521773861; pgv_pvid=7532008008; o_cookie=2114246631"
    }
    link_url = url
    body = requests.get(link_url, headers=headers, verify=False).text
    print(body)
    time.sleep(2)

    response = etree.HTML(body)

    info = response.xpath('//*[@id="loading"]')
    print(info)

    if len(info) != 0:
        print('请输入验证码')


    #微信号名称
    try:
        name_list = response.xpath('//*[@id="js_name"]/text()')
        name = name_list[0].strip()
        print(name)
    except:
        name = 'None'

    #微信号id
    id = 'None'

    #微信唯一标识biz
    script_list = response.xpath('//*[@id="activity-detail"]/script[1]/text()')
    print(script_list)
    n = len(script_list)
    biz = script_list[n-1]
    #biz_list = response.xpath('/html/body/script[8]/text()')
    #for biz in biz_list:
    print(biz.strip())
    biz = biz[20:36]
    print(biz)

    items = {
        'user_name':name,
        'user_id':id,
        'biz':biz
    }

    return items

if __name__ == "__main__":
    db = connect(host="localhost", port=3306, db="spider", user="root", password="secret", charset="utf8")
    cursor = db.cursor()
    try:
        sql = """select id,user_name from wechat_game"""
        cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    for i in range(len(data)):
        id = data[i][0]
        print(id)
        style = data[i][1]
        print(style)
        sougou_weixin(style)
        time.sleep(0.5)

    db.close()
