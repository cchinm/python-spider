# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import pymysql
class MingdataPipeline(object):


    def __init__(self):
        param = dict(host='yourshost', user='root', password='yourpasswords',
            db='yourdb', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.pool = adbapi.ConnectionPool('pymysql',
                                          **param)

    def process_item(self, item, spider):
        self.pool.runInteraction(self.do_insert, item).addErrback(self.handler)
        return item

    def do_insert(self,cursor, item):
        if item['room_id'] == -1:
            sql = 'insert ignore into bili_live_data(area_id, parea_id, male, female, ctime, total, sum, amo) ' \
                  'values (%(tid)s, %(pid)s, %(male)s, %(female)s, \'%(ctime)s\', %(total)s, %(count)s, %(max_count)s) ' \
                  ' ON DUPLICATE KEY UPDATE male=male+%(male)s, female=female+%(female)s, ' \
                  'sum=sum+ %(count)s, amo = if(amo > %(max_count)s, amo, %(max_count)s), pages=pages+1'
            print(sql % item)
            cursor.execute(sql % item)
        else:
            sql = 'insert ignore into bili_live_room(area_id, ctime, room_id, parea_id) ' \
                  'values (%(tid)s, "%(ctime)s", %(room_id)s, %(pid)s)'
            print(sql % item)
            cursor.execute(sql % item)

    def handler(self,e):
        print(e)

