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
        data  = {'touser': uid, 'msgtype':'text', 'agentid':aid, 'text':{'content': content}}
        data  = urllib.urlencode(data)
        req   = urllib2.Request(cmd, data)
        data  = urllib2.urlopen(req)
        res   = data.read()
        print(res)
wxapi = WxAPI()

if __name__ == '__main__':
    res = wxapi.access_token()
    atk = 'BX-8o8S1T84CJtUP2uVVqoufZ7YQKqUjCpbMfiOBvf-EJEHxZLmC2hRWPTqgsA0VhHkjjtWavfRhDUiVrRYuKHAESbqtY7npY8c75Sn3Py2geb1XN1NlAvTAb2eMJ2RCqbU1xRlOLl3854QKgjBwh0KvMudcoMAGC91g4r_m7yPqNe4Z0e8KhJOcq020xtdaUXRijy7WERCuugLjNc4zC2oZfz_vBOcNfI1G6cIN-QpH-lrzCHDk2nP9DOs1j2kORcCZOCg4vHdK8OvFefw8uioq-oDpGI2O0dZdmXsQuGo'
    wxapi.msg(atk, '@all', conf.agentid, 'hello tanqiang')
