#-*- coding: utf-8 -*-

import time
from tables   import query_dish_by_day_db, query_dish_by_id_db
from tables   import write_dish_db, query_comments_by_dish_id_db
from tables   import query_all_users_db, write_user_db, write_comment_db
from tables   import delete_dish_by_id_db, update_dish_db
from tables   import query_reserve_by_day_db, query_dish_by_ids_db
from tables   import query_user_by_mobile_db, write_order_db, query_user_by_mobiles_db
from tables   import query_order_by_mobile_db, delete_order_db
from tables   import query_order_left_db, query_order_middle_db, query_order_right_db
from tables   import orderconfirm_db

from conf    import conf

def write_user(mobile, u):
    name      = u['name']
    mobile    = u['mobile']
    gender    = u['gender']
    userid    = u['userid']
    teleph    = u['telephone']
    avatar    = u['avatar']
    r         = write_user_db(name, mobile, gender, userid, teleph, avatar)
    return r

def query_dish_by_day(day):
    r         = query_dish_by_day_db(day)
    return r

def query_dish_by_id(did):
    r         = query_dish_by_id_db(did)
    return r

def query_comments_by_dish_id(did):
    r         = query_comments_by_dish_id_db(did)
    return r

def write_dish(name, pic_loc, day, material, kind, price, unit):
    r         = write_dish_db(name, pic_loc, day, material, kind, price, unit)
    return r

def write_comment(mobile, num, cnt, did):
    r         = write_comment_db(mobile, num, cnt, did)
    return r

def query_all_users():
    r         = query_all_users_db()
    u         = {}
    for e in r:
        u[e['mobile']] = e
    return u

def delete_dish_by_id(did):
    r         = query_comments_by_dish_id(did)
    if not r:
        r     = delete_dish_by_id_db(did)
        return r
    else:
        return False

def update_dish(did, name, pic_loc, day, material, kind, price, unit):
    r         = update_dish_db(did, name, pic_loc, day, material, kind, price, unit)
    return r

def query_reserve(t, p):
    r     = []
    if t == 'day':
        r = query_reserve_by_day_db(p)
    return r

def query_dish_by_ids(ids):
    r     = query_dish_by_ids_db(ids)
    return r

def query_user_by_mobile(mobile):
    r     = query_user_by_mobile_db(mobile)
    return r

def query_user_by_mobiles(mobiles):
    r     = query_user_by_mobiles_db(mobiles)
    return r

def write_order(user, data, dishes, day):
    r     = write_order_db(user, data, dishes, day)
    return r

def query_order_by_mobile(mobile):
    r     = query_order_by_mobile_db(mobile)
    return r

def delete_order(oid):
    r     = delete_order_db(oid)
    return r

def query_order_left():
    return query_order_left_db()

def query_order_middle():
    a, b, o = query_order_middle_db()
    return a, b, o

def query_order_right():
    return query_order_right_db()

def orderconfirm(orderid):
    r = orderconfirm_db(orderid)
    return r

def query_today_order():
    r      =  query_today_order_db()
    return r

from tornado.httpclient import AsyncHTTPClient
import sys, urllib
def notify(mobile, cnt):
    def response(res):
        pass
    url = "http://localhost:8000/msgsend?mobile=%s&content=%s"%(mobile, cnt)
    http_client = AsyncHTTPClient()
    http_client.fetch(url, response)

def check_and_notify():
    t     = time.localtime()
    h     = int(time.strftime("%H", t))
    m     = int(time.strftime("%M", t))
    if m == 0:
        return 0
    if h == conf.notify_hour and m <= conf.notify_min:
        ids, O, mobile = query_order_left_db()
        if len(O) == 0:
            return 0
        for o in O:
            oid    = o['oid']
            mobile = o['mobile']
            cnt    = str(oid)
            notify(mobile, cnt)
    else:
        pass

'''
now='2017-10-25'
'''
def get_next_week(now):
    import datetime
    from datetime import timedelta
    arr = now.split('-')
    arr = [int(e) for e in arr]
    d = datetime.datetime(arr[0], arr[1], arr[2])
    n = d.weekday()

    #n = 1 if n == 0 else 7-n
    aDay = timedelta(days=6-n)
    d = d + aDay
    res = []
    for i in xrange(7):
        aDay = timedelta(days=1+i)
        t = d + aDay
        res.append(t.strftime("%Y-%m-%d"))
    return res
if __name__ == "__main__":
    r = get_next_week('2017-10-30')
    print(r)
