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
    def __init__(self, r_name, n_name, r_img, n_img, o_phone, m_phone,  password, role):
        self.id            = 0
        self.real_name     = r_name
        self.nick_name     = n_name
        self.real_img_url  = r_img
        self.nick_img_url  = n_img
        self.office_phone  = o_phone
        self.mobile_phone  = m_phone
        self.password      = password
        self.role          = role
    def dic_return(self):
        return {'id': self.id, 'real_name':str(self.real_name), 
                'nick_name': str(self.nick_name), 'real_img_url': str(self.real_img_url),
                'nick_img_url': str(self.nick_img_url),
                'office_phone': str(self.office_phone),
                'mobile_phone': str(self.mobile_phone),
                'password': str(self.password), 'role': self.role}
# 表的名字:
    __tablename__ = conf.t_user

# 表的结构:
    #用户的id
    id                = Column(Integer, primary_key=True)
    #用户真实名字
    real_name         = Column(String(64))
    #用户昵称名字
    nick_name         = Column(String(64))
    #real_img_url
    real_img_url      = Column(String(128))
    #nick_img_url
    nick_img_url      = Column(String(128))
    #office_phone
    office_phone      = Column(String(32))
    #mobile_phone
    mobile_phone      = Column(String(32))
    password          = Column(String(32))
    role              = Column(Integer)

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
    def __init__(self, id_, uid, did, num, p, u, t, t1, t2, r, pay):
        self.id            = id_
        self.user_id       = uid
        self.dish_id       = did
        self.num           = num
        self.price         = p
        self.unit          = u
        self.time          = t
        self.time1         = t1
        self.time2         = t2
        self.remove        = r
        self.pay_status    = pay
    def dic_return(self):
        return {'id': self.id, 'user_id': self.user_id, 'dish_id': self.dish_id,
                'num':self.num, 'price': self.price, 'unit': self.unit, 'remove': self.remove,
                'time':str(self.time), 'time1': str(self.time1), 'time2': str(self.time2),
                'remove':self.remove, 'pay_staus': self.pay_staus}
    id          = Column(Integer, primary_key=True)
    user_id     = Column(Integer)
    dish_id     = Column(Integer)
    num         = Column(Integer)
    price       = Column(Integer)
    unit        = Column(Integer)
    time        = Column(TIMESTAMP) #下单的时间
    time1       = Column(TIMESTAMP) #预计取食品的时间
    time2       = Column(TIMESTAMP) #实际取食品的时间
    remove      = Column(Integer)
    pay_staus   = Column(Integer)

class Comment(Base):
    __tablename__ = conf.t_comment
    def __init__(self, id_, did_, uid_, r_name, n_name, r_img, n_img, s_, c_):
        t = time.localtime();
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", t)
        self.id          = id_
        self.dish_id     = did_
        self.user_id     = uid_
        self.real_name   = r_name
        self.nick_name   = n_name
        self.real_img_url= r_img
        self.nick_img_url= n_img
        self.stars       = s_
        self.time        = timestamp
        self.content     = c_
    def dic_return(self):
        return {'id': self.id, 'dish_id': self.dish_id, 'user_id': self.user_id,
                'real_name': str(self.real_name), 'nick_name': str(self.nick_name),
                'real_img_url':str(self.real_img_url), 'nick_img_url':str(self.nick_img_url),
                'stars': self.stars, 'time': str(self.time), 'content': str(self.content)}
    #comment的id
    id          = Column(Integer, primary_key=True)
    dish_id     = Column(Integer)
    user_id     = Column(Integer)
    real_name   = Column(String(64))
    nick_name   = Column(String(64))
    real_img_url= Column(String(128))
    nick_img_url= Column(String(128))
    stars       = Column(Integer)
    time        = Column(TIMESTAMP)
    content     = Column(String(512))


