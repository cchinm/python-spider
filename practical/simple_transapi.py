"""
简单使用的翻译api，抓包获取有道翻译的翻译api.
使用次数过多容易被Ban，建议还是使用官方开放api
对参数进行解析，方便日常短词翻译。
"""

import requests
import hashlib
import time
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
           # "Cookie":'_ga=GA1.2.914577764.1561213321; OUTFOX_SEARCH_USER_ID_NCOO=834227477.8411206; OUTFOX_SEARCH_USER_ID="2076912312@10.168.11.11"; JSESSIONID=aaatO8n_MFD71fbGNnZUw; ___rl__test__cookies=1562080308876',
           "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
           "Host": "fanyi.youdao.com",
            "Origin": "http://fanyi.youdao.com",
            "Referer": "http://fanyi.youdao.com/",
            "X-Requested-With": "XMLHttpRequest"}


class YDaoTransApi:
    """
    有道翻译简单api， 建议申请开发者去官网申请api调用
    """
    def __init__(self):
        self.url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        self.timestmp = int(time.time()*1000) - 271
        self.formdata = {
        "i": "",
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": self.timestmp,
        "sign": "",
        "ts": self.timestmp // 10,
        "bv": "3a019e7d0dda4bcd253903675f2209a5",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME",
        }

    def md5(self, query):
        md = hashlib.md5()
        sign_text = "fanyideskweb" +  query + str(self.timestmp) + "@6f#X3=cCuncYssPsuRUE"

        md.update(sign_text.encode("utf8"))
        sign = md.hexdigest()
        self.formdata['sign'] = sign
        self.formdata['i'] = query

    def transapi(self, query):
        self.md5(query)

        sess = requests.Session()
        sess.get("http://fanyi.youdao.com/")
        req = sess.post(self.url, data=self.formdata, headers=headers)
        sess.close()
        print(req.text)


p = YDaoTransApi()
for i in range(100):
    p.transapi('sess.close()')