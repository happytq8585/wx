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

from data import query_dish_by_day

define("port", default=8000, help="run on the given port", type=int)

user_cache = {}

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

class UploadFileHandler(BaseHandler):
    def _get_time_delta(self, kind):
        if kind == 0x0000:
            return ' 07:30:00'
        if kind == 0x0010:
            return ' 07:30:00'
        if kind == 0x0100:
            return ' 11:30:00'
        if kind == 0x1000:
            return ' 17:30:00'
        return ' 00:00:00'
    @tornado.web.authenticated
    def post(self):
        if not os.path.exists("static/files"):
            os.makedirs("static/files");
        day = self.get_argument("day", None)
        if not day:
            self.write("no day parameter")
        else:
            kind          = int(self.get_argument('dish_order', 0))
            delta         = self._get_time_delta(kind)
            now = time.strftime("%Y-%m-%d %H:%m:%S")
            if now > day + delta:
                self.write('不能上传现在时刻之前的菜了')
                return
            arr = [int(e) for e in day.split('-')]
            timestamp = "%4d%02d%02d"%(arr[0], arr[1], arr[2])
            todaydir = "static/files/" + timestamp
            upload_path = os.path.join(os.path.dirname(__file__), todaydir)
            file_metas  = self.request.files.get('file')
            filename = ''
            if file_metas:
                meta = file_metas[0]
                filename = meta.get('filename', '')
            if filename:
                if not os.path.exists(todaydir):
                    os.makedirs(todaydir)
                filename = todaydir + '/' +  filename
                with open(filename, 'wb') as up:
                    up.write(meta['body'])
            name          = self.get_argument('dish_name', '')
            pic_loc       = filename
            t             = day 
            material      = self.get_argument('dish_material', '')
            price         = self.get_argument('dish_price', 0)
            if price == '':
                price = 0
            unit          = self.get_argument('dish_unit', '')
            print(name, pic_loc, t, material, int(kind), int(price), unit)
            write_dish(name, pic_loc, t, material, int(kind), int(price), unit)
            self.write('上传成功!')

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        code = self.get_argument('code', None)
        if not code:
            self.finish()
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
                        self._write_user_cache(info)
                        self.render('index.html')
    def _write_user_cache(self, u):
        mobile = u.get('mobile', '')
        self.set_secure_cookie('mobile', mobile)
        user_cache[mobile] = u

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
        self.render('add.html')
    @tornado.web.authenticated
    def post(self):
        pass

class DeleteDishHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        did      = int(self.get_argument('id', 0))
        if did:
            ordered = query_order_by_dish_id(did)
            if not ordered:
                delete_dish_by_id(did)
                self.write('delete success')
            else:
                self.set_status(400)
        else:
            self.write('dish id is invalid')

class CanteenItemBottomModule(tornado.web.UIModule):
    def render(self, comments, device):
        target = '%s/canteenList/modules/canteen_item_bottom.html' % device
        return self.render_string(target, comments=comments)

class CanteenItemHandler(BaseHandler):
    def _already_comment(self, comments):
        uid       = int(self.get_secure_cookie('uid'))
        for e in comments:
            if e['user_id'] == int(uid):
                return e['stars']
        return 0
    @tornado.web.authenticated
    def get(self):
        did           = int(self.get_argument('id', 0))
        if did:
            dish      = query_dish_by_id(did)
            kind      = dish['kind']
            uid       = int(self.get_secure_cookie('uid'))
            ordered   = False
            if kind == 0x0000:
                ordered = query_already_ordered(uid, did)
            comments  = query_comments_by_dish_id(did)
            user_comment = self._already_comment(comments)
            device    = self.get_secure_cookie('pc_or_mobile')
            target    = '%s/canteenList/canteenList.html' % device
            head      = self._get_head_nav()
            canteen   = self._get_canteen()
            t         = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.render(target, head=head, canteen=canteen, device=device, comments=comments, dish=dish, user_comment=user_comment, T=t, ordered=ordered)
    #handle comments
    def post(self):
        did           = int(self.get_argument('id', 0))
        if did:
            uid       = int(self.get_secure_cookie('uid'))
            real_name = self.get_secure_cookie('real_name')
            nick_name = self.get_secure_cookie('nick_name')
            r_img_url = self.get_secure_cookie('real_img_url')
            n_img_url = self.get_secure_cookie('nick_img_url')
            stars     = int(self.get_argument('star', 0))
            words     = self.get_argument('words', '')
            write_comment(did, uid, real_name, nick_name, r_img_url, n_img_url, stars, words)
            self.write('comment successfully!')

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
               (r'/notice',  ConstructHandler),
              ]
    application = tornado.web.Application(handler, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