# 初始化数据库连接:
db_url = 'mysql+mysqlconnector://' + str(conf.db_user) + ':@localhost:' + str(conf.db_port) + '/' + conf.db_db
engine = create_engine(db_url, encoding=conf.db_encode)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''User'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#失败返回{}
#成功返回User字典
def query_user_db(name, password):
    S = DBSession()
    res = S.query(User).filter(User.real_name==name, User.password==password).first()
    S.close()
    return {} if not res else res.dic_return()

def query_user_by_id_db(uid):
    S = DBSession()
    res = S.query(User).filter(User.id == uid).first()
    S.close()
    return {} if not res else res.dic_return()

def query_user_all_db():
    S = DBSession()
    res = S.query(User).all()
    S.close()
    return [] if not res else [e.dic_return() for e in res]

    
#查询这一天的菜, return []
def query_dish_by_day_db(day):
    S   = DBSession()
    res = S.query(Dish).filter(Dish.time == day).all()
    return [] if not res else [e.dic_return() for e in res]

def write_dish_db(name, pic, time, material, kind, price, unit):
    S   = DBSession()
    d   = Dish(0, name, pic, time, material, kind, price, unit, 0, 0)
    S.add(d)
    S.commit()
    S.close()

def delete_dish_by_id_db(did):
    S   = DBSession()
    res = S.query(Dish).filter(Dish.id == did).delete(synchronize_session=False)
    S.commit()
    S.close()

def query_comments_by_dish_id_db(did):
    S   = DBSession()
    res = S.query(Comment).filter(Comment.dish_id == did).all()
    return [] if not res else [e.dic_return() for e in res]

def query_dish_by_id_db(did):
    S   = DBSession()
    res = S.query(Dish).filter(Dish.id == did).first()
    return {} if not res else res.dic_return()

def write_comment_db(did, uid, r_name, n_name, r_img, n_img, stars, words):
    S   = DBSession()
    c   = Comment(0, did, uid, r_name, n_name, r_img, n_img, s_, c_)
    S.add(c)
    S.commit()
    S.close()

def update_password_db(uid, old, new):
    S   = DBSession()
    res = S.query(User).filter(User.id == uid).first()
    if not res:
        return -1#user does not exist
    r   = res.dic_return()
    if r['password'] != old:
        return -2#old password does not match
    r['password'] = new
    S.query(User).filter(User.id == uid).update(r)
    S.commit()
    return 0

def update_personal_info_db(uid, r_name, n_name, r_img, n_img, o_phone, m_phone):
    D = {}
    if r_name:
        D['real_name']        = r_name
    if n_name:
        D['nick_name']        = n_name
    if r_img:
        D['real_img_url']     = r_img
    if n_img:
        D['nick_img_url']     = n_img
    if o_phone:
        D['office_phone']     = o_phone
    if m_phone:
        D['mobile_phone']     = m_phone
    S = DBSession()
    res = S.query(User).filter(User.id == uid).update(D)
    S.commit()
    S.close()
    return res

def update_user_by_id_db(uid, r_name, n_name, o_phone, m_phone, password, role):
    D = {}
    if r_name:
        D['real_name']        = r_name
    if n_name:
        D['nick_name']        = n_name
    if o_phone:
        D['office_phone']     = o_phone
    if m_phone:
        D['mobile_phone']     = m_phone
    if password:
        D['password']         = password
    if role:
        D['role']             = int(role)
    S = DBSession()
    res = S.query(User).filter(User.id == uid).update(D)
    S.commit()
    S.close()
    return res

def add_user_db(r_name, n_name, o_phone, m_phone, password, role):
    u       = User(r_name, n_name, '', '', o_phone, m_phone,  password, role)
    S       = DBSession()
    res     = S.add(u)
    res     = S.commit()
    S.close()
    return res

def delete_user_by_id_db(uid):
    S = DBSession()
    res = S.query(User).filter(User.id == uid).delete(synchronize_session=False)
    S.commit()
    S.close()
    return res

def write_order_db(uid, did, num, p, u, t, t1, t2):
    S = DBSession()
    o   = Order(0, uid, did, num, p, u, t, t1, t2, 0, 0)
    S.add(o)
    r = S.commit()
    S.close()
    return r

