#coding = utf-8

from pymysql import *
import redis

'''
微信公众号号主提取：从Redis到MySQL
'''

#从redis中获取去重后的微信公众号
def redis_set(name,biz):
    pipe.set(biz,name)
    pipe.execute()

#保存进MySQL
def get_key(v,k):
    params = [v, k]
    sql = """insert into wechat(userName,biz) VALUE(%s,%s)"""
    try:
        conn.execute(sql, params)
        db.commit()
    except:
        db.rollback()

if __name__ == "__main__":
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
    r = redis.StrictRedis(connection_pool=pool)
    pipe = r.pipeline(transaction=False)

    db = connect(host="localhost", port=3306, db="spider", user="root", password="secret", charset="utf8")
    conn = db.cursor()
    
    #管道缓存
    pipe = r.pipeline()
    pipe_size = 100000

    len = 0
    key_list = []
    print(r.pipeline())
    keys = r.keys()
    for key in keys:
        key_list.append(key)
        pipe.get(key)
        if len < pipe_size:
            len += 1
        else:
            for (k, v) in zip(key_list, pipe.execute()):
                userName = v
                biz = k
                get_key(v,k)
            len = 0
            key_list = []

    for (k, v) in zip(key_list, pipe.execute()):
        userName = v
        biz = k
        get_key(v, k)
    print('ok')

    db.close()
