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
    atk = 'HLz8MIrI9ClphUP0KNONARnu5NzRVxZGRGz0g3oMRT0h0H2p4wWqSfsx1D6qSqzu6xZ5Ia8dFXj2JsM_2OMkNBpBMTQwn2vflqTgsmY74WXrsFTT5vfPy7nYGZV9GgXBK9jsp8YHUEAax67_jMoqtOhPnzmQzvvGhVq1lojsxgLYi4Z0ECBMNR0tgO2LCrZqML9PyeG9GLpUMYisoHPqDC5f-Q6zDtr5vdvXS0yjEwnrLUmICt2Ztq3jliN5Yuz6K_4Lw8QvD02v69zzsuCwW6OMxMVxFXzBpxCzFWHtSCM'
#   wxapi.msg(atk, 'TanQiang', conf.agentid, 'hello tanqiang')
    wxapi.msg(atk, 'ZhengErYang', 1000002, '您的包子已领取！')
