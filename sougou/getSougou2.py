# -*- coding:utf-8 -*-

import requests
from fake_useragent import UserAgent
from lxml import etree
import time
from pymysql import *
from get_img import *
import random
from selenium import webdriver
from bs4 import BeautifulSoup
import re

'''
通过分词或者微信名搜索的方式获取微信公众号的唯一标识：
每页最多可搜10个公众号，最多可以搜有10页

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
        url = 'https://weixin.sogou.com/weixin?query=' + style + '&_sug_type_=&s_from=input&_sug_=n&type=1&page=' + str(i) + '&ie=utf8'
        body = requests.get(url,headers=headers,verify=False).text
        response = etree.HTML(body)

        #主页链接
        url_list = response.xpath('//*[@id]/div/div[2]/p[1]/a/@href')
        print(url_list)
        for url in url_list:
            link = url
            print(link)
            items = get_biz(link)
            save_biz(items)
            time.sleep(0.5)

        if len(url_list) < 10:
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
        # "User-Agent": ua.random,
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
    soup = requests.get(link_url, headers=headers, verify=False)
    body = soup.text
    print(soup.cookies.get_dict())
    tamstamp = int(time.time() * 1000)
    rand = round(random.random(), 4)
    cert = tamstamp + rand
    rands = str(cert)
    print(body)

    response = etree.HTML(body)
    info = response.xpath('//*[@id="loading"]')

    if len(info) != 0:
        driver = webdriver.PhantomJS()
        driver.get(url)
        time.sleep(0.5)
        driver.refresh()
        driver.implicitly_wait(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pattern = soup.find_all('img',{'id':'verify_img'})
        link = pattern[0]
        link = str(link)
        pattern = re.compile('src=[^\s]*')
        body = re.findall(pattern,link)

        response = body[0].strip()
        response = response[5:-2]
        img_url = 'https://mp.weixin.qq.com' + response
        print(img_url)

        #get_code(img_url)
        body = driver.find_element_by_id("verify_img").text
        print(body)
        with open('file.jpg', 'wb') as file:  # 以byte形式将图片数据写入
            file.write(body)
            file.flush()

        file.close()
        time.sleep(0.2)

        result = get_value()

        pattern = re.compile('cert=[^\s]*')
        response = re.findall(pattern, img_url)
        cert = response[0]
        cert = str(cert)
        cert = cert[5:]
        print('cert=' + cert)

        #items = test(result,cert,link_url)
        driver.find_element_by_id("input").send_keys(result)
        driver.find_element_by_id("bt").click()
        print(driver.page_source)

        #return items

    else:
        # 微信号名称
        try:
            name_list = response.xpath('/html/body/div/div[1]/div[1]/div[1]/div/strong/text()')
            name = name_list[0].strip()
            print(name)
        except:
            return

        # 微信号id
        try:
            id_list = response.xpath('/html/body/div/div[1]/div[1]/div[1]/div/p/text()')
            id = id_list[0].strip()
            id = id[4:].strip()
            print(id)
        except:
            id = 'None'

        # 微信唯一标识biz
        script_list = response.xpath('/html/body/script/text()')
        print(script_list)
        n = len(script_list)
        biz = script_list[n - 1]
        print(biz)
        # biz_list = response.xpath('/html/body/script[8]/text()')
        # for biz in biz_list:
        biz = biz
        print(biz)
        print(biz.strip())
        biz = biz[21:37]
        print(biz)

        items = {
            'user_name': name,
            'user_id': id,
            'biz': biz
        }

        return items

def test(result,cert,link_url):
    ua = UserAgent()
    value = result
    cert = cert
    data = {
        "cert": str(cert),
        "input": value,
        "appmsg_token": "",
    }

    headers = {
        #"User-Agent": ua.random,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
        "Host": "mp.weixin.qq.com",
        "Connection": "keep-alive",
        "Content-Length": "47",
        "Origin": "https://mp.weixin.qq.com",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": link_url,
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "pgv_pvi=3951376384; pgv_pvid=5654839444; pt2gguin=o2114246631; RK=RvgJ6q1FZ1; ptcz=1ae8b06580dbebbe46069f5d0d9ce8e59dd5567840ee6e8f8714f7877a7af293; ua_id=T1mjsmJJVV5AiXisAAAAALfEVbc7XEOwQE7O1ej30R0=; mm_lang=zh_CN; rewardsn=; wxtokenkey=777; sig=h0193f18617eb218e3a24f4a303cf1dff628581bfd45d2a9957fd290ceaf9bbd6cc93785a6a12dcaed7"
    }
    url = 'https://mp.weixin.qq.com/mp/verifycode'
    body = requests.post(url, data=data, headers=headers, verify=False).text
    print(body)
    response = etree.HTML(body)

    # 微信号名称
    try:
        name_list = response.xpath('/html/body/div/div[1]/div[1]/div[1]/div/strong/text()')
        name = name_list[0].strip()
        print(name)
    except:
        return

    # 微信号id
    try:
        id_list = response.xpath('/html/body/div/div[1]/div[1]/div[1]/div/p/text()')
        id = id_list[0].strip()
        id = id[4:].strip()
        print(id)
    except:
        id = 'None'

    # 微信唯一标识biz
    script_list = response.xpath('/html/body/script/text()')
    print(script_list)
    n = len(script_list)
    biz = script_list[n - 1]
    print(biz)
    # biz_list = response.xpath('/html/body/script[8]/text()')
    # for biz in biz_list:
    biz = biz
    print(biz)
    print(biz.strip())
    biz = biz[21:37]
    print(biz)

    items = {
        'user_name': name,
        'user_id': id,
        'biz': biz
    }

    return items

def get_code(img_url):
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
    }
    url = img_url
    body = requests.get(url, headers=headers, verify=False).content
    print(body)

    with open('file.jpg', 'wb') as file:  # 以byte形式将图片数据写入
        file.write(body)
        file.flush()

    file.close()

def get_value():
    # 用户名
    username = 'secret'
    # 密码
    password = 'secret'
    # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appid = 1
    # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appkey = '22cc5376925e9387a23cf797cb9ba745'
    # 图片文件
    filename = 'file.jpg'
    # 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
    codetype = 1004
    # 超时时间，秒
    timeout = 60

    # 检查
    if (username == 'username'):
        print('请设置好相关参数再测试')
    else:
        # 初始化
        yundama = YDMHttp(username, password, appid, appkey)

        # 登陆云打码
        uid = yundama.login()
        print('uid: %s' % uid)

        # 查询余额
        balance = yundama.balance()
        print('balance: %s' % balance)

        # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
        cid, result = yundama.decode(filename, codetype, timeout)
        print('cid: %s, result: %s' % (cid, result))
        return result

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
        time.sleep(0.1)

    db.close()
