# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     wx_pyq_report
   Description :  微信年度朋友圈报表
   Author :       zm.z
   date：          2019/11/5
-------------------------------------------------
   Change Activity:
                   2019/11/5:
-------------------------------------------------
"""
__author__ = 'zm.z'
import re
import jieba
import sqlite3
import datetime
import pandas
db_dir = "./SnsMicroMsg.db"
db_select = "select createTime, content, attrBuf from SnsInfo"

def save_data():
    db_dir = "./SnsMicroMsg.db"
    cursor = sqlite3.connect(db_dir)
    result = cursor.execute(db_select)

    year_month_post = dict()
    year_hour_post = dict()
    year_month_origin = dict()
    # print(result)
    word_count = dict()

    for createTime, content, attrBuf in result:
        dt = datetime.datetime.fromtimestamp(createTime)
        year_month_post[dt.strftime("%Y-%m")] = year_month_post.get(dt.strftime("%Y-%m"), 0) + 1
        year_hour_post[dt.strftime("%Y-%H")] = year_hour_post.get(dt.strftime("%Y-%H"), 0) + 1
        cot = re.search(b"\x05.(.+?)2&\r", content)
        # print(content)
        if cot:
            # print(str(cot.group(1), encoding="utf8", errors="ignore"))
            cot = re.sub("[^\u4e00-\u9fa5]", "", str(cot.group(1), encoding="utf8", errors="ignore"))
            for i in jieba.cut(cot, cut_all=False):
                if len(i) == 1:
                    continue
                word_count[i] = word_count.get(i, 0) + 1
            year_month_origin[dt.strftime("%Y-%m")] = year_month_origin.get(dt.strftime("%Y-%m"), 0) + 1
        # print(content)

        # print(str(content, encoding="utf8", errors="ignore"))
    print(year_month_post)
    print(year_hour_post)
    print(year_month_origin)
    print(word_count)

    writer = pandas.ExcelWriter("test1.xlsx")
    pandas.DataFrame([{"timeM":k, "ymPost":v, "ymPostOrigin":year_month_origin[k]} for k, v in year_month_post.items()]
                     ).to_excel(writer, sheet_name="df1")
    pandas.DataFrame(
        [{"timeH": k, "yhPost": v,} for k, v in year_hour_post.items()]
        ).to_excel(writer, sheet_name="df2")

    pandas.DataFrame(
        [{"word":k, "count":v} for k, v in word_count.items()]
    ).to_excel(writer, sheet_name="df3")
    # pandas.DataFrame().to_excel(writer, sheet_name="df")
    writer.save()

if __name__ == '__main__':
    save_data()