def query_all_orders_db():
    S = DBSession()
    res = S.query(Order).filter(Order.remove == 0).all()
    S.close()
    return [] if not res else [e.dic_return() for e in res]

def query_orders_by_uid_db(uid):
    S = DBSession()
    res = S.query(Order).filter(Order.user_id == uid).filter(Order.remove == 0).all()
    S.close()
    return [] if not res else [e.dic_return() for e in res]

def query_dish_by_ids_db(ids):
    S = DBSession()
    res = S.query(Dish).filter(Dish.id.in_(ids)).all()
    return [] if not res else [e.dic_return() for e in res]








def query_user_by_id_db(uid):
    S = DBSession()
    res = S.query(User).filter(User.id==uid).first()
    return None if not res else res.dic_return()
    S.close()

def write_user_db(r_name, n_name, r_img, n_img, o_phone, m_phone,  password, role):
    S = DBSession()
    u   = User(r_name, n_name, r_img, n_img, o_phone, m_phone,  password, role)
    S.add(u)
    S.commit()
    S.close()

def update_user_password_db(uid, old, new):
    S = DBSession()
    r = S.query(User).filter(User.id == uid).first()
    if not r:
        return False
    if r['password'] != old:
        return False
    D = {User.password: new}
    S.query(User).filter(User.id == uid).update(D)
    S.close()
    return True


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Dish'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#返回数组，每个元素是Dish字典
def query_dish_by_day_db(day):
    S = DBSession()
    res = S.query(Dish).filter(Dish.time == day).order_by(Dish.time.desc()).all()
    S.close()
    return [] if not res else [e.dic_return() for e in res]

def query_dish_by_dish_id_db(did):
    res = S.query(Dish).filter(Dish.id == did).first()
    return {} if not res else res.dic_return()


def update_dish_by_id_db(did, name, pic, time, material, kind, price, unit, s, n):
    S = DBSession()
    D   = {Dish.name:name, Dish.pic_loc:pic, Dish.time:time, Dish.material:material,
           Dish.kind:kind, Dish.price:price, Dish.unit:unit, Dish.score:s, Dish.num:n}
    res = S.query(Dish).filter(Dish.id == did).update(D)
    S.commit()
    S.close()

def delete_dish_by_dish_id_db(did):
    S = DBSession()
    res = S.query(Dish).filter(Dish.id == did).delete(synchronize_session=False)
    S.commit()
    S.close()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Order'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def query_order_list_by_uid_db(uid):
    S = DBSession()
    res = S.query(Order).filter(Order.user_id == uid).all()
    S.close()
    return [] if not res else [e.dic_return() for e in res]
def query_order_by_user_id_db():
    pass
def query_order_list_all_db():
    S = DBSession()
    res = S.query(Order).filter(Order.remove == 0).filter(Order.time2 == "").all()
    S.close()
    return [] if not res else [e.dic_return() for e in res]

def update_order_by_id_db(oid, uid, did, num, p, u, t, t1, t2, rm):
    S = DBSession()
    D   = {Order.user_id:uid, Order.dish_id:did, Order.num:num, Order.price:p,
           Order.unit:u, Order.time:t, Order.time1:t1, Order.time2:t2, Order.remove:rm}
    u   = S.query(Order).filter(Order.id == oid).update(D)
    S.commit()
    S.close()

def delete_order_by_id_db(oid):
    S = DBSession()
    res = S.query(Order).filter(Order.id == oid).delete(synchronize_session=False)
    S.commit()
    S.close()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Comment'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def query_comment_by_dish_id_db(did):
    S = DBSession()
    res = S.query(Comment).filter(Comment.dish_id == did).order_by(Comment.time.desc()).all()
    S.close()
    return [] if not res else [e.dic_return() for e in res]

def write_comment_db(did_, uid_, r_name, n_name, r_img, n_img, s_, c_):
    S = DBSession()
    c   = Comment(0, did_, uid_, r_name, n_name, r_img, n_img, s_, c_)
    S.add(c)
    S.commit()
    S.close()

