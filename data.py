#-*- coding: utf-8 -*-

import time
from tables   import query_user_db, query_dish_by_day_db, write_dish_db
from tables   import delete_dish_by_id_db, query_comments_by_dish_id_db
from tables   import query_dish_by_id_db, write_comment_db, update_password_db
from tables   import update_personal_info_db, query_user_by_id_db, query_user_all_db
from tables   import update_user_by_id_db, add_user_db, delete_user_by_id_db
from tables   import write_order_db, query_all_orders_db, query_orders_by_uid_db
from tables   import query_dish_by_ids_db, query_user_by_ids_db, order_confirm_db
from tables   import query_order_by_dish_id_db, query_already_ordered_db

from conf    import conf
def query_user(name, password):
    r          = {}
    if conf.s_cache == 1:
        pass
    if not r:
        r      = query_user_db(name, password)
    return r

def query_user_by_id(uid):
    r          = {}
    if conf.s_cache == 1:
        pass
    if not r:
        r      = query_user_by_id_db(uid)
    return r

def query_dish_by_day(day):
    r          = []
    if conf.s_cache == 1:
        pass
    if not r:
        r      = query_dish_by_day_db(day)
    return r

def write_dish(name, pic, tm, material, kind, price, unit):
    write_dish_db(name, pic, tm, material, kind, price, unit)

def delete_dish_by_id(did):
    delete_dish_by_id_db(did)

def query_comments_by_dish_id(did):
    r          = []
    if conf.s_cache == 1:
        pass
    if not r:
        r      = query_comments_by_dish_id_db(did)
    return r

def query_dish_by_id(did):
    r          = {}
    if conf.s_cache == 1:
        pass
    if not r:
        r      = query_dish_by_id_db(did)
    return r

def write_comment(did, uid, r_name, n_name, r_img, n_img, stars, words):
    r          = {}
    if conf.s_cache == 1:
        pass
    if not r:
        r      = write_comment_db(did, uid, r_name, n_name, r_img, n_img, stars, words)

def update_password(uid, old_pass, new_pass):
    r          = update_password_db(uid, old_pass, new_pass)
    return r

def update_personal_info(uid, r_name, n_name, r_img, n_img, o_phone, m_phone):
    r          = update_personal_info_db(uid, r_name, n_name, r_img, n_img, o_phone, m_phone)
    return r

def query_user_all():
    r          = query_user_all_db()
    return r

def update_user_by_id(uid, r_name, n_name, o_phone, m_phone, password, role):
    r          = update_user_by_id_db(uid, r_name, n_name, o_phone, m_phone, password, role)
    return r

def add_user(r_name, n_name, o_phone, m_phone, password, role):
    r          = add_user_db(r_name, n_name, o_phone, m_phone, password, role)
    return r

def delete_user_by_id(uid):
    r          = delete_user_by_id_db(uid)
    return r

def write_order(uid, did, num, price, unit):
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    gt = time.strftime('%Y-%m-%d', time.localtime(time.time() + 3600*24))
    gt = gt + ' ' + str(conf.fetch_time)
    r          = write_order_db(uid, did, num, price, unit, t, gt, None)
    return r

def query_all_orders():
    r          = query_all_orders_db()
    return r

def query_orders_by_uid(uid):
    r          = query_orders_by_uid_db(uid)
    return r

def query_dish_by_ids(ids):
    r          = query_dish_by_ids_db(ids)
    return r

def query_user_by_ids(ids):
    r          = query_user_by_ids_db(ids)
    d          = {}
    for e in r:
        d[e['id']] = e
    return d

def order_confirm(oid):
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    r          = order_confirm_db(oid, t)
    return r

def query_order_by_dish_id(did):
    r          = query_order_by_dish_id_db(did)
    return r

def query_already_ordered(uid, did):
    r          = query_already_ordered_db(uid, did)
    return r
