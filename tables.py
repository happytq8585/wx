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
    S     = DBSession()
    r     = S.query(User).filter(User.mobile == mobile).first()
    S.close()
    return {} if not r else r.dic_return()

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
    name        = user['name']
    mobile      = user['mobile']
    S = DBSession()
    N = len(data[0])
    oid         = now + '-' + name
    for i in xrange(N):
        if data[1][i] == 0:
            continue;
        price   = dishes[i]['price']
        unit    = dishes[i]['unit']
        o       = Order(0, oid, mobile, data[0][i], data[1][i], price, unit, now1, day, '', 0, 0)
        S.add(o)
    r = S.commit()
    S.close()
    return r

#return: [ {'oid':oid,'list':[dish, dish,...]}, ... ]
def query_order_by_mobile_db(mobile):
    S = DBSession()
    r = S.query(Order).filter(Order.mobile == mobile).order_by(Order.time).all()
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
    return dids, O

def delete_order_db(oid):
    S = DBSession()
    r = S.query(Order).filter(Order.orderid == oid).delete(synchronize_session=False)
    S.commit()


if __name__ == "__main__":
    from conf import conf
    m = '17313615918'
    r = query_order_by_mobile_db(m)
    print(r)