def delete_comment_by_id(cid):
    S = DBSession()
    res = S.query(Comment).filter(Comment.id == cid).delete(synchronize_session=False)
    S.commit()
    S.close()
"""
将上传的图片信息写入数据库，图片存放在本地服务器上
一个图片对应一道菜
"""
def write_dish(filename, dish_name, dish_material, dish_order):
    session = DBSession()
    [pic_loc, timestamp] = filename.split('\3')
    d = Dish(id=0, name=dish_name, pic_loc=pic_loc, time=timestamp, can_order=dish_order, material=dish_material)
    session.add(d)
    session.commit()
    session.close()
"""
将评论写入数据库，一个用户id对应一个菜的id
"""
def write_comment(userid, dish_id, star, words):
    session = DBSession()
    c = Comment(0, dish_id, userid, star, words)
    session.add(c)
    session.commit()
    session.close()
    return True
"""
将预订信息写入数据库
"""
def write_order(userid, username, dish_id, dish_name, img_url, num):
    session = DBSession()
    o = Order(0, userid, username, dish_id, dish_name, img_url, num)
    session.add(o)
    session.commit()
    session.close()
    return True
"""
查询菜的评论
"""
def query_comments_by_id(dish_id):
    session = DBSession()
    c       = session.query(Comment).filter(Comment.dish_id == dish_id).all()
    return c
"""
查询指定日期的菜谱信息, 指定日期是yyyy-mm-dd
"""
def query_dish_by_day(day):
    return None
def dish_delete(imgid):
    session = DBSession()
    res = session.query(Dish).filter(Dish.id == imgid).delete(synchronize_session=False)
    session.commit()

def regist_user(info):
    [uname, passwd] = info.split('\3');
    if not uname or not passwd:
        return -1#name or password is None
    session = DBSession()
    res = session.query(User).filter(User.name == uname).count()
    if not res:
        sha512 = hashlib.sha512(passwd.encode()).hexdigest()
        u = User(uname, sha512)
        ret = session.add(u)
        session.commit()
        return 0#regist successfully
    return 1#name duplicated

def update_user_password(userid, old, passwd):
    session = DBSession()
    sha512 = hashlib.sha512(passwd.encode()).hexdigest()
    sha512old = hashlib.sha512(old.encode()).hexdigest()
    res = session.query(User).filter(User.id == userid).filter(User.password == sha512old).count()
    if not res:
        return None
    res = session.query(User).filter(User.id == userid).update({User.password:sha512})
    session.commit()
    session.close()
    return True

def query_order_list_by_uid(uid):
    session = DBSession()
    res = session.query(Order).filter(Order.user_id == uid).order_by(Order.time.desc()).all()
    ret = [{'img_url':e.img_url, 'num': e.num, 'dish_name': e.dish_name, 'time': e.time} for e in res]
    session.close()
    return ret

def query_all_users():
    session = DBSession()
    res = session.query(User).all()
    ret = [{"name": e.name, "role": e.role, "id":e.id, "passwd": e.password} for e in res]
    session.close()
    return ret

def update_user(name, passwd, role, uid):
    session = DBSession()
    res = session.query(User).filter(User.id == uid).first()
    if not res:
        return True
    sha512 = res.password
    if sha512 != passwd:
        sha512 = hashlib.sha512(passwd.encode()).hexdigest()
    res = session.query(User).filter(User.id == uid).update({User.password:sha512, User.name: name, User.role: role})
    session.commit()
    session.close()
    return True
def delete_user(uid):
    session = DBSession()
    res = session.query(User).filter(User.id == uid).delete()
    session.commit()
    session.close()
    return True
def add_user(name, passwd, role):
    session = DBSession()
    sha512 = hashlib.sha512(passwd.encode()).hexdigest()
    user    = User(name, sha512, role)
    res = session.add(user)
    session.commit()
    session.close()
    return True

if __name__ == "__main__":
    r = query_dish_by_day_db('20170821')
    print(r)
    t = r['time']
