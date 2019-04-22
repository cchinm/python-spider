from scrapy.spiders import Spider
from scrapy import Request
import json, jsonpath
import re
from mingdata import items
from datetime import  datetime
from urllib import request
BILI_REQUEST_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://live.bilibili.com',
    'Referer': 'https://live.bilibili.com/p/eden/area-tags?parentAreaId=2&areaId=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
PAGE_SIZE = 50

class BiLiSpider(Spider):
    name = 'bililive'

    custom_settings = {'DEFAULT_REQUEST_HEADERS':BILI_REQUEST_HEADERS}


    # redis_key = 'bili:start_urls'
    # 直播频道与直播内容url
    start_urls = [
        'https://api.live.bilibili.com/room/v1/Area/getList',
    ]

    # 获取直播房间信息， 获取房间播主信息
    DEFAULT_URL_PREFIX = ['https://api.live.bilibili.com/room/v3/area/getRoomList?page={2}&platform=web'
                          '&parent_area_id={0}&cate_id=0&area_id={1}&sort_type=&page_size=50'
                          '&tag_version=1',
                          'https://api.live.bilibili.com/live_user/v1/UserInfo/get_anchor_in_room?roomid={}']

    def parse(self, response):
        """
        解析节目列表
        :param response:
        :return:
        """
        jsoninfo = json.loads(response.body)
        data = jsonpath.jsonpath(jsoninfo, '$..data[*].list[*]')
        for i in data[:]:
            yield Request(url=self.DEFAULT_URL_PREFIX[0].format(i['parent_id'], i['id'], 1),
                          headers=self.custom_settings['DEFAULT_REQUEST_HEADERS'],
                          meta={'type':i['id'], 'ptype':i['parent_id']},
                          callback=self.parse_room,
                          dont_filter=True)


    def parse_room(self, response):
        """
        解析每个频道下的房间，
        并找下一页的房间信息
        :param response:
        :return:
        """
        jsoninfo = json.loads(response.body)
        total = jsoninfo['data']['count']
        print('total ', total)
        pages = total // PAGE_SIZE + 1
        response.meta['total'] = total
        for i in range(1, pages+1):
            tmp = self.custom_settings['DEFAULT_REQUEST_HEADERS'].copy()
            tmp['Referer'] = "https://live.bilibili.com/p/eden/area-tags?parentAreaId" \
                              "={}&areaId={}&visit_id=4wzs7yoxvshs".format(response.meta['ptype'],
                                response.meta['type'])

            yield Request(url=self.DEFAULT_URL_PREFIX[0].format(response.meta['ptype'],
                                                                response.meta['type'],
                                                                i),
                      headers=tmp,
                      meta=response.meta,
                      callback=self.parse_room_info,
                     dont_filter=True)

    def parse_room_info(self, response):
        """
        房间信息详情，并将信息value存入item
        :param response:
        :return:
        """
        # print(response.url)
        item = items.BiliItem()
        jsoninfo = json.loads(response.body)
        data = jsonpath.jsonpath(jsoninfo, '$..data.list[*]') or []
        item['tid'] = response.meta.get('type',-1)
        item['pid'] = response.meta.get('ptype', -1)
        item['total'] = response.meta.get('total', 0)
        item['ctime'] = datetime.now().strftime('%Y-%m-%d %H:00:00')
        item['male'] = 0
        item['female'] = 0
        item['max_count'] = 0
        item['count'] = 0
        # print(data)
        for d in data:
            item['max_count'] = item['max_count'] if item['max_count'] > d['online'] else d['online']
            item['count'] += d['online']
            item['room_id'] = d['roomid']
            yield item.copy()

        # 获取房间主播性别信息
        # IO堵塞太高，采用扩展件后处理方式提高效率
        #     gender = self.gender_resolve(self.DEFAULT_URL_PREFIX[1].format(d['roomid']))
        #     if gender == 1:
        #         item['male'] += 1
        #     elif gender == 0:
        #         item['female'] += 1
        # print(response.url[-8:])
        # print(item)

        # item['room_id'] = -1
        # yield item.copy()

    def gender_resolve(self, url):
        proxy = request.ProxyHandler({'http':'14.17.121.132:12138'})
        opener = request.build_opener(proxy)
        req = request.Request(url=url, headers=self.custom_settings['DEFAULT_REQUEST_HEADERS'])
        response = opener.open(req)
        jsoninfo = json.loads(response.read())
        data = jsonpath.jsonpath(jsoninfo, '$..gender')[0]
        # print('gender', data, type(data))
        return data
