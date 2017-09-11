#-*- coding: utf-8 -*-

import time

from sqlalchemy import Column, String, Integer, Date, TIMESTAMP, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from conf import conf
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# 创建对象的基类:
Base = declarative_base()

class User(Base):
# 表的名字:
    __tablename__ = conf.t_user
    def __init__(self, i, n, m, g, u, t, a):
        self.id            = i
        self.name          = n
        self.mobile        = m
        self.gender        = g
        self.userid        = u
        self.telephone     = t
        self.avatar        = a
    def dic_return(self):
        return {'id': self.id, 'name':str(self.name), 
                'mobile': str(self.mobile), 'gender': str(self.gender),
                'userid': str(self.userid), 'telephone': str(self.telephone),
                'avatar': self.avatar}
# 表的结构:
    #用户的id
    id                = Column(Integer, primary_key=True)
    #用户真实名字
    name              = Column(String(64))
    #mobile_phone
    mobile            = Column(String(32))
    #0=female 1=male
    gender            = Column(String(2))
    #userid
    userid            = Column(String(64))
    #telephone
    telephone         = Column(String(32))
    #avatar
    avatar            = Column(String(256))

class Dish(Base):
# 表的名字:
    __tablename__ = conf.t_dish
    def __init__(self, i, name, pic, time, m, k, pr, u, score, num):
        self.id             = i
        self.name           = name
        self.pic_loc        = pic
        self.time           = time
        self.material       = m
        self.kind           = k
        self.price          = pr
        self.unit           = u
        self.score          = score
        self.num            = num
    def dic_return(self):
        return {'id':self.id, 'name':str(self.name), 'pic_loc':str(self.pic_loc),
                'time':str(self.time), 'material':str(self.material),
                'kind':self.kind, 'price':self.price, 'unit': str(self.unit),
                'score': self.score, 'num': self.num }
# 表的结构:
    #图片的id
    id          = Column(Integer, primary_key=True)
    #图片的名字
    name        = Column(String(128))
    #图片存储的位置
    pic_loc     = Column(String(256))
    #图片上传的时间
    time        = Column(Date)
    #菜的食材
    material    = Column(String(128))
    #菜的类型
    kind        = Column(Integer)
    #菜的价格
    price       = Column(Integer)
    #菜的单位
    unit        = Column(String(8))
    #菜的总分
    score       = Column(Integer)
    #菜的评价次数
    num         = Column(Integer)

class Order(Base):
    __tablename__ = conf.t_order
    def __init__(self, i, mo, di, nu, pr, un, t, t1, t2, c, p):
        self.id            = i
        self.mobile        = mo
        self.dish_id       = di
        self.num           = nu
        self.price         = pr
        self.unit          = un
        self.time          = t
        self.time1         = t1
        self.time2         = t2
        self.confirm       = c
        self.pay_status    = p
    def dic_return(self):
        return {'id': self.id, 'mobile': self.mobile, 'dish_id': self.dish_id,
                'num':self.num, 'price': self.price, 'unit': self.unit, 
                'time':str(self.time), 'time1': str(self.time1), 'time2': str(self.time2),
                'confirm':self.confirm, 'pay_status': self.pay_status}
    id          = Column(Integer, primary_key=True)
    mobile      = Column(Integer)
    dish_id     = Column(Integer)
    num         = Column(Integer)
    price       = Column(Integer)
    unit        = Column(Integer)
    time        = Column(TIMESTAMP) #下单的时间
    time1       = Column(TIMESTAMP) #预计取食品的时间
    time2       = Column(TIMESTAMP) #实际取食品的时间
    confirm     = Column(Integer)
    pay_status  = Column(Integer)

class Comment(Base):
    __tablename__ = conf.t_comment
    def dic_return(self):
        return {'id': self.id, 'dish_id': self.dish_id, 'mobile': self.mobile,
                'stars': self.stars, 'time': str(self.time), 'content': str(self.content)}
    #comment的id
    id          = Column(Integer, primary_key=True)
    dish_id     = Column(Integer)
    mobile      = Column(String(16))
    stars       = Column(Integer)
    time        = Column(TIMESTAMP)
    content     = Column(String(512))

    def __init__(self, i, di, mo, st, co):
        t = time.localtime();
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", t)
        self.id           = i
        self.dish_id      = di
        self.mobile       = mo
        self.stars        = st
        self.time         = timestamp
        self.content      = co

# 初始化数据库连接:
db_url = 'mysql+mysqlconnector://' + str(conf.db_user) + ':ygb1canteen2017@localhost:' + str(conf.db_port) + '/' + conf.db_db
engine = create_engine(db_url, encoding=conf.db_encode)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

def write_user_db(name, mobile, gender, userid, telephone, avatar):
    S      = DBSession()
    r      = S.query(User).filter(User.mobile == mobile).first()
    if not r:
        u  = User(0, name, mobile, gender, userid, telephone, avatar)
        S.add(u)
        S.commit()
    else:
        D = {User.name:name, User.mobile:mobile, User.gender:gender,
             User.telephone:telephone, User.avatar:avatar}
        r = S.query(User).filter(User.mobile == mobile).update(D)
        S.commit()
    S.close()
    return True

def query_all_users_db():
    S     = DBSession()
    r     = S.query(User).all()
    S.close()
    return [] if not r else [e.dic_return() for e in r]

def query_dish_by_day_db(day):
    S     = DBSession()
    r     = S.query(Dish).filter(Dish.time == day).all()
    S.close()
    return [] if not r else [e.dic_return() for e in r]

def query_dish_by_id_db(did):
    S     = DBSession()
    r     = S.query(Dish).filter(Dish.id == did).first()
    S.close()
    return {} if not r else r.dic_return()

def query_comments_by_dish_id_db(did):
    S     = DBSession()
    r     = S.query(Comment).filter(Comment.dish_id == did).all()
    S.close()
    print('query_comments_by_dish_id_db', r)
    return [] if not r else [e.dic_return() for e in r]

def write_dish_db(name, pic_loc, day, material, kind, price, unit):
    S = DBSession()
    d     = Dish(0, name, pic_loc, day, material, kind, price, unit, 0, 0)
    S.add(d)
    S.commit()
    S.close()
    return True

def write_comment_db(mobile, num, cnt, did):
    S = DBSession()
    c = Comment(0, did, mobile, num, cnt)
    S.add(c)
    S.commit()
    S.close()
    return True
