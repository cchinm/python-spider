import aiohttp
import asyncio
from lxml import html
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
tasks = []
urls = [
    ('http://quote.eastmoney.com/stock_list.html#sh', 'sh'),
    ('http://quote.eastmoney.com/stock_list.html#sz', 'sz'),
    ]

bd_url = 'https://gupiao.baidu.com/api/stocks/stockdaybar?from=pc&os_ver=1&cuid=xxx&vv=100&format=json' \
         '&stock_code=%s%s&step=3&start=&count=160&fq_type=no&timestamp=1558624339268'


sh_url = 'http://www.sse.com.cn/assortment/stock/list/share/'
# http://query.sse.com.cn/security/stock/getStockListData2.do?
# &jsonCallBack=jsonpCallback97486&isPagination=true&stockCode=
# &csrcCode=&areaName=&stockType=1&pageHelp.cacheSize=1&pageHelp
# .beginPage=3&pageHelp.pageSize=25&pageHelp.pageNo=3&pageHelp.endPage=31&_=1558626613345

sz_url = 'http://www.szse.cn/market/stock/list/index.html'
# http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&
# CATALOGID=1110&TABKEY=tab1&PAGENO=2&random=0.642795889378557
async def get_stock_code(url, q):
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url=url, headers=headers) as resp:
            resp = await resp.read()
            resp = html.fromstring(resp)
            stock_code_lst = resp.xpath('//*[@id="quotesearch"]/ul[1]/li/a/text()')
            for _ in stock_code_lst:
                code = re.search('\((.+)\)', _).group(1)
                async with sess.get(url=bd_url%(q, code), headers=headers) as _resp:
                    _resp = await _resp.read()
                    print(q,code, _resp)


def run():
    for url, area in urls:
        task = asyncio.ensure_future(get_stock_code(url, area))
        tasks.append(task)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run()
    loop.run_until_complete(asyncio.wait(tasks))

