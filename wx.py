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
        data  = {'touser': uid, 'toparty': '测试119', 'totag':'', 'msgtype':'text', 'agentid':aid, 'text':{'content': content}}
        data  = urllib.urlencode(data)
        req   = urllib2.Request(url=cmd, data=data)
        data  = urllib2.urlopen(req)
        res   = data.read()
        print(res)
wxapi = WxAPI()

if __name__ == '__main__':
#   res = wxapi.access_token()
    atk = '3X70xt-ol7wtZjqxOEJPPBs5FSv2-zQtjwQhlmEs3vZZ9MHa1qXPrb8WGc2XXfmTROSymCbAzYjBCWeB23YWH8GFaS27rPcj4xGaU8NEkc5kE_pETrYVsSiopVuoCK78gcTSBn9WN591IwCfq3kOxtCvd7RZNdXvSDBhh9b40L1K-gQ-jNuvUcZV4Qbz5goFJK2ET4CEb3iaOPMVDHS2_5NCooSzy5GsW1T8U5TN95tjico0ZwzaldU8PHqrM-IqzEo_64J5o6iBh9SwSw6SlC9aGvRGn5DUph3NIYUHQl8'
#   wxapi.msg(atk, 'TanQiang', conf.agentid, 'hello tanqiang')
    wxapi.msg(atk, 'TanQiang', conf.agentid, 'hello world')
