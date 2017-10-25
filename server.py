#-*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import hashlib
import os.path
import json
import time
import datetime
import re

from device import isMobileDevice, checkMobile
from tornado.web import StaticFileHandler
from tornado.options import define, options

from wx import wxapi
from conf import conf
from log import log

from data import query_dish_by_day, write_dish, query_dish_by_id
from data import query_comments_by_dish_id, write_user, write_comment
from data import query_all_users, delete_dish_by_id, update_dish
from data import query_reserve, query_dish_by_ids, query_user_by_mobile, query_user_by_mobiles
from data import write_order, query_order_by_mobile, delete_order
from data import query_order_left, query_order_middle, query_order_right
from data import orderconfirm, check_and_notify

from tables import check_pc_user

define("port", default=8000, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("mobile")
    def get_role(self):
        return int(self.get_secure_cookie("role"))

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        code = self.get_argument('code', None)
        if not code:
            mobile = self.get_secure_cookie('mobile')
            if not mobile:
                self.write('请登录企业APP')
                self.finish()
            else:
                r = yield tornado.gen.Task(self._query_user, mobile)
                if not r or r['mobile'] != mobile:
                    self.write('请登录企业APP')
                    self.finish()
                else:
                    self.render('index.html', mobile=mobile)
        else:
            atk    = yield tornado.gen.Task(self._access)
            if not atk:
                self.finish()
            else:
                print("atk=%s"%atk)
                uid    = yield tornado.gen.Task(self._userid, atk, code)
                if not uid:
                    self.finish()
                else:
                    print("userid=%s"%uid)
                    info   = yield tornado.gen.Task(self._userinfo, atk, uid)
                    if not info:
                        self.finish()
                    else:
                        print("userinfo=%s"%info)
                        log.Print(str(info))
                        yield tornado.gen.Task(self._write_user_cache, info)
                        self.render('index.html', mobile=info.get('mobile', ''))
    @tornado.gen.coroutine
    def _query_user(self, mobile):
        r = query_user_by_mobile(mobile)
        return r
    @tornado.gen.coroutine
    def _write_user_cache(self, u):
        mobile = u.get('mobile', '')
        self.set_secure_cookie('mobile', mobile, expires_days=None)
        write_user(mobile, u)

    @tornado.gen.coroutine
    def _access(self):
        return wxapi.access_token()

    @tornado.gen.coroutine
    def _userid(self, atk, code):
        return wxapi.userid(atk, code)

    @tornado.gen.coroutine
    def _userinfo(self, atk, uid):
        return wxapi.userinfo(atk, uid)

class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin_login.html')
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        mobile  = self.get_argument('username', None)
        passwd  = self.get_argument('password', None)
        if not mobile or not passwd:
            self.finish()
        else:
            r = yield tornado.gen.Task(self.__check_user, mobile, passwd)
            if r:
                self.set_secure_cookie('mobile', mobile, expires_days=None)
                self.render('index.html', mobile=mobile)
            else:
                self.write('username or password error!')
                self.finish()
    @tornado.gen.coroutine
    def __check_user(self, mobile, passwd):
        r = check_pc_user(mobile, passwd)
        return r

class DishModule(tornado.web.UIModule):
    def render(self, arr, mobile, expire, conf):
        target = 'menu_modules/dish.html'
        return self.render_string(target, arr=arr, mobile=mobile, expire=expire, conf=conf)

class MenuHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def get(self):
        day         = self.get_argument('day', None)
        data        = self.get_argument('data', None)
        t           = time.localtime()
        now         = time.strftime('%Y-%m-%d', t)
        offset      = time.strftime('%H:%M:%S', t)
        if not day:
            day     = now
        expire      = True if day + conf.timeoffset  < now + offset else False
        arr         = yield tornado.gen.Task(self._get_dish_by_day, day)
        breakfast   = []
        lunch       = []
        dinner      = []
        for e in arr:
            if e['kind'] == 0x0010:
                breakfast.append(e)
            elif e['kind'] == 0x0100:
                lunch.append(e)
            elif e['kind'] == 0x1000:
                dinner.append(e)
            else:
                pass
        mobile      = self.get_secure_cookie('mobile')
        if not data:
            self.render('menu_modules/menu.html', breakfast=breakfast, lunch=lunch, dinner=dinner, mobile=mobile, expire=expire, conf=conf, day=day)
        else:
            R = self.render_string('menu_modules/tab.html',breakfast=breakfast, lunch=lunch, dinner=dinner, mobile=mobile, expire=expire, conf=conf)
            self.write(R)
            self.finish()
    @tornado.gen.coroutine
    def _get_dish_by_day(self, day):
        r = query_dish_by_day(day)
        return r

class AddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        day = self.get_argument('day', None)
        if not day:
            self.write('没有选择时间, 没法添加')
        else:
            self.render('add.html')
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        if not os.path.exists("static/files"):
            os.makedirs("static/files");
        day = self.get_argument("day", None)
        if not day:
            self.write("no day parameter")
        else:
            name         = self.get_argument('name', '')
            material     = self.get_argument('material', '')
            unit         = self.get_argument('unit', '')
            price        = self.get_argument('price', 0)
            kind         = self.get_argument('kind', 0)
            todaydir = "static/files/" + day
            upload_path = os.path.join(os.path.dirname(__file__), todaydir)
            file_metas  = self.request.files.get('file')
            filename = ''
            pic_loc  = ''
            if file_metas:
                meta = file_metas[0]
                filename = meta.get('filename', '')
            print("filename=", filename)
            if filename:
                pic_loc = todaydir + '/' + filename
                if not os.path.exists(todaydir):
                    os.makedirs(todaydir)
                filename = todaydir + '/' +  filename
                yield tornado.gen.Task(self._up_img, filename, meta['body'])
            yield tornado.gen.Task(self._write_dish, name, pic_loc, day, material, kind, price, unit)
            self.write("上传成功!")
            self.finish()

    @tornado.gen.coroutine
    def _up_img(self, name, body):
        with open(name, 'wb') as up:
            up.write(body)
    @tornado.gen.coroutine
    def _write_dish(self, name, pic_loc, day, material, kind, price, unit):
        write_dish(name, pic_loc, day, material, kind, price, unit)

class DishHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        did             = self.get_argument('id', None)
        day             = self.get_argument('day', '')
        if not did:
            pass
        else:
            t           = time.localtime()
            now         = time.strftime("%Y-%m-%d", t)
            dish        = yield tornado.gen.Task(self._get_dish, did)
            comments    = yield tornado.gen.Task(self._get_comments, did)
            mobile      = self.get_secure_cookie('mobile')
            tag         = False
            for e in comments:
                if e['mobile'] == mobile:
                    tag = True
                    break
            if dish['time'] > now:
                tag = True
            users = yield tornado.gen.Task(self._get_users)
            print(users)
            self.render('dish.html', d=dish, C=comments, U=users, already=tag, day=day)

    @tornado.gen.coroutine
    def _get_users(self):
        r = query_all_users()
        return r
    @tornado.gen.coroutine
    def _get_comments(self, did):
        r = query_comments_by_dish_id(did)
        return r

    @tornado.gen.coroutine
    def _get_dish(self, did):
        r = query_dish_by_id(did)
        return r
    @tornado.web.authenticated
    def post(self):
        pass

class DishReserveHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        did             = self.get_argument('id', None)
        day             = self.get_argument('day', '')
        if not did:
            self.finish()
        else:
            t           = time.localtime()
            now         = time.strftime("%Y-%m-%d", t)
            dish        = yield tornado.gen.Task(self._get_dish, did)
            comments    = yield tornado.gen.Task(self._get_comments, did)
            mobile      = self.get_secure_cookie('mobile')
            tag         = False
            for e in comments:
                if e['mobile'] == mobile:
                    tag = True
                    break
            if dish['time'] > now:
                tag = True
            users = yield tornado.gen.Task(self._get_users)
            print(users)
            self.render('dish_reserve.html', d=dish, C=comments, U=users, already=tag, day=day)

    @tornado.gen.coroutine
    def _get_users(self):
        r = query_all_users()
        return r
    @tornado.gen.coroutine
    def _get_comments(self, did):
        r = query_comments_by_dish_id(did)
        return r

    @tornado.gen.coroutine
    def _get_dish(self, did):
        r = query_dish_by_id(did)
        return r
    @tornado.web.authenticated
    def post(self):
        pass

class CommentHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        mobile = self.get_secure_cookie('mobile')
        if not mobile:
            self.write('mobile is null')
        else:
            num  = int(self.get_argument('num', 0))
            cnt  = self.get_argument('content', '')
            did  = int(self.get_argument('did', 0))
            if not num:
                self.write('num is null')
            elif not did:
                self.write('dish id is null')
            else:
                yield tornado.gen.Task(self._write_comment, mobile, num, cnt, did)
                self.write('ok')
        self.finish()

    @tornado.gen.coroutine
    def _write_comment(self, mobile, num, cnt, did):
        write_comment(mobile, num, cnt, did)        

class EditHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def get(self):
        did       = self.get_argument('id', None)
        if not did:
            self.write('invalid dish id')
        else:
            d     = yield tornado.gen.Task(self._query_dish, did)
            self.render('edit.html', d=d)

    @tornado.gen.coroutine
    def _query_dish(self, did):
        d   = query_dish_by_id(did)
        return d

    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def post(self):
        day = self.get_argument('day', None)
        if not day or len(day) == 0:
            self.write('没有选择时间, 没法编辑')
            self.finish()
        else:
            if not os.path.exists("static/files"):
                os.makedirs("static/files");
            old_img      = self.get_argument('old_img', '')
            did          = self.get_argument('did', '')
            name         = self.get_argument('name', '')
            material     = self.get_argument('material', '')
            unit         = self.get_argument('unit', '')
            price        = self.get_argument('price', 0)
            kind         = self.get_argument('kind', 0)
            todaydir = "static/files/" + day
            upload_path = os.path.join(os.path.dirname(__file__), todaydir)
            file_metas  = self.request.files.get('file')
            filename = ''
            pic_loc  = ''
            if file_metas:
                meta = file_metas[0]
                filename = meta.get('filename', '')
            print("filename=", filename)
            if filename:
                pic_loc = todaydir + '/' + filename
                if not os.path.exists(todaydir):
                    os.makedirs(todaydir)
                filename = todaydir + '/' +  filename
                yield tornado.gen.Task(self._up_img, filename, meta['body'])
            else:
                pic_loc = old_img
            r = yield tornado.gen.Task(self._update_dish, did, name, pic_loc, day, material, kind, price, unit)
            if not r:
                self.write("更新失败!")
            else:
                self.write("更新成功!")
            self.finish()

    @tornado.gen.coroutine
    def _up_img(self, name, body):
        with open(name, 'wb') as up:
            up.write(body)

    @tornado.gen.coroutine
    def _update_dish(self, did, name, pic_loc, day, material, kind, price, unit):
        r = update_dish(did, name, pic_loc, day, material, kind, price, unit)
        return r

class DeleteDishHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def post(self):
        did    = self.get_argument('id', None)
        if not did:
            self.write('dish id is invalid')
        else:
            r  = yield tornado.gen.Task(self._delete_dish, did)
            if not r:
                self.write('有人评价,不能删除!')
            else:
                self.write('删除成功!')
        self.finish()

    @tornado.gen.coroutine
    def _delete_dish(self, did):
        r = delete_dish_by_id(did)
        return r

class ReserveHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def get(self):
        day  = self.get_argument('day', None)
        data = self.get_argument('data', None)
        canorder = True
        T   = time.time()
        T   = T + 24*3600
        t   = time.localtime(T)
        now = time.strftime('%Y-%m-%d %H:%M:%S', t)
        if not day:
            day = time.strftime('%Y-%m-%d', t)
        d    = yield tornado.gen.Task(self._query_reserve, 'day', day)
        print(d)
        if now > day + ' ' + conf.orderfood_offset:
            canorder = False
        if data:
            r = self.render_string('reserve/data.html', D=d)
            R = {'data':r, 'len':len(d), 'canorder':canorder}
            print(canorder)
            self.write(R)
            self.finish()
        else:
            self.render('reserve/reserve.html', D=d, day=day, canorder=canorder)

    @tornado.gen.coroutine
    def _query_reserve(self, t, p):
        d    = query_reserve(t, p)
        return d

    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def post(self):
        day  = self.get_argument('day',  None)
        data = self.get_argument('data', None)
        if not day or not data:
            self.finish()
        else:
            ret         = data.split('\r')
            ids, nums   = ret[0], ret[1]
            ids         = [int(e) for e in ids.split('\t')]
            nums        = [int(e) for e in nums.split('\t')]
            data        = [ids, nums]
            day         = day + ' ' + conf.getfood_offset
            mobile      = self.get_secure_cookie('mobile')
            u           = yield tornado.gen.Task(self._query_user, mobile)
            if not u:
                self.write('mobile phone number missing')
                self.finish()
            else:
                dishes = yield tornado.gen.Task(self._query_dishes, ids)
                r      = yield tornado.gen.Task(self._write_order, u, data, dishes, day)
                if not r:
                    self.write('-1')
                else:
                    self.write('0')
                self.finish()

    @tornado.gen.coroutine
    def _query_dishes(self, ids):
        r = query_dish_by_ids(ids)
        return r

    @tornado.gen.coroutine
    def _query_user(self, mobile):
        r = query_user_by_mobile(mobile)
        return r

    @tornado.gen.coroutine
    def _write_order(self, user, data, dishes, day):
        r = write_order(user, data, dishes, day)
        return r

class OrderHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def get(self):
        mobile      = self.get_secure_cookie('mobile', None)
        data        = self.get_argument('data', None)
        if not mobile:
            self.finish()
        else:
            t           = time.localtime()
            now         = time.strftime('%Y-%m-%d', t)

            u           = yield tornado.gen.Task(self._get_user, mobile)
            name        = u['name']
            if mobile not in conf.canteen_admin_mobile.split(','):
                dids, O     = yield tornado.gen.Task(self._get_order, mobile)
                D           = {}
                if len(dids):
                    dishes      = yield tornado.gen.Task(self._get_dishes, dids)
                    for e in dishes:
                        D[e['id']] = e
                    self._get_sum(O, D)
                if not data:
                    self.render('order/vieworder.html', name=name, O=O, D=D, now=now)
                else:
                    loc = self.get_argument('loc', None)
                    if not loc:
                        self.finish()
                    else:
                        loc = int(loc)
                        R = ''
                        if loc == 0:
                            R = self.render_string('order/now.html', name=name, O=O, D=D, now=now)
                        elif loc == 1:
                            R = self.render_string('order/history.html', name=name, O=O, D=D, now=now)
                        self.write(R)
                        self.finish()
            else:
                if not data:
                    self.render('order/vieworder-admin.html')
                else:
                    loc = self.get_argument('loc', None)
                    if not loc:
                        self.finish()
                    else:
                        loc = int(loc)
                        if loc == 0:
                            ids, O, mobile = yield tornado.gen.Task(self._get_left)
                            users  = yield tornado.gen.Task(self._get_users, mobile)
                            U = {}
                            for e in users:
                                U[e['mobile']] = e.get('name', e['mobile'])
                            dishes = yield tornado.gen.Task(self._get_dish, ids)
                            D = {}
                            for e in dishes:
                                D[e['id']] = e
                            R = self.render_string('order/now-admin.html', O=O, D=D, U=U, now=now)
                            self.write(R)
                            self.finish()
                        elif loc == 1:
                            ids, O, orders = yield tornado.gen.Task(self._get_middle)
                            dishes = yield tornado.gen.Task(self._get_dish, ids)
                            D = {}
                            for e in dishes:
                                D[e['id']] = e
                            T = self._get_tormorrow()

                            mobile = [e for e in orders]
                            users  = yield tornado.gen.Task(self._get_users, mobile)
                            U = {}
                            for e in users:
                                U[e['mobile']] = e.get('name', e['mobile'])
                            R = self.render_string('order/statistic.html', O=O, D=D, tormorrow=T, orders=orders, U=U)
                            self.write(R)
                            self.finish()
                        elif loc == 2:
                            ids, O, mobile = yield tornado.gen.Task(self._get_right)
                            users  = yield tornado.gen.Task(self._get_users, mobile)
                            U = {}
                            for e in users:
                                U[e['mobile']] = e.get('name', e['mobile'])
                            dishes = yield tornado.gen.Task(self._get_dish, ids)
                            D = {}
                            for e in dishes:
                                D[e['id']] = e
                            R = self.render_string('order/now-admin.html', O=O, D=D, U=U, now=now)
                            self.write(R)
                            self.finish()
                        else:
                            self.finish()
    def _get_tormorrow(self):
        t           = time.time() + 24*3600
        t           = time.localtime(t)
        day         = time.strftime('%Y-%m-%d', t)
        return day
    @tornado.gen.coroutine
    def _get_left(self):
        r = query_order_left()
        return r
    @tornado.gen.coroutine
    def _get_right(self):
        r = query_order_right()
        return r
    @tornado.gen.coroutine
    def _get_dish(self, ids):
        r = query_dish_by_ids(ids)
        return r
    @tornado.gen.coroutine
    def _get_users(self, mobiles):
        r = query_user_by_mobiles(mobiles)
        return r
    @tornado.gen.coroutine
    def _get_middle(self):
        ids, o, orders = query_order_middle()
        return ids, o, orders

    def _get_sum(self, O, D):
        for o in O:
            s  = 0
            for e in o['list']:
                n = e['num']
                p = D[e['dish_id']]['price']
                s = s + n*p
            s = round(s/100.0, 2)
            o['sum'] = s

    @tornado.gen.coroutine
    def _get_dishes(self, dids):
        r = query_dish_by_ids(dids)
        return r

    @tornado.gen.coroutine
    def _get_order(self, mobile):
        r = query_order_by_mobile(mobile)
        return r

    @tornado.gen.coroutine
    def _get_user(self, mobile):
        r = query_user_by_mobile(mobile)
        return r

    def post(self):
        pass

class DeleteOrderHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def post(self):
        oid     = self.get_argument('id', None)
        if not oid:
            self.finish()
        else:
            yield tornado.gen.Task(self._del_order, oid)
            self.finish()

    @tornado.gen.coroutine
    def _del_order(self, oid):
        r = delete_order(oid)
        return r

class PersonalHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def get(self):
        mobile = self.get_argument('mobile', None)
        if not mobile:
            self.finish()
        else:
            u = yield tornado.gen.Task(self._get_user, mobile)
            if not u:
                self.finish()
            else:
                if u['gender'] == '1':
                    u['gender'] = '男'
                elif u['gender'] == '2':
                    u['gender'] = '女'
                else:
                    u['gender'] = 'unknown'
                self.render('user.html', U=u)

    @tornado.gen.coroutine
    def _get_user(self, mobile):
        r = query_user_by_mobile(mobile)
        return r

class OrderConfirmHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def post(self):
        orderid = self.get_argument('orderid', None)
        if not orderid:
            self.finish()
        else:
            yield tornado.gen.Task(self._confirm, orderid)
            self.write('confirmed!')
            self.finish()

    @tornado.gen.coroutine
    def _confirm(self, orderid):
        r = orderconfirm(orderid)
        return r

class MsgHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        mobile = self.get_argument('mobile', None)
        cnt    = self.get_argument('content', None)
        if not mobile or not cnt:
            self.finish()
        else:
            u      = yield tornado.gen.Task(self._get_user, mobile)
            if not u:
                self.finish()
            else:
                cnt    = '您的订单号' + cnt + '今天该取啦'
                atk    = yield tornado.gen.Task(self._access)
                r      = yield tornado.gen.Task(self._send, atk, u['userid'], conf.agentid, cnt)
                self.write(str(r))
                self.finish()

    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def post(self):
        mobile = self.get_argument('mobile', None)
        cnt    = self.get_argument('content', None)
        if not mobile or not cnt:
            self.finish()
        else:
            u      = yield tornado.gen.Task(self._get_user, mobile)
            if not u:
                self.finish()
            else:
                atk    = yield tornado.gen.Task(self._access)
                r      = yield tornado.gen.Task(self._send, atk, u['userid'], conf.agentid, cnt)
                self.write(str(r))
                self.finish()

    @tornado.gen.coroutine
    def _get_user(self, mobile):
        r = query_user_by_mobile(mobile)
        return r
    @tornado.gen.coroutine
    def _access(self):
        return wxapi.access_token()

    @tornado.gen.coroutine
    def _send(self, atk, uid, agentid, cnt):
        return wxapi.msg(atk, uid, agentid, cnt)

class ConstructHandler(BaseHandler):
    pass

if __name__ == "__main__":
    tornado.options.parse_command_line()
    ui_modules = {'Dish_module':DishModule}
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,
        "login_url": "/",
        "ui_modules":ui_modules,
        "debug":True}
    handler = [
               (r"/static/(.*)", StaticFileHandler, {"path": "static"}),  
               (r"/css/(.*)", StaticFileHandler, {"path": "static/css"}),  
               (r"/js/(.*)", StaticFileHandler, {"path": "static/js"}),  
               (r"/img/(.*)", StaticFileHandler, {"path": "static/img"}), 
               (r"/images/(.*)", StaticFileHandler, {"path": "static/images"}), 
               (r'/', IndexHandler),
               (r'/admin', AdminHandler),
               (r'/menu', MenuHandler),
               (r'/add', AddHandler),
               (r'/up', AddHandler),
               (r'/dish', DishHandler),
               (r'/dish_reserve', DishReserveHandler),
               (r'/comment', CommentHandler),
               (r'/edit', EditHandler),
               (r'/delete', DeleteDishHandler),
               (r'/reserve', ReserveHandler),
               (r'/order', OrderHandler),
               (r'/delorder', DeleteOrderHandler),
               (r'/personal', PersonalHandler),
               (r'/msgsend', MsgHandler),
               (r'/orderconfirm', OrderConfirmHandler),
               (r'/notice',  ConstructHandler),
              ]
    application = tornado.web.Application(handler, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.PeriodicCallback(check_and_notify, conf.notify_interval).start()
    tornado.ioloop.IOLoop.instance().start()
