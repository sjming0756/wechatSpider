# -*- coding:utf-8 -*-

import requests
from lxml import etree
import re
from pymysql import *
import time
from bs4 import BeautifulSoup

'''
微信公众号号主抓取，抓取网站http://www.5ce.com
此网站需要登录，并且只能抓取10页，公众号号主不是很全，一般只能抓最新发布文章的号主
'''

def get_5ce(i):
    headers = {
        'Host':'www.5ce.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'X-CSRF-TOKEN': 'CfDJ8A8trPnvhYhOgjBnKrfrdaCZSxhRLvlvtlQp0wX39OSLHL04kRz6syNchXAi9qXmFhpulrIo1ypazheqRpCRSMKBef5bZjtT57EoewHTyfmbWS3Ti9tSo_65e35cTxhfgArA22O0rWD59RIG686oNlA8bH3CsysA5JH09Ck9TtN2oH3WXduFU2YgMVjky_rLTw',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '.5ce.session=614024d4-875d-4847-9c84-2e06e3b44c31; Hm_lvt_2d56acf42b4056540e59888ab8e03687=1535528811; Hm_lvt_a38000c86c99ba91fdd1ebad27fc0902=1535528811; .AspNetCore.Cookies=CfDJ8A8trPnvhYhOgjBnKrfrdaBTsA4XsbbN8XijzXSFS2fP5_V0iKsaDvM63udwxentFsDVPuBoCiHiwfBxK5_JO3MOdrZEC9J6KQQILlWYRlwutXxbgDVPkkiuPC697SZ1vywkRN5QLRIemGa3YjA4M8-P2Fb3TfCaFSWBoBTzB3kjSMGRYoKyxrhNqdQboQsyu0oYOTYpF3KBjPqZiNzKENaX8L6rRCTI48oiQsvk6_OxcQcbCvEadJkh8waWN-7tkJuUiweQxYNNBB6u0VVlBBU33El0ALiFPOxgrFuar8Uf7KWjs2Ggmfe6nP-CTx1N5lJxK42fU75PkV8Ts0l2N3X0_ax_SBKW7f7Hx_jw_JpY1InJcKOFaqh_UxPXnux1i8FHM7xpAbiv-hVBDFa2Ai-lOf3PZqS9C7IPqcd15ci3XraKi-jNDcclVf2OQ2eJaZTdLRUBgpfUVf020EWAOs9yHu8lH0uM_edMTYTKUXHf2eW_DDjsBAxACJPnUNgbAnv37n_18CKpljKKrB69qnyRa1U647hm3dKaKEBqrKPalArJbrMSo-en3vS0Fv9KdraNem54CI6XF-2oRZhZb1eJd1dp7fmzwvScU4hEpiIaiFCgqLwg-840fxkx_HC3aktBtaX6aYSh3O1pWa87JEI; .AspNetCore.Antiforgery.ixigDfNCJGc=CfDJ8A8trPnvhYhOgjBnKrfrdaDfpwNrli7V21WAoIlP5o2vUSzzbzqejUPkQsYe_CCkJT61CC6mSKSh7thdNYQ9FHt4I5VRACXPAiu8kECUlJgVWTTFtTj7iryKJ9oDisQmQPRI6n4rSfn7Q_b74O4IcHk; Hm_lpvt_2d56acf42b4056540e59888ab8e03687=1536216327; Hm_lpvt_a38000c86c99ba91fdd1ebad27fc0902=1536216327'
    }
    
    url = 'http://www.5ce.com/hots/data?name=weixin&rank=wxrw&rankGuid=a1db899f-4e32-e811-b201-d4ae52d0f72c&sort=sortindex&sortType=DESC&catalogId=all&pageIndex=' + str(i)
    body = requests.get(url,headers=headers,verify=False).text
    response = etree.HTML(body)

    #匹配文章链接
    #url_list = response.xpath('//*[@id="app"]/div[2]/section/div[1]/div[2]/div[3]/div[2]/div/div[1]/dl//a/@href')
    pattern = re.compile('href="/[^\s]*')
    url_list = re.findall(pattern,body)
    #print(url_list)
    for url in url_list:
        url = url[6:-1]
        link = 'http://www.5ce.com' + url
        #print(link)
        items = get_biz(link)
        save_biz(items)
        time.sleep(0.5)

