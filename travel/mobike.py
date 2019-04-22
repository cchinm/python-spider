#! /usr/bin/python3

import travel
from travel import request, session, fakeUserAgent
import asyncio, aiohttp
from numpy import arange
from travel import ABCbase as abcSpider

# 1 latitude ~= 111km; 1 longitude ~= 111km.
# 你选取的经纬度范围
first_latlng = (23.032330,113.3586326 )
last_latlng = (23.073841, 113.41520)
# 经纬度间的间隔,约166m
step = .02

mb_url = 'https://mwx.mobike.com/nearby/nearbyBikeInfo'
mb_vars = {'longitude':113.384090, 'latitude':23.04916, 'citycode':'020', 'biketype':1}
mb_headers = {
    'host': "mwx.mobike.com",
    'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Mobile/14B150 MicroMessenger/7.0.3(0x17000321) NetType/WIFI Language/zh_CN",
    'referer': "https://servicewechat.com/wx80f809371ae33eda/424/page-frame.html",
    'wxapp': "1",
    'mainsource': "4003",
    'platform': "3",
    'eption': "efde6",
    'content-type': "application/x-www-form-urlencoded",
    'citycode': "020",
    }

'''
create database sql

CREATE TABLE `sth_location_data`  (
  `sth_id` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `sthlat` decimal(10, 6) DEFAULT NULL,
  `sthlng` decimal(10, 6) DEFAULT NULL,
  `ctime` datetime(0) DEFAULT NULL,
  `type` int(1) DEFAULT NULL,
  `source_id` int(5) DEFAULT NULL,
  UNIQUE INDEX `key_1`(`sth_id`, `ctime`) USING BTREE,
  INDEX `key_2`(`type`, `source_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic

'''
tmp_sql = '''
    INSERT IGNORE INTO `sth_location_data`(`sth_id`, 
    `sthlat`, `sthlng`, `ctime`, `type`, `source_id`) 
VALUES ('%s', %s, %s, '%s', 0, 1)
'''
sessali = session()


class MobileBike(abcSpider):

    name = 'mobileBike'
    headers = mb_headers


    async def request(self, url:str, *args, **kwargs):
        """
        向uri发送请求，data相应参数，header请求头
        :param url:
        :param args:
        :param kwargs:
        :return:
        """
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url=url, data=kwargs['data'], headers=kwargs['headers']) as resp:
                _resp = await resp.text()
                return _resp

    def parse(self, future, **kwargs):
        """
        解析请求后的返回结果
        :param future: future类型的对象
        :param kwargs:
        :return:
        """
        resp = travel.JsonDecode(future.result())
        objects = travel.jsonpath(resp, '$..object[*]') or []
        for item in objects:
            lat = round(item['distY'],6)
            lng = round(item['distX'],6)
            sth_id = hex(int(item['bikeIds'][:-1]))[2:]
            ctime = travel.datetime.now().strftime('%Y-%m-%d %H:00:00')
            print(tmp_sql % (sth_id, lng, lat, ctime))
            sessali.execute(tmp_sql%(sth_id, lat, lng, ctime))
            sessali.commit()


    def run(self):
        """
        执行这个函数，采用AIO方式
        :return:
        """
        global first_latlng, last_latlng, step
        # 获取两个经纬度间的点阵
        localtions = ((i,j) for i in arange(first_latlng[0], last_latlng[0], step)
                      for j in arange(first_latlng[1], last_latlng[1], step))
        while True:
            task = []
            count = 0
            headers = self.headers.copy()
            headers['user-agent'] = fakeUserAgent(1)
            for x, y in localtions:
                count += 1
                # 构造请求参数
                data = mb_vars.copy()
                data['longitude'] = round(y, 7)
                data['latitude'] = round(x, 7)
                print(data)
                # 控制并发数在30以内
                cor = asyncio.ensure_future(
                    self.request(url=mb_url, data=data, headers=headers)
                )
                cor.add_done_callback((self.parse)) # 添加解析回调函数
                task.append(cor)

                if count > 29:
                    break
            else:
                loop_handlers = asyncio.get_event_loop()
                loop_handlers.run_until_complete(asyncio.wait(task))
                break
            loop_handlers = asyncio.get_event_loop()
            loop_handlers.run_until_complete(asyncio.wait(task))


    def close(self):
        pass


if __name__ == '__main__':
    p = MobileBike()
    p.run()
