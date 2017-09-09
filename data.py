#-*- coding: utf-8 -*-

import time
from tables   import query_dish_by_day_db

from conf    import conf

def query_dish_by_day(day):
    r         = query_dish_by_day_db(day)
    return r
