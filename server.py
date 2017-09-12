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
from data import query_order

define("port", default=8000, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("mobile")
    def get_role(self):
        return int(self.get_secure_cookie("role"))
    def _get_head_nav(self):
        if not hasattr(self, 'pb_data'):
            real_name      = self.get_secure_cookie('real_name')
            role           = self.get_secure_cookie('role')
            self.pb_data   = PublicData(real_name, role)
        return self.pb_data.get_head()
    def _get_canteen(self):
        if not hasattr(self, 'pb_data'):
            real_name      = self.get_secure_cookie('real_name')
            role           = self.get_secure_cookie('role')
            self.pb_data   = PublicData(real_name, role)
        return self.pb_data.get_canteen()
    def _get_user(self):
        u = {}
        u['id']            = int(self.get_secure_cookie('uid'))
        u['real_name']     = self.get_secure_cookie('real_name')
        u['nick_name']     = self.get_secure_cookie('nick_name')
        u['real_img_url']  = self.get_secure_cookie('real_img_url')
        u['nick_img_url']  = self.get_secure_cookie('nick_img_url')
        u['office_phone']  = self.get_secure_cookie('office_phone')
        u['mobile_phone']  = self.get_secure_cookie('mobile_phone')
        u['role']          = int(self.get_secure_cookie('role'))
        u['password']      = ''
        return u

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        code = self.get_argument('code', None)
        if not code:
            self.set_secure_cookie('mobile', '123456789')
            self.render('index.html')
            #self.finish()
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
                        self.render('index.html')
    @tornado.gen.coroutine
    def _write_user_cache(self, u):
        mobile = u.get('mobile', '')
        self.set_secure_cookie('mobile', mobile)
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

class DishModule(tornado.web.UIModule):
    def render(self, arr, mobile, expire, conf):
        target = 'menu_modules/dish.html'
        return self.render_string(target, arr=arr, mobile=mobile, expire=expire, conf=conf)

class MenuHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        day         = self.get_argument('day', None)
        t           = time.localtime()
        now         = time.strftime('%Y-%m-%d', t)
        offset      = time.strftime('%H:%M:%S', t)
        if not day:
            day     = now
        expire      = True if day + conf.timeoffset  < now + offset else False
        arr         = query_dish_by_day(day)
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
        self.render('menu_modules/menu.html', breakfast=breakfast, lunch=lunch, dinner=dinner, mobile=mobile, expire=expire, conf=conf)

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
        if not did:
            pass
        else:
            dish        = yield tornado.gen.Task(self._get_dish, did)
            comments    = yield tornado.gen.Task(self._get_comments, did)
            mobile      = self.get_secure_cookie('mobile')
            tag         = False
            for e in comments:
                if e['mobile'] == mobile:
                    tag = True
                    break
            users = yield tornado.gen.Task(self._get_users)
            print(users)
            self.render('dish.html', d=dish, C=comments, U=users, already=tag)

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

class DeleteHandler(BaseHandler):
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
                self.write('delete failed!')
            else:
                self.write('delete success!')
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
        if not day:
            t   = time.localtime()
            now = time.strftime('%Y-%m-%d', t)
            day = now 
        d    = yield tornado.gen.Task(self._query_order, 'day', day)
        print(d)
        self.render('food_reservation.html', D=d)

    @tornado.gen.coroutine
    def _query_order(self, t, p):
        d    = query_order(t, p)
        return d

    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def post(self):
        self.finish()

class PersonalHandler(BaseHandler):
    def get(self):
        action      = self.get_argument('action', '')
        role        = int(self.get_secure_cookie('role'))
        device      = self.get_secure_cookie('pc_or_mobile')
        head    = self._get_head_nav()
        canteen = self._get_canteen()
        if action == 'info':#personal information and password
            target    = '%s/personal/PersonalCenter.html' % device
            user    = self._get_user()
            self.render(target, device=device, head=head, canteen=canteen, user=user)
        elif action == 'management':
            target    = '%s/personal/Employeelists.html' % device
            users     = query_user_all()
            self.render(target, device=device, head=head, users=users)
    def post(self):
        action      = self.get_argument('action', '')
        if action == 'password':
            old_pass    = self.get_argument('old_pass', '')
            new_pass    = self.get_argument('new_pass', '')
            uid         = int(self.get_secure_cookie('uid'))
            r           = update_password(uid, old_pass, new_pass)
            self.write(str(r))
        elif action == 'info':
            r_name      = self.get_argument('real_name', '')
            n_name      = self.get_argument('nick_name', '')
            o_phone     = self.get_argument('office_phone', '')
            m_phone     = self.get_argument('mobile_phone', '')
            personal_img_dir = "static/img/personal"
            if not os.path.exists(personal_img_dir):
                os.makedirs(personal_img_dir)
            upload_path = os.path.join(os.path.dirname(__file__), personal_img_dir)
            file_metas  = self.request.files['file']
            meta = file_metas[0]
            filename = meta['filename']
            filename = personal_img_dir + '/' +  filename
            with open(filename, 'wb') as up:
                up.write(meta['body'])
            f_name      = filename
            uid         = int(self.get_secure_cookie('uid'))
            r = update_personal_info(uid, r_name, n_name, '', f_name, o_phone, m_phone)
            if r == 1:
                e = query_user_by_id(uid)
                self._update_cookie(e)
                self.write('update success!')
            else:
                self.write('update failed!')
        elif action == 'adduser':
            uid         = int(self.get_argument('user_id', 0))
            r_name      = self.get_argument('real_name', '')
            n_name      = self.get_argument('nick_name', '')
            o_phone     = self.get_argument('office_phone', '')
            m_phone     = self.get_argument('mobile_phone', '')
            password    = self.get_argument('password', '')
            role        = int(self.get_argument('role', '0'))
            r           = 0
            device      = self.get_secure_cookie('pc_or_mobile')
            target      = '%s/personal/user_op.html' % device
            if not uid:
                r       = add_user(r_name, n_name, o_phone, m_phone, password, role)
                self.render(target, msg='添加成功')
            else:
                r       = update_user_by_id(uid, r_name, n_name, o_phone, m_phone, password, role)
                self.render(target, msg='修改成功')
        elif action == 'delete':
            uid         = int(self.get_argument('user_id', 0))
            r           = delete_user_by_id(uid)
            if not r:
                self.write("没有这个用户")
            else:
                self.write("删除成功")
    def _update_cookie(self, e):
            self.set_secure_cookie('uid', str(e['id']), expires_days=None)
            self.set_secure_cookie('real_name', e['real_name'], expires_days=None)
            self.set_secure_cookie('nick_name', e['nick_name'], expires_days=None)
            self.set_secure_cookie('real_img_url', e['real_img_url'], expires_days=None)
            self.set_secure_cookie('nick_img_url', e['nick_img_url'], expires_days=None)
            self.set_secure_cookie('office_phone', e['office_phone'], expires_days=None)
            self.set_secure_cookie('mobile_phone', e['mobile_phone'], expires_days=None)
            self.set_secure_cookie('role', str(e['role']), expires_days=None)

class OrderHandler(BaseHandler):
    def _grp_orders(self, orders):
        t            = {}
        r            = {}
        ids_tmp      = {}
        for e in orders:
            ids_tmp[e['dish_id']] = 1
            day = e['time1'].split(' ')[0]
            arr = t.get(day)
            if not arr:
                t[day] = [e]
            else:
                t[day].append(e)
        ids          = [e for e in ids_tmp]
        R            = query_dish_by_ids(ids)
        DishDic = {}
        for e in R:
            DishDic['%dpic' % e['id']] = e['pic_loc']
            DishDic['%dname' % e['id']] = e['name']
            DishDic['%dunit' % e['id']] = e['unit']

        for e in t:
            d   = {}
            arr = t[e]
            for i in arr:
                did = i['dish_id']
                pic_key = '%dpic'%did
                name_key= '%dname'%did
                unit_key= '%dunit'%did
                if not d.get(did):
                    d[did] = {'num': i['num'], 'early': i['time1'], 'late': i['time1'], 'pic_loc': DishDic.get(pic_key, ''), 'name':DishDic.get(name_key, ''), 'unit':DishDic.get(unit_key, '')}
                else:
                    d[did]['num'] = d[did]['num'] + i['num']
                    if i['time1'] < d[did]['early']:
                        d[did]['early'] = i['time1']
                    if i['time1'] > d[did]['late']:
                        d[did]['late']  = i['time1']
            r[e] = d
        return r, DishDic
    #个人订单、管理员所有订单查看
    def get(self):
        uid          = int(self.get_secure_cookie('uid'))
        role         = int(self.get_secure_cookie('role'))
        action       = self.get_argument('action', '')
        device       = self.get_secure_cookie('pc_or_mobile')
        res          = []
        head    = self._get_head_nav()
        if action == 'orderlist':
            if role == conf.canteen_admin_role:
                res      = query_all_orders()
                dids     = [e['dish_id'] for e in res]
                dishes   = query_dish_by_ids(dids)

                uids     = [e['user_id'] for e in res]
                user     = query_user_by_ids(uids)

                D        = {}
                grp, D   = self._grp_orders(res)
                target   = '%s/AdminCanteen.html' % device
                self.render(target, device=device, head=head, orders=res, groups=grp, D=D, user=user)
            else:
                res      = query_orders_by_uid(uid)
                dids     = [e['dish_id'] for e in res]
                dishes   = query_dish_by_ids(dids)
                D        = {}
                for e in dishes:
                    D['%dpic'%e['id']] = e['pic_loc']
                    D['%dname'%e['id']] = e['name']
                target = '%s/Orderlist.html' % device 
                self.render(target, device=device, head=head, orders=res, D=D)
    #下单
    def post(self):
        did          = int(self.get_argument('r_did', 0))
        num          = int(self.get_argument('num', 0))
        price        = int(self.get_argument('r_price', 0))
        unit         = self.get_argument('unit', '')
        uid          = int(self.get_secure_cookie('uid'))
        r = write_order(uid, did, num, price, unit)
        self.write(str(r))
class OrderConfirmHandler(BaseHandler):
    def post(self):
        oid          = self.get_argument('order_id', '')
        if oid:
            r        = order_confirm(oid)
            self.write('ok')
class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("real_name");
        self.clear_cookie("nick_name");
        self.clear_cookie("real_img_url")
        self.clear_cookie("nick_img_url")
        self.clear_cookie("office_phone")
        self.clear_cookie("mobile_phone")
        self.clear_cookie("role")
        self.redirect("/")

class ConstructHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("Constructing!")

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
               (r'/menu', MenuHandler),
               (r'/add', AddHandler),
               (r'/up', AddHandler),
               (r'/dish', DishHandler),
               (r'/comment', CommentHandler),
               (r'/edit', EditHandler),
               (r'/delete', DeleteHandler),
               (r'/reserve', ReserveHandler),
               (r'/notice',  ConstructHandler),
              ]
    application = tornado.web.Application(handler, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
