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

from data   import query_user, query_dish_by_day, write_dish
from data   import delete_dish_by_id, query_comments_by_dish_id
from data   import query_dish_by_id, write_comment, update_password
from data   import update_personal_info, query_user_by_id, query_user_all
from data   import update_user_by_id, add_user, delete_user_by_id
from data   import write_order, query_all_orders, query_orders_by_uid
from data   import query_dish_by_ids, query_user_by_ids
from data   import order_confirm, query_order_by_dish_id
from conf import conf
define("port", default=8000, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("real_name")
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
    @tornado.web.authenticated
    def post(self):
        if not os.path.exists("static/files"):
            os.makedirs("static/files");
        day = self.get_argument("day", None)
        if not day:
            self.write("no day parameter")
        else:
            arr = [int(e) for e in day.split('-')]
            timestamp = "%4d%02d%02d"%(arr[0], arr[1], arr[2])
            todaydir = "static/files/" + timestamp
            if not os.path.exists(todaydir):
                os.makedirs(todaydir)
            upload_path = os.path.join(os.path.dirname(__file__), todaydir)
            file_metas  = self.request.files['file']
            meta = file_metas[0]
            filename = meta['filename']
            filename = todaydir + '/' +  filename
            with open(filename, 'wb') as up:
                up.write(meta['body'])
            name          = self.get_argument('dish_name', '')
            pic_loc       = filename
            t             = day 
            material      = self.get_argument('dish_material', '')
            kind          = self.get_argument('dish_order', 0)
            price         = self.get_argument('dish_price', 0)
            if price == '':
                price = 0
            unit          = self.get_argument('dish_unit', '')
            print(name, pic_loc, t, material, int(kind), int(price), unit)
            write_dish(name, pic_loc, t, material, int(kind), int(price), unit)
            self.write('上传成功!')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        r = checkMobile(self.request)
        device = ''
        if r:
            device = 'mobile'
            self.set_secure_cookie('pc_or_mobile', device)
        else:
            device = 'pc'
            self.set_secure_cookie('pc_or_mobile', device)
        target = device + '/' + 'index.html'
        self.render(target, name=conf.tpl_index_name, device=device)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        device = self.get_secure_cookie('pc_or_mobile')
        target = device + '/' + 'index.html'
        self.render(target, name=conf.tpl_index_name, device=device)
    def post(self):
        rname = self.get_argument("real_name")
        upass = self.get_argument("password")
        e     = query_user(rname, upass)#返回user表的字典
        if not e:
            self.set_status(400)
        else:
            print(e)
            self._write_cookie(e)
    def _write_cookie(self, e):
        if e:
            self.set_secure_cookie('uid', str(e['id']), expires_days=None)
            self.set_secure_cookie('real_name', e['real_name'], expires_days=None)
            self.set_secure_cookie('nick_name', e['nick_name'], expires_days=None)
            self.set_secure_cookie('real_img_url', e['real_img_url'], expires_days=None)
            self.set_secure_cookie('nick_img_url', e['nick_img_url'], expires_days=None)
            self.set_secure_cookie('office_phone', e['office_phone'], expires_days=None)
            self.set_secure_cookie('mobile_phone', e['mobile_phone'], expires_days=None)
            self.set_secure_cookie('role', str(e['role']), expires_days=None)
class BreakfastModule(tornado.web.UIModule):
    def render(self, arr, device, role, t):
        target = '%s/canteen/modules/breakfast.html' % device
        return self.render_string(target, breakfast=arr, role=role, conf=conf, T=t)
class LunchModule(tornado.web.UIModule):
    def render(self, arr, device, role, t):
        target = '%s/canteen/modules/lunch.html' % device
        return self.render_string(target, lunch=arr, role=role, conf=conf, T=t)
class DinnerModule(tornado.web.UIModule):
    def render(self, arr, device, role, t):
        target = '%s/canteen/modules/dinner.html' % device
        return self.render_string(target, dinner=arr, role=role, conf=conf, T=t)
class ReserveModule(tornado.web.UIModule):
    def render(self, arr, device, role, t):
        target = '%s/canteen/modules/reserve.html' % device
        return self.render_string(target, reserve=arr, role=role, conf=conf, T=t)
class TabModule(tornado.web.UIModule):
    def render(self, arr, device, canteen, role):
        breakfast = []
        lunch     = []
        dinner    = []
        reserve   = []
        for e in arr:
            if e['kind'] == 0x0000:
                reserve.append(e)
            elif e['kind'] == 0x0010:
                breakfast.append(e)
            elif e['kind'] == 0x0100:
                lunch.append(e)
            elif e['kind'] == 0x1000:
                dinner.append(e)
            else:
                pass
        target = '%s/canteen/modules/tab.html' % device
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        return self.render_string(target, canteen=canteen, breakfast=breakfast,lunch=lunch, dinner=dinner, reserve=reserve, device=device, role=role, conf=conf, T=t)

class PublicData():
    def __init__(self, name, role):
        self.real_name    = name
        self.role         = int(role)
    def get_head(self):
        head = {}
        head['agent_name']       = conf.agent_name
        head['canteen_service']  = conf.canteen_service
        head['meeting_service']  = conf.meeting_service
        head['notice_service']   = conf.notice_service
        head['property_service'] = conf.property_service
        head['real_name']        = self.real_name
        head['personal_center']  = conf.personal_center
        head['order_list']       = conf.order_list
        head['member_management']= conf.member_management
        head['role']             = self.role
        head['conf']             = conf
        return head
    def get_canteen(self):
        canteen  = {}
        canteen['breakfast']     = conf.breakfast
        canteen['lunch']         = conf.lunch
        canteen['dinner']        = conf.dinner
        canteen['reserve']       = conf.reserve
        return canteen
class CanteenHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        head    = self._get_head_nav()
        canteen = self._get_canteen()
        role    = int(self.get_role())
        device  = self.get_secure_cookie('pc_or_mobile')
        target  = '%s/canteen/canteen.html' % device
        self.render(target, head=head, canteen=canteen, device=device, role=role, conf=conf)
    @tornado.web.authenticated
    def post(self):
        day     = self.get_argument('day', None)
        if day:
            arr     = query_dish_by_day(day)
            device  = self.get_secure_cookie('pc_or_mobile')
            canteen = self._get_canteen()
            role    = int(self.get_role())
            target  = '%s/canteen/modules/tab_tmp.html' % device
            self.render(target, dishes=arr, device=device, canteen=canteen, role=role)

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
    def _alread_comment(self, comments):
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
            comments  = query_comments_by_dish_id(did)
            user_comment = self._alread_comment(comments)
            device    = self.get_secure_cookie('pc_or_mobile')
            target    = '%s/canteenList/canteenList.html' % device
            head      = self._get_head_nav()
            canteen   = self._get_canteen()
            t         = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.render(target, head=head, canteen=canteen, device=device, comments=comments, dish=dish, user_comment=user_comment, T=t)
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
        elif action == 'orderlist':
            if role == conf.canteen_admin_role:#admin
                target    = '%s/personal/AdminCanteen.html' % device
                self.render(target, device=device, head=head, canteen=canteen)
            elif role == conf.common_member_role:#members
                target    = '%s/personal/OrderList.html' % device
                self.render(target, device=device, head=head, canteen=canteen)
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
        get_time     = self.get_argument('g_time', '')
        unit         = self.get_argument('unit', '')
        uid          = int(self.get_secure_cookie('uid'))
        r = write_order(uid, did, num, price, unit, get_time)
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
    ui_modules = {'Breakfast_module':BreakfastModule,
                  'Lunch_module':LunchModule,
                  'Dinner_module':DinnerModule,
                  'Reserve_module':ReserveModule,
                  'Tab_tmp_module':TabModule,
                  'Canteen_item_bottom_module':CanteenItemBottomModule}
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,
        "login_url": "/login",
        "ui_modules":ui_modules,
        "debug":True}
    handler = [
               (r"/static/(.*)", StaticFileHandler, {"path": "static"}),  
               (r"/css/(.*)", StaticFileHandler, {"path": "static/css"}),  
               (r"/js/(.*)", StaticFileHandler, {"path": "static/js"}),  
               (r"/img/(.*)", StaticFileHandler, {"path": "static/img"}), 
               (r'/', IndexHandler),
               (r'/login', LoginHandler),
               (r'/canteen', CanteenHandler),
               (r'/canteenItem', CanteenItemHandler),
               (r'/comment', CanteenItemHandler),
               (r'/up', UploadFileHandler),
               (r'/delete', DeleteDishHandler),
               (r'/personal', PersonalHandler),
               (r'/order', OrderHandler),
               (r'/orderconfirm', OrderConfirmHandler),
               (r'/logout', LogoutHandler),
               (r'/meeting', ConstructHandler),
               (r'/property',ConstructHandler),
               (r'/notice',  ConstructHandler),
              ]
    application = tornado.web.Application(handler, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
