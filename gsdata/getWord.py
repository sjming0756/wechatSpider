# -*- coding:utf-8 -*-

import requests
import re
from pymysql import *

def test():
    url = 'https://gist.githubusercontent.com/indiejoseph/eae09c673460aa0b56db/raw/ac66c1900b048e3c72a4388b2304893ca3b9a571/%25E7%258E%25B0%25E4%25BB%25A3%25E6%25B1%2589%25E8%25AF%25AD%25E5%25B8%25B8%25E7%2594%25A8%25E8%25AF%258D%25E8%25A1%25A8.txt'
    body = requests.get(url,verify=False).text
    print(body)

    pattern = re.compile('[\u4e00-\u9fa5]*')
    soup = re.findall(pattern,str(body))

    letters = []
    for i in soup:
        if i != '':
            letters.append(i)
    letters_list = list(set(letters))

    for i in letters_list:

        items = {'word':i}

        sql = """insert into keywords01(word) values(%s)"""
        try:
            cursor.execute(sql, (
                items['word']))
            db.commit()
            print("success")
        except:
            db.rollback()

if __name__ == "__main__":
    db = connect(host="localhost", port=3306, db="spider", user="root", password="secret", charset="utf8")
    cursor = db.cursor()
    test()
    db.close()
