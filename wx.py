#-*- coding: utf-8 -*-

import urllib2
import urllib
import json

from conf import conf

class WxAPI():
    def _same_api(self, cmd):
        req   = urllib2.Request(cmd)
        data  = urllib2.urlopen(req)
        res   = data.read()
        return json.loads(res)

    def access_token(self):
        cmd   = conf.access_token % (conf.corpid, conf.secret)
        r     = self._same_api(cmd)
        return r.get('access_token')
    def userid(self, access_token, code):
        cmd   = conf.userid % (access_token, code)
        r     = self._same_api(cmd)
        return r.get('UserId')
    def userinfo(self, access_token, uid):
        cmd  = conf.userinfo % (access_token, uid)
        r    = self._same_api(cmd)
        return r
    def msg(self, access_token, uid, aid, content):
        cmd   = conf.msg % (access_token)
        print(cmd)
        #data  = {'touser': uid, 'toparty': conf.toparty, 'totag':'', 'msgtype':'text', 'agentid':aid, 'text':{'content': content}}
        data  = {'touser': uid, 'totag':'', 'msgtype':'text', 'agentid':aid, 'text':{'content': content}}

        #data  = urllib.urlencode(data)
        data = json.dumps(data)
        print(data)
        req   = urllib2.Request(url=cmd, data=data)
        data  = urllib2.urlopen(req)
        res   = data.read()
        print(res)
wxapi = WxAPI()

if __name__ == '__main__':
#   res = wxapi.access_token()
    atk = 'bDDS-eWlbTcsDgQiXav2M3iTcUYt1HMCqUWvlmWpX_BaBL_6lIp6Eqe3H-uGGRbWCcqGaZt6B_52U02n6zrXW9Hz4KXuWShpv0aecAwi8f1pfYrsy--2OYxjeGEiWyXhJ8PYV7BJBgg-eqg9vPoc6y_T_YRFbvTfsCdNkvU1wrYoqVP3r05mZxN9Z0jAOkpyo1Io2hg1fU7UdbgJuoX-POHA-immuss46n9YO7afN_IJ7JR6ReHM9N9fir7QoeCTwOYFSwVgb4R7sc161nW3XQmYEqaUSaDi9Y5j4wSN--0'
    code = 'BuCvi7f8pJbiE1rOekiJSDRhFI6mPphLIFZp6Nb1X6U'
    user = wxapi.userinfo(atk, code)
    print(user)
#   wxapi.msg(atk, 'TanQiang', conf.agentid, 'hello tanqiang')
#   wxapi.msg(atk, 'ZhengErYang', 1000002, '您的包子已领取！')
