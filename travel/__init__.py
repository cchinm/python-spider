#! /usr/bin/python3
import json
from urllib import request
import urllib
from datetime import datetime
import asyncio
import aiohttp
import aiowebsocket
import websocket
from jsonpath import jsonpath

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

session = sessionmaker(bind=create_engine('yours mysqlurl',
                                          pool_size=200,
                                          pool_recycle=3600))


__all__=['urllib', 'datetime', 'asyncio', 'aiohttp', 'JsonDecode', 'JsonEncode']
JsonEncode = json.dumps
JsonDecode = json.loads


import random
wx_uas =[
    'Mozilla/5.0 (Linux; Android 8.1; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.143 Crosswalk/24.53.595.0 XWEB/358 MMWEBSDK/23 Mobile Safari/537.36 MicroMessenger/6.7.2.1340(0x2607023A) NetType/4G Language/zh_CN',
    'Mozilla/5.0 (Linux; Android 8.0; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044353 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools',
    'Mozilla/5.0 (Linux; Android 8.0; MHA-AL00 Build/HUAWEIMHA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/NON_NETWORK Language/zh_CN Process/tools',
    'Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044207 Mobile Safari/537.36 MicroMessenger/6.7.3.1340(0x26070332) NetType/4G Language/zh_CN Process/tools',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Mobile/14B150 MicroMessenger/7.0.3(0x17000321) NetType/WIFI Language/zh_CN',

]

mob_uas = []
pc_uas =[]


def fakeUserAgent(type=1):
    if type == 1:
        return random.choice(wx_uas)
    elif type == 2:
        return random.choice(mob_uas)
    elif type == 3:
        return random.choice(pc_uas)
    else:
        return 'SimpleCrawl +Request'


import abc


class ABCbase(object):

    __metaclass__=abc.ABCMeta


    @abc.abstractmethod
    def request(self, url, *args, **kwargs):
        return

    @abc.abstractmethod
    def parse(self, response, **kwargs):
        return


    @abc.abstractmethod
    def close(self):
        pass

    @abc.abstractmethod
    def run(self):
        return