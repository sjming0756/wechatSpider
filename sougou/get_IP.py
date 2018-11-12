# -*- coding:utf-8 -*-

import requests

'''
调用快代理API接口动态实时获取IP
'''

#获取Ip
def getIp():
    print('================请求开始中==================')
    # 获取IP列表
    url = 'https://dps.kdlapi.com/api/getdps/?orderid=943170645710612&num=1&pt=1&ut=1&format=json&sep=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    }
    data = requests.get(url,headers=headers).text
    # 转成字典的形式
    data_dict = eval(data)
    try:
        ip_list = data_dict['data']['proxy_list']
        return ip_list
    except Exception:
        getIp()

def AddIp():
    ip_list = getIp()  # 获取IP
    if len(ip_list) < 1:
        while True:
            if len(ip_list)< 1:
                ip_list = getIp()
            else:
                return
    ip=ip_list[0]
    return ip
