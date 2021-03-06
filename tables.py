#-*- coding: utf-8 -*-

import time

from sqlalchemy import Column, String, Integer, Date, TIMESTAMP, create_engine
from sqlalchemy.sql import and_, or_, not_
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

class PCUser(Base):
    __tablename__ = 'pcuser'
    id          = Column(Integer, primary_key=True)
    name        = Column(String(16))
    mobile      = Column(String(16))
    gender      = Column(String(2))
    password    = Column(String(16))

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
    def __init__(self, i, oi, mo, di, nu, pr, un, t, t1, t2, c, p):
        self.id            = i
        self.orderid       = oi
        self.mobile        = mo
        self.dish_id       = di
        self.num           = nu
        self.time          = t
        self.time1         = t1
        self.time2         = t2
        self.confirm       = c
        self.pay_status    = p
    def dic_return(self):
        return {'id': self.id, 'mobile': self.mobile, 'dish_id': self.dish_id,
                'orderid':str(self.orderid), 'time':str(self.time), 'num': self.num,
                'time1': str(self.time1), 'time2': str(self.time2),
                'confirm':self.confirm, 'pay_status': self.pay_status}
    id          = Column(Integer, primary_key=True)
    orderid     = Column(String(32))
    mobile      = Column(String(16))
    dish_id     = Column(Integer)
    num         = Column(Integer)
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

def check_pc_user(mobile, passwd):
    S      = DBSession()
    r      = S.query(PCUser).filter(PCUser.mobile == mobile).filter(PCUser.password == passwd).first()
    return False if not r else True

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

def query_user_by_mobile_db(mobile):
    if not mobile or mobile == '':
        return {}
    S     = DBSession()
    r     = S.query(User).filter(User.mobile == mobile).first()
    S.close()
    return {} if not r else r.dic_return()

def query_user_by_mobiles_db(mobiles):
    if len(mobiles) == 0:
        return []
    S     = DBSession()
    r     = S.query(User).filter(User.mobile.in_(mobiles)).all()
    S.close()
    return [] if not r else [e.dic_return() for e in r]


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

def update_dish_db(did, name, pic_loc, day, material, kind, price, unit):
    S = DBSession()
    D = {Dish.name:name, Dish.pic_loc:pic_loc, Dish.time:day, Dish.material:material, Dish.kind:kind, Dish.price:price, Dish.unit:unit}
    r = S.query(Dish).filter(Dish.id == did).update(D)
    S.commit()
    S.close()
    return r

def write_comment_db(mobile, num, cnt, did):
    S = DBSession()
    c = Comment(0, did, mobile, num, cnt)
    S.add(c)
    S.commit()
    S.close()
    return True

def delete_dish_by_id_db(did):
    S = DBSession()
    r = S.query(Dish).filter(Dish.id == did).delete(synchronize_session=False)
    r = S.commit()
    S.close()
    return True

def query_reserve_by_day_db(day):
    S = DBSession()
    r = S.query(Dish).filter(Dish.time == day).filter(Dish.kind == 0).order_by(Dish.time.desc()).all()
    S.close()
    return [] if not r else [e.dic_return() for e in r]

def query_reserve_by_user_id_db(mobile):
    S = DBSession()
    r = S.query(Dish).filter(Dish.mobile == mobile).all()
    S.close()
    return [] if not r else [e.dic_return() for e in r]

def query_reserve_by_reserve_id_db(oid):
    S = DBSession()
    r = S.query(Dish).filter(Dish.id == oid).all()
    S.close()
    return {} if not r else [e.dic_return() for e in r]

def query_dish_by_ids_db(dids):
    S = DBSession()
    r = S.query(Dish).filter(Dish.id.in_(dids)).all()
    S.close()
    return [] if not r else [e.dic_return() for e in r]

#data=[ [did, num], [did, num] ... ]
#dishes=[ {dish}, {dish}, ... ]
#user={user}
#day=预计取单时间
def write_order_db(user, data, dishes, day):
    t           = time.localtime()
    now         = time.strftime('%Y%m%d-%H%M%S', t)
    now1        = time.strftime('%Y-%m-%d %H:%M:%S', t)
    if now1 > day:
        return False
    name        = user['name']
    mobile      = user['mobile']
    S = DBSession()
    N = len(data[0])
    oid         = now + '-' + mobile
    for i in xrange(N):
        if data[1][i] == 0:
            continue;
        price   = dishes[i]['price']
        unit    = dishes[i]['unit']
        o       = Order(0, oid, mobile, data[0][i], data[1][i], price, unit, now1, day, '', 0, 0)
        S.add(o)
    r = S.commit()
    S.close()
    return True

#return: [ {'oid':oid,'list':[dish, dish,...]}, ... ]
def query_order_by_mobile_db(mobile):
    S = DBSession()
    r = S.query(Order).filter(Order.mobile == mobile).order_by(Order.time1, Order.time).all()
    S.close()
    if not r:
        return [], []
   
    dids = [e.dish_id for e in r]
    O = []
    d = {}
    for e in r:
        if not d.get(e.orderid):
            d[e.orderid] = [e.dic_return()]
        else:
            d[e.orderid].append(e.dic_return())
    for e in d:
        O.append({'oid':e, 'list':d[e]})
    S.close()
    return dids, O

def delete_order_db(oid):
    S = DBSession()
    r = S.query(Order).filter(Order.orderid == oid).delete(synchronize_session=False)
    S.commit()
    S.close()


