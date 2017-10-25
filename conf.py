#-*- coding: utf-8 -*-
import ConfigParser

class Wxconf():
    def __init__(self, name):
        p = ConfigParser.ConfigParser()
        p.read(name)
        self.db_host    = p.get('db', 'host')
        self.db_port    = p.getint('db', 'port')
        self.db_pass    = p.get('db', 'password')
        self.db_user    = p.get('db', 'user')
        self.db_db      = p.get('db', 'db')
        self.db_encode  = p.get('db', 'encode')

        self.t_user     = p.get('table', 'user')
        self.t_dish     = p.get('table', 'dish')
        self.t_order    = p.get('table', 'order')
        self.t_comment  = p.get('table', 'comment')

        self.r_host     = p.get('redis',  'host')
        self.r_port     = p.getint('redis',  'port')
        self.r_pass     = p.get('redis',  'password')

        self.s_cache    = p.getint('system', 'cache')
        
        self.tpl_index_name = p.get('tpl', 'index_name')

        self.agent_name           = p.get('navhead', 'agent_name')
        self.canteen_service      = p.get('navhead', 'canteen_service')
        self.meeting_service      = p.get('navhead', 'meeting_service')
        self.property_service     = p.get('navhead', 'property_service')
        self.notice_service       = p.get('navhead', 'notice_service')
        self.personal_center      = p.get('navhead', 'personal_center')
        self.order_list           = p.get('navhead', 'order_list')
        self.member_management    = p.get('navhead', 'member_management')

        self.breakfast            = p.get('canteen', 'breakfast')
        self.lunch                = p.get('canteen', 'lunch')
        self.dinner               = p.get('canteen', 'dinner')
        self.reserve              = p.get('canteen', 'reserve')

        self.canteen_admin_mobile = p.get('role', 'canteen_admin_mobile')
        self.office_admin_mobile  = p.get('role', 'office_admin_mobile')

        self.timeoffset           = p.get('offset', 'timeoffset')
        self.getfood_offset       = p.get('offset', 'getfood_offset')
        self.orderfood_offset     = p.get('offset', 'orderfood_offset')
        self.notify_interval      = p.getint('offset', 'notify_interval')
        self.notify_hour          = p.getint('offset', 'notify_hour')
        self.notify_min           = p.getint('offset', 'notify_min')
        self.notify_cnt           = str(p.get('offset', 'notify_cnt'))


        self.corpid               = p.get('wx', 'corpid')
        self.secret               = p.get('wx', 'secret')
        self.access_token         = p.get('wx', 'access_token')
        self.userid               = p.get('wx', 'userid')
        self.userinfo             = p.get('wx', 'userinfo')
        self.msg                  = p.get('wx', 'msg')
        self.agentid              = p.get('wx', 'agentid')

        self.uselog               = p.getint('log', 'uselog')
        self.logloc               = p.get('log', 'location')
        self.interval_unit        = p.get('log', 'interval_unit')
        self.interval             = p.getint('log', 'interval')

        self.toparty              = p.get('message', 'toparty')
        self.history_limit        = p.getint('message', 'history_limit')

        self.breakfast_edit       = p.get('edit', 'breakfast_edit')
        self.lunch_edit           = p.get('edit', 'lunch_edit')
        self.supper_edit          = p.get('edit', 'supper_edit')
    def canteen(self):
        r = {} 
        r['breakfast']            = self.breakfast
        r['lunch']                = self.lunch
        r['dinner']               = self.dinner
        r['reserve']              = self.reserve
        r['fetch_time']           = self.fetch_time
        return r
    def navhead(self):
        r = {}
        r['agent_name']           = self.agent_name
        r['canteen_service']      = self.canteen_service
        r['meeting_service']      = self.meeting_service
        r['property_service']     = self.property_service
        r['notice_service']       = self.notice_service
        r['personal_center']      = self.personal_center
        r['order_list']           = self.order_list
        r['member_management']    = self.member_management
        return r
    def display(self):
        print(self.db_host)
        print(self.db_port)
        print(self.db_user)
        print(self.db_pass)
        print(self.db_db)
        print(self.db_encode)

        print(self.t_user)
        print(self.t_order)
        print(self.t_dish)
        print(self.t_comment)

        print(self.r_host)
        print(self.r_port)
        print(self.r_pass)

        print(self.s_cache)
        print(self.tpl_index_name)
        print(self.navhead())

        print(self.canteen_admin_role)
        print(self.office_admin_role)
        print(self.common_member_role)
        print(self.other_role)
conf    = Wxconf('./conf.txt')
if __name__ == "__main__":
    print(conf.notify_cnt)
