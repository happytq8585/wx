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

wxapi = WxAPI()

if __name__ == '__main__':
    res = wxapi.access_token()
    #res = json.loads(res)
    print res
    a_tk = res['access_token']
    code = 'z6WyXWLZpGQ4Jw8i0S69YYoqj83km7rbj_iK7q-DsuM'
    res = wxapi.userid(a_tk, code)
    print res

    uid = res['UserId']

    res = wxapi.userinfo(a_tk, uid)
    print res
