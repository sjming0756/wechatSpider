# -*- coding:utf-8 -*-

import requests
from fake_useragent import UserAgent
from lxml import etree
import time
from pymysql import *
from get_img import *
import random

def sougou_weixin(style):
    ua = UserAgent()
    headers = {
        #"User-Agent":ua.random,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
        "Host": "weixin.sogou.com",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://weixin.sogou.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "SUV=004017817783A8CB5AEAC727EAA71499; IPLOC=CN4401; SUID=7FAB83774842910A000000005AEC5311; SUID=7FAB83773120910A000000005AEC5312; CXID=854B6BA093B26929C237D28053DEF393; ad=iyllllllll2bYFbKlllllVHP2HDlllllphfl0Zllllwllllllqxlw@@@@@@@@@@@; ABTEST=0|1533620992|v1; weixinIndexVisited=1; JSESSIONID=aaaMx5Sk0z7cy5DdgCBvw; sct=65; PHPSESSID=4s4c1nu2jiroftcaq84h9segv6; SNUID=52AD00352D2B5953528F66BB2EB7B59E"
    }

    url = 'https://weixin.sogou.com/pcindex/pc/pc_' + style + '/pc_' + style + '.html'
    body = requests.get(url,headers=headers,verify=False).text
    print(body)
    response = etree.HTML(body)
    # 最近文章链接
    url_list = response.xpath('//*[@id="pc_6_0"]/li/div[1]/a/@href')
    print(url_list)

    for url in url_list:
        link = url
        print(link)
        items = get_biz(link)
        save_biz(items)
        time.sleep(5)

    for i in range(1,5):
        url = 'https://weixin.sogou.com/pcindex/pc/pc_' + style + '/' + str(i) + '.html'
        body = requests.get(url,headers=headers,verify=False).text
        print(body)

        response = etree.HTML(body)

        #最近文章链接
        url_list = response.xpath('//*[@id="pc_6_0"]/li/div[1]/a/@href')
        print(url_list)
        for url in url_list:
            link = url
            print(link)
            items = get_biz(link)
            save_biz(items)
            time.sleep(5)


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
        return

    #微信号id

    id = 'None'

    #微信唯一标识biz
    script_list = response.xpath('//*[@id="activity-detail"]/script[1]/text()')
    print(script_list)
    n = len(script_list)
    biz = script_list[n-1]
    print(biz)
    #biz_list = response.xpath('/html/body/script[8]/text()')
    #for biz in biz_list:
    biz = biz
    print(biz)
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

    '''
    ....
    5：科技
    6：财经
    7：汽车
    ....
    15：教育
    16：星座
    17：体育
    18：军事
    19：游戏
    ....
    等等
    '''
    style = '19'
    sougou_weixin(style)
    time.sleep(0.2)

    db.close()