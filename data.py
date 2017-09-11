#-*- coding: utf-8 -*-

import time
from tables   import query_dish_by_day_db, query_dish_by_id_db
from tables   import write_dish_db, query_comments_by_dish_id_db
from tables   import query_all_users_db, write_user_db, write_comment_db

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
    return r

user_cache = {}

def init_user_cache():
    r      = query_all_users()
    for u in r:
        user_cache[u['mobile']] = u

init_user_cache()

if __name__ == "__main__":
    print(user_cache)
