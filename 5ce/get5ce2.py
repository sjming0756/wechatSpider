# -*- coding:utf-8 -*-

import requests
from lxml import etree
import re
from pymysql import *
import time
from bs4 import BeautifulSoup
import json

'''
微信公众号号主抓取，主要抓取公众号唯一标识biz,网站：http://www.5ce.com
主要通过搜索分词的方式，对公众号进行搜索，此网站需要登录
'''

def rearch_5ce(keyword):
    headers = {
        'Host': 'www.5ce.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Origin': 'http://www.5ce.com',
        'X-CSRF-TOKEN': 'CfDJ8A8trPnvhYhOgjBnKrfrdaAXzcoRJno-RQRUJwZlqgJ7BRFz5c5wUhSU-oAy-ZSR6np6MJWnyd1G6WCYvExDBBZ05RKzEq0V6-zsSlUvjPMIrX-WSBXRXJaViESKluAsi9p6gYQZh2VScbee1fzrCQqCpoQDb6OtkRri0h1KP5WZHA1qx7e_wSaXVuj4dPCYhw',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '.5ce.session=614024d4-875d-4847-9c84-2e06e3b44c31; Hm_lvt_2d56acf42b4056540e59888ab8e03687=1535528811; Hm_lvt_a38000c86c99ba91fdd1ebad27fc0902=1535528811; .AspNetCore.Cookies=CfDJ8A8trPnvhYhOgjBnKrfrdaBLocwGmIUjOv7Sks2qjuVhx1sUYlaoZC93lj9ojsRdPiEwAg45sC-wKTvlJS5g5CKzPM5fbL6aV00xmgXHTITGYTv4376bWz7d9PlvXcDls8ITsGAC-KfRZrDmZ2L-_sktsKWwVF_28SfDxhBELQvLIe_aOOzaX1gMmVDyRp6fZHuXcMrEgUJWG3n7qbc315_ZUewrNA7TmK7cHgTMO_tYINAn2o0fO-oqO321Mzs8hB5L6N0Y-pwvYAivrmagLuhpAEbslxkpinpZSzT5WPpjJFRQ22NndH1jkB-xzgDJk-UJGcZhcr4RDd5rYeNIRkA3TiT9fgury4uBa1IockOepByfLDQpGEt-Dny5oUR9cH5rTQG6AhwIu45PtLehTVkiPOYm6QaNfc_CPI1Uv0WJpHnvwoGQKTELwGMSfgQhsODBOGU5_gIAoq-RRQakNbR6C2dEk8eOmHkLt0JXkNfuCTgIFKP_Q4wCg2MWE9yP4KQNUKTADiSVl4TIXo1wixUBuOZAbRaBpws2BEwH-0d1lI6La6DCUXWpxTtWOrjCkqm3bgWbLNtxEm9XKzgMIJ_I-Cgd6J7KhJ6kPy_VH9OkZs4XgHVoC3J2_19kBeoBta4RGGJZI2o2y8OEb6QcanE; .AspNetCore.Antiforgery.ixigDfNCJGc=CfDJ8A8trPnvhYhOgjBnKrfrdaCUJtvCiNZw7dxSQFHvnGBQgkfmmx1ZgBtxxLmUzodbw1aUNTZX68yijtozn6XzV4fmSt1WdZpVWW4jiWGV2en-YPSuvh5YSi_OLC2F1SZMwhdRncEixjnR941hAf3TfEg; Hm_lpvt_2d56acf42b4056540e59888ab8e03687=1535702767; Hm_lpvt_a38000c86c99ba91fdd1ebad27fc0902=1535702768'
    }
    payload = {"resourcePlatformGuid": "",
               "keywordsList": keyword,
               "catalogGuid": "",
               "authorGuid": "",
               "issueTimeStart": "",
               "issueTimeEnd": "",
               "readCountMin": -999,
               "readCountMax": -999,
               "titleLikeString": "",
               "articleContentLikeString": "",
               "articleContentNotlikeString": "",
               "isKOL": -999,
               "isOriginal": -999,
               "orderByColumn": "issueTime",
               "pageIndex": 1,
               "dateRange": "",
               "dataType": "dataList"
            }

    url = 'http://www.5ce.com/api/sucai/search'
    body = requests.post(url, data=json.dumps(payload), headers=headers).text #post请求 
    
