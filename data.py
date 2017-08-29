#-*- coding: utf-8 -*-

from tables   import query_user_db, query_dish_by_day_db, write_dish_db
from tables   import delete_dish_by_id_db, query_comments_by_dish_id_db
from tables   import query_dish_by_id_db, write_comment_db, update_password_db
from tables   import update_personal_info_db, query_user_by_id_db, query_user_all_db
from tables   import update_user_by_id_db, add_user_db, delete_user_by_id_db
from tables   import write_order_db, query_all_orders_db, query_orders_by_uid_db
from tables   import query_dish_by_ids_db

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

def write_dish(name, pic, time, material, kind, price, unit):
    write_dish_db(name, pic, time, material, kind, price, unit)

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

def write_order(uid, did, num, price, unit, get_time):
    r          = write_order_db(uid, did, num, price, unit, None, get_time, None)
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