def get_biz(url):
    headers = {
        'Host': 'www.5ce.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'X-CSRF-TOKEN': 'CfDJ8A8trPnvhYhOgjBnKrfrdaCZSxhRLvlvtlQp0wX39OSLHL04kRz6syNchXAi9qXmFhpulrIo1ypazheqRpCRSMKBef5bZjtT57EoewHTyfmbWS3Ti9tSo_65e35cTxhfgArA22O0rWD59RIG686oNlA8bH3CsysA5JH09Ck9TtN2oH3WXduFU2YgMVjky_rLTw',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '.5ce.session=614024d4-875d-4847-9c84-2e06e3b44c31; Hm_lvt_2d56acf42b4056540e59888ab8e03687=1535528811; Hm_lvt_a38000c86c99ba91fdd1ebad27fc0902=1535528811; .AspNetCore.Cookies=CfDJ8A8trPnvhYhOgjBnKrfrdaBTsA4XsbbN8XijzXSFS2fP5_V0iKsaDvM63udwxentFsDVPuBoCiHiwfBxK5_JO3MOdrZEC9J6KQQILlWYRlwutXxbgDVPkkiuPC697SZ1vywkRN5QLRIemGa3YjA4M8-P2Fb3TfCaFSWBoBTzB3kjSMGRYoKyxrhNqdQboQsyu0oYOTYpF3KBjPqZiNzKENaX8L6rRCTI48oiQsvk6_OxcQcbCvEadJkh8waWN-7tkJuUiweQxYNNBB6u0VVlBBU33El0ALiFPOxgrFuar8Uf7KWjs2Ggmfe6nP-CTx1N5lJxK42fU75PkV8Ts0l2N3X0_ax_SBKW7f7Hx_jw_JpY1InJcKOFaqh_UxPXnux1i8FHM7xpAbiv-hVBDFa2Ai-lOf3PZqS9C7IPqcd15ci3XraKi-jNDcclVf2OQ2eJaZTdLRUBgpfUVf020EWAOs9yHu8lH0uM_edMTYTKUXHf2eW_DDjsBAxACJPnUNgbAnv37n_18CKpljKKrB69qnyRa1U647hm3dKaKEBqrKPalArJbrMSo-en3vS0Fv9KdraNem54CI6XF-2oRZhZb1eJd1dp7fmzwvScU4hEpiIaiFCgqLwg-840fxkx_HC3aktBtaX6aYSh3O1pWa87JEI; .AspNetCore.Antiforgery.ixigDfNCJGc=CfDJ8A8trPnvhYhOgjBnKrfrdaDfpwNrli7V21WAoIlP5o2vUSzzbzqejUPkQsYe_CCkJT61CC6mSKSh7thdNYQ9FHt4I5VRACXPAiu8kECUlJgVWTTFtTj7iryKJ9oDisQmQPRI6n4rSfn7Q_b74O4IcHk; Hm_lpvt_2d56acf42b4056540e59888ab8e03687=1536216327; Hm_lpvt_a38000c86c99ba91fdd1ebad27fc0902=1536216327'
    }

    body = requests.get(url, headers=headers, verify=False).text
    response = BeautifulSoup(body,'lxml')
    time.sleep(0.1)
    #print(response)

    url = response.find_all('span',{'class':'soucre'})
    data = url[0]
    data = str(data)
    print(data)

    # 获取微信号名称
    pattern = re.compile('[\u4e00-\u9fa5]+')
    soup = re.findall(pattern,data)
    name = soup[0]
    name = name.strip()
    print(name)

    # 获取微信号id
    id = 'None'

    # 获取微信参数_biz
    pattern = re.compile('href="[a-zA-z]+://[^\s]*')
    soup = re.findall(pattern, data)
    href = soup[0]
    href = href.strip()
    url = href[6:-1]
    url = str(url)
    print(url)
    pattern = re.compile('biz=[^\s]*')
    soup = re.findall(pattern, url)
    soup = soup[0]
    soup = soup.strip()
    biz = soup[4:20]
    print(biz)

    items = {
        'user_name': name,
        'user_id': id,
        'biz': biz
    }

    return items

def save_biz(items):
    sql = """insert into 5ce_wechat(user_name,user_id,biz) values(%s,%s,%s)"""
    try:
        cursor.execute(sql, (
            items["user_name"], items["user_id"], items["biz"]))
        db.commit()
        print("success")
    except:
        db.rollback()

if __name__ == "__main__":
    db = connect(host="localhost", port=3306, db="spider", user="root", password="secret", charset="utf8")
    cursor = db.cursor()

    for i in range(1,10): #只能翻10页
        get_5ce(i)
        time.sleep(0.1)

    db.close()
