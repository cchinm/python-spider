# -*- coding:UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
import json, jsonpath
from urllib import urlencode
from model import session, TcityCode, TcompInfo
from baidu_params import data, search_param_city, headers
import re
import copy
from gevent import queue
import gevent
from gevent import monkey, pool;monkey.patch_all()


compInfo = TcompInfo.__table__.insert().prefix_with("ignore")
cityCode = TcityCode.__table__.insert().prefix_with("ignore")
sess = session()
qn = queue.Queue(maxsize=20)


def request(url, data, headers):
    """

    :param url: uri
    :param data: request data
    :param headers: random requested headers
    :return:
    """
    if data is None:
        t = requests.get(url, headers=headers, proxies={'your proxies':'xxx'})
        return t

    _data = urlencode(data)
    t = requests.get(url+_data,
                     headers=headers,
                     proxies={'your proxies':'xxx',})
    return t




def getall(url, data, headers):
    """
    Search for relevant company information based on input keywords
    :param url:
    :param data:
    :param headers:
    :return:
    """
    name = ('孵化器/孵化中心/科技Y/智慧Y/软件Y/创新Y/创意Y/创业Y/科学Y/科技Y'
            '/科创Y/信息Y/金融Y/生态Y/生医Y/生物Y/服务Y/产业X/创意X/文化X/科技X'
            '/创新X/科创X/高新X/技术X/电子X/智造X/信息X/互联网X/金融X/医学X')
    for _name in name.split("/"):
        if 'Y' in _name:
            for t in ('园', '谷', '港'):
                _data = data.copy()
                _data['wd'] = re.sub('Y', t, _name)
                yield request(url=url, data=_data, headers=headers), _data
            continue

        if 'X' in _name:
            for t in ('产业园','园区','基地','中心'):
                _data = data.copy()
                _data['wd'] = re.sub('X', t, _name)
                yield request(url=url, data=_data, headers=headers), _data
            continue
        _data = data.copy()
        _data['wd'] = _name
        yield request(url=url, data=_data, headers=headers), _data

def search_city():
    """
    search city code and put it to the queue.

    :return:
    """
    url = 'https://map.baidu.com/?'
    headers = {'referer': "https//map.baidu.com/search/%E5%AD%B5%E5%8C%96%E5%99%A8/@11606355.22,4669275.879999999,5z?querytype=s&da_src=shareurl&wd=%E5%AD%B5%E5%8C%96%E5%99%A8&c=1&src=0&pn=0&sug=0&l=5&b=(3725737.959983792,2695764.749996028;19454377.959983792,6283860.749996028)&from=webmap&biz_forward=%7B%22scaler%221,%22styles%22%22pl%22%7D&device_ratio=1",
               'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",}

    for i, _data in getall(url, data, headers):
        count = 0
        resp = json.loads(i.content)

        city_list = jsonpath.jsonpath(resp, '$..more_city[*]') or []
        hot_citys = jsonpath.jsonpath(resp, '$..hot_city[*]') or []
        data_list = []
        for city in hot_citys:
            name, code = city.split("|")
            data_list.append({'p_code':0, 'code':code, 'name':name})
            count += 1
        for city in city_list:
            pcode = city['province_id']
            data_list.append({'p_code':0, 'code':city['province_id'], 'name':city['province']})
            for c in city['city']:
                data_list.append({'p_code':pcode, 'code':c['code'], 'name':c['name']})
                count+=1
        qn.put(data_list)



def parse(url, data, headers):
    """
    page turning and parsing json
    :param url:
    :param data:
    :param headers:
    :return:
    """
    data['nn'] = int(data['nn']) + 10
    data['pn'] = int(data['pn']) + 1
    req = request(url, data, headers)
    if req.status_code == 200:
        resp = json.loads(req.content)
        cot = resp.get('content', False) or []
        if len(cot) == 0:
            return
        task = []
        for i in cot:
            try:
                item = dict()
                item['name'] = i['name']
                item['lat'] = i['diPointX']/10000000.
                item['lng'] = i['diPointY']/10000000.
                item['area_name'] = i['area_name']
                item['aid'] = i['admin_info']['area_id']
                item['cid'] = i['admin_info']['city_id']
                item['addr'] = i['addr']
                item['tags'] = i['std_tag']
                item['kw'] = data['wd']
                task.append(item.copy())
            except:
                continue
        qn.put(copy.deepcopy(task))
        parse(url=url, data=data, headers=headers)




def search_keyword(data, headers):
    """
    Request api and
    parse information.
    If not end , continue to execute recursion function
    :param data:
    :param headers:
    :return:
    """
    global sess
    uri = ('https://map.baidu.com/?')
    for i, _data in getall(url=uri, data=data, headers=headers):
        resp = json.loads(i.content)
        cot = resp.get('content', False) or []
        if len(cot) == 0:
            continue
        task = []
        for i in cot:
            try:
                item = dict()
                item['name'] = i['name']
                item['lat'] = i['diPointX']/10000000.
                item['lng'] = i['diPointY']/10000000.
                item['area_name'] = i['area_name']
                item['aid'] = i['admin_info']['area_id']
                item['cid'] = i['admin_info']['city_id']
                item['addr'] = i['addr']
                item['tags'] = i['std_tag']
                item['kw'] = _data['wd']
                task.append(item.copy())
            except:
                continue
        qn.put(copy.deepcopy(task))
        parse(url=uri, data=_data, headers=headers)


def writeAssist(table):
    """
    Read data from the queue
    and write it to the mysql database
    :return:
    """
    while True:
        try:
            elem = qn.get(1000)
            count = 0
            while count < 3:
                try:
                    sess.execute(table, elem)
                    sess.commit()
                    break
                except:
                    count += 1
        except:
            break



def seekCityCode():
    """
    This script is required for the initialization operation.
    If you don't want this step, you can ignore it directly.
    :return:
    """
    gt = [gevent.spawn(search_city),
          gevent.spawn(writeAssist, cityCode)]
    gevent.joinall(gt)


def main():
    """
    main function
    Crawl the  technology park information for each city
    :return:
    """
    global data
    gpool = pool.Pool(size=5)
    _data = data
    result = sess.execute('select code from city_code where p_code <> 0').fetchall()
    sess.commit()
    gt = []
    gt.append(gpool.spawn(writeAssist, compInfo))
    for _id in result:
        print(_id)
        _data['c'] = _id[0]
        gt.append(gpool.spawn(search_keyword, _data.copy(), headers()))
    gevent.joinall(gt)



# initialize this script.
# run
# seekCityCode()
# main()