def get_5ce(i,keyword):
    headers = {
        'Host': 'www.5ce.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Origin': 'http://www.5ce.com',
        'X-CSRF-TOKEN': 'CfDJ8A8trPnvhYhOgjBnKrfrdaAXzcoRJno-RQRUJwZlqgJ7BRFz5c5wUhSU-oAy-ZSR6np6MJWnyd1G6WCYvExDBBZ05RKzEq0V6-zsSlUvjPMIrX-WSBXRXJaViESKluAsi9p6gYQZh2VScbee1fzrCQqCpoQDb6OtkRri0h1KP5WZHA1qx7e_wSaXVuj4dPCYhw',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '.5ce.session=614024d4-875d-4847-9c84-2e06e3b44c31; Hm_lvt_2d56acf42b4056540e59888ab8e03687=1535528811; Hm_lvt_a38000c86c99ba91fdd1ebad27fc0902=1535528811; .AspNetCore.Cookies=CfDJ8A8trPnvhYhOgjBnKrfrdaBLocwGmIUjOv7Sks2qjuVhx1sUYlaoZC93lj9ojsRdPiEwAg45sC-wKTvlJS5g5CKzPM5fbL6aV00xmgXHTITGYTv4376bWz7d9PlvXcDls8ITsGAC-KfRZrDmZ2L-_sktsKWwVF_28SfDxhBELQvLIe_aOOzaX1gMmVDyRp6fZHuXcMrEgUJWG3n7qbc315_ZUewrNA7TmK7cHgTMO_tYINAn2o0fO-oqO321Mzs8hB5L6N0Y-pwvYAivrmagLuhpAEbslxkpinpZSzT5WPpjJFRQ22NndH1jkB-xzgDJk-UJGcZhcr4RDd5rYeNIRkA3TiT9fgury4uBa1IockOepByfLDQpGEt-Dny5oUR9cH5rTQG6AhwIu45PtLehTVkiPOYm6QaNfc_CPI1Uv0WJpHnvwoGQKTELwGMSfgQhsODBOGU5_gIAoq-RRQakNbR6C2dEk8eOmHkLt0JXkNfuCTgIFKP_Q4wCg2MWE9yP4KQNUKTADiSVl4TIXo1wixUBuOZAbRaBpws2BEwH-0d1lI6La6DCUXWpxTtWOrjCkqm3bgWbLNtxEm9XKzgMIJ_I-Cgd6J7KhJ6kPy_VH9OkZs4XgHVoC3J2_19kBeoBta4RGGJZI2o2y8OEb6QcanE; .AspNetCore.Antiforgery.ixigDfNCJGc=CfDJ8A8trPnvhYhOgjBnKrfrdaCUJtvCiNZw7dxSQFHvnGBQgkfmmx1ZgBtxxLmUzodbw1aUNTZX68yijtozn6XzV4fmSt1WdZpVWW4jiWGV2en-YPSuvh5YSi_OLC2F1SZMwhdRncEixjnR941hAf3TfEg; Hm_lpvt_2d56acf42b4056540e59888ab8e03687=1535702767; Hm_lpvt_a38000c86c99ba91fdd1ebad27fc0902=1535702768'
    }

    payload = {"resourcePlatformGuid":"26ef1325-59fb-e711-b201-d4ae52d0f72c",
            "keywordsList":keyword,
            "catalogGuid":"",
            "authorGuid":"",
            "issueTimeStart":"",
            "issueTimeEnd":"",
            "readCountMin":-999,
            "readCountMax":-999,
            "titleLikeString":"",
            "articleContentLikeString":"",
            "articleContentNotlikeString":"",
            "isKOL":-999,
            "isOriginal":-999,
            "orderByColumn":"issueTime",
            "pageIndex":i,
            "dateRange":[]}


    url = 'http://www.5ce.com/api/sucai/filter?dataType=dataList'
    body = requests.post(url,data=json.dumps(payload),headers=headers).text #post请求

    response = json.loads(body)
    print(response)

    #匹配文章链接
    data_list = response['data']
    for i in range(len(data_list)):
        data = data_list[i]
        link = data['url']
        print(link)
        items = get_biz(link)
        save_biz(items)
        time.sleep(0.3)

def get_biz(url):
    headers = {
        'Host': 'mp.weixin.qq.com',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'pgv_pvi=3951376384; pgv_pvid=5654839444; pt2gguin=o2114246631; RK=RvgJ6q1FZ1; ptcz=1ae8b06580dbebbe46069f5d0d9ce8e59dd5567840ee6e8f8714f7877a7af293; ua_id=T1mjsmJJVV5AiXisAAAAALfEVbc7XEOwQE7O1ej30R0=; mm_lang=zh_CN; rewardsn=; wxtokenkey=777; sig=h014565c6eceeceb2445044acfff5941cd035ede17b7692d75f4827eea625ce816fbc833ed5a7820175; pgv_info=ssid=s7297622360'
    }

    body = requests.get(url, headers=headers, verify=False).text
    response = etree.HTML(body)
    time.sleep(0.2)
    print(response)

    #url = response.find_all('span',{'class':'soucre'})
    #data = str(data)
    #print(data)

    # 获取微信号名称
    try:
        name_list = response.xpath('//*[@id="js_name"]/text()')
        print(name_list)
        name = name_list[0]
        name = name.strip()
        print(name)
    except:
        return

    # 获取微信号id
    id = 'None'

    # 获取微信参数_biz
    script_list = response.xpath('//*[@id="activity-detail"]/script[1]/text()')
    print(script_list)
    biz = script_list[0]
    biz = biz.strip()
    biz = biz[15:31]
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

    keyword = "延禧攻略"
    rearch_5ce(keyword)
    for i in range(1,26):
        get_5ce(i,keyword)
        time.sleep(0.5)

    db.close()