def query_order_left_db():
    t          = time.localtime()
    now        = time.strftime('%Y-%m-%d', t)
    begin      = now + ' 00:00:00'
    end        = now + ' 23:59:59'
    S = DBSession()
    r = S.query(Order).filter(and_(Order.time1 > begin, Order.time1 < end, Order.confirm == 0)).order_by(Order.time).all()
    if not r:
        return [], [], []
    ids    = [e.dish_id for e in r]
    mobile = [e.mobile  for e in r]
    O      = []
    d = {}
    for e in r:
        if not d.get(e.orderid):
            d[e.orderid] = [e.dic_return()]
        else:
            d[e.orderid].append(e.dic_return())
    for e in d:
        O.append({'oid':e, 'mobile': d[e][0]['mobile'], 'list':d[e]})

    S.close()
    return ids, O, mobile

def query_order_right_db():
    t          = time.localtime()
    now        = time.strftime('%Y-%m-%d', t)
    begin      = now + ' 00:00:00'
    S = DBSession()
    r = S.query(Order).filter(and_(Order.time1 < begin, Order.confirm == 0)).order_by(Order.time).limit(conf.history_limit).all()
    if not r:
        return [], [], []
    ids    = [e.dish_id for e in r]
    mobile = [e.mobile  for e in r]
    O      = []
    d = {}
    for e in r:
        if not d.get(e.orderid):
            d[e.orderid] = [e.dic_return()]
        else:
            d[e.orderid].append(e.dic_return())
    for e in d:
        O.append({'oid':e, 'mobile': d[e][0]['mobile'], 'list':d[e]})
    S.close()
    return ids, O, mobile


def query_order_middle_db():
    t          = time.time()
    t          = t + 24*3600
    t          = time.localtime(t)
    now        = time.strftime('%Y-%m-%d', t)
    begin      = now + ' 00:00:00'
    end        = now + ' 23:59:59'
    S          = DBSession()
    r          = S.query(Order).filter(and_(Order.time1 >= begin,Order.time1 <= end, Order.confirm == 0)).all()
    S.close()
    if not r:
        return [], {}, []
    d          = {}
    ids        = []
    for e in r:
        if not d.get(e.dish_id):
            d[e.dish_id] = e.num
        else:
            d[e.dish_id] = d[e.dish_id] + e.num
    n = 0
    for e in d:
        n = n + d[e]
        ids.append(e)
    d['sum'] = n

    mobile = {}
    for e in r:
        if not mobile.get(e.mobile):
            mobile[e.mobile] = [e.dic_return()]
        else:
            mobile[e.mobile].append(e.dic_return())
    return ids, d, mobile


def orderconfirm_db(oid):
    S       = DBSession()
    t       = time.localtime()
    now        = time.strftime('%Y-%m-%d %H:%M:%S', t)
    S.query(Order).filter(Order.orderid == oid).update({Order.time2: now, Order.confirm:1})
    S.commit()
    S.close()
    return True

#only success if day_des is empty
def copy_dish_a_day(day_src, day_des):
    S       = DBSession()
    r       = S.query(Dish).filter(and_(Dish.time == day_des, or_(Dish.kind == 0x0000, Dish.kind == 0x0010))).all()
    if r:
        S.close()
        return False
    r       = S.query(Dish).filter(and_(Dish.time == day_src, or_(Dish.kind == 0x0000, Dish.kind == 0x0010))).all()
    if not r:
        S.close()
        return True
    for e in r:
        e.time = day_des
        e.score = 0
        e.num = 0
        S.add(e)
    S.commit()
    S.close()
    return True

def copy_a_day(src, des):
    S = DBSession()
    r = S.query(Dish).filter(and_(Dish.time == src, Dish.kind == 0x0000)).all()
    if not r:
        S.close()
        return True
    for e in r:
        o = Dish(0, e.name, e.pic_loc, des, e.material, e.kind, e.price, e.unit, 0, 0)
        S.add(o)
    S.commit()
    S.close()
    return True
def copy_a_breakfast(src, des):
    S = DBSession()
    r = S.query(Dish).filter(and_(Dish.time == src, Dish.kind == 0x0010)).all()
    if not r:
        S.close()
        return True
    for e in r:
        o = Dish(0, e.name, e.pic_loc, des, e.material, e.kind, e.price, e.unit, 0, 0)
        S.add(o)
    S.commit()
    S.close()
    return True
if __name__ == "__main__":
    copy_a_breakfast('2017-11-24', '2017-12-01')
'''
    src = ['2017-11-27', '2017-11-28', '2017-11-29','2017-11-30', '2017-12-01']
    des = [
            ['2017-12-04', '2017-12-05', '2017-12-06', '2017-12-07', '2017-12-08'],
            ['2017-12-11', '2017-12-12', '2017-12-13', '2017-12-14', '2017-12-15'],
            ['2017-12-18', '2017-12-19', '2017-12-20', '2017-12-21', '2017-12-22'],
            ['2017-12-25', '2017-12-26', '2017-12-27', '2017-12-28', '2017-12-29'],

            ['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04', '2018-01-05'],
            ['2018-01-08', '2018-01-09', '2018-01-10', '2018-01-11', '2018-01-12'],
            ['2018-01-15', '2018-01-16', '2018-01-17', '2018-01-18', '2018-01-19'],
            ['2018-01-22', '2018-01-23', '2018-01-24', '2018-01-25', '2018-01-26'],
            ['2018-01-29', '2018-01-30', '2018-01-31', '2018-02-01', '2018-02-02']
          ]
    for e in des:
        for i in xrange(len(e)):
            copy_a_day(src[i], e[i])
'''
