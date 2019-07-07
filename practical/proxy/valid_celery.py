# author: Z.M Z

from crawler import cele

import requests
import lxml.html
from crawler import redis_conn
import time
import traceback

HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
           # "Cookie":'_ga=GA1.2.914577764.1561213321; OUTFOX_SEARCH_USER_ID_NCOO=834227477.8411206; OUTFOX_SEARCH_USER_ID="2076912312@10.168.11.11"; JSESSIONID=aaatO8n_MFD71fbGNnZUw; ___rl__test__cookies=1562080308876',
}



def crawl_proxy(rules):
    """
    爬取xicidaili的免费代理IP

    :param rules:
    :return:
    """
    url = rules['url']
    host = rules['host']
    port = rules['port']
    req = requests.get(url, headers=HEADERS)
    resp = lxml.html.fromstring(req.text)
    host_text = resp.xpath(host)
    port_text = resp.xpath(port)
    for i in range(len(host_text)):
        valid_proxy.delay(host_text[i], port_text[i])


@cele.task
def common_crawl():
    """
    将爬取操作封装成celery的任务进行调用，使用定时操作。可以启动此任务
    :return:
    """
    for i in range(1, 3):
        rules = {
            'url': 'https://www.xicidaili.com/wt/%d' % i,
            'host': '//*[@id="ip_list"]//tr/td[2]/text()',
            'port': '//*[@id="ip_list"]//tr/td[3]/text()'
        }
        crawl_proxy(rules)

@cele.task
def valid_proxy(host, port):
    """
    验证ip是否有效，如果有效插入数据库，否则在数据库删除此记录
    :param host:
    :param port:
    :return:
    """
    http_proxy = 'http://{}:{}'.format(host, port)
    count = 1
    while count <= 3:
        try:
            timeout = 3 * count
            req = requests.get(url="http://120.79.19.42/post/celery",
                               headers=HEADERS,
                               proxies={'http':http_proxy},
                               timeout=timeout)
            print(req.status_code, http_proxy)
            if req.status_code == 200:
                redis_conn.add(name="http_proxy",
                               key='{}:{}'.format(host, port),
                               value=int(time.time()))
            break
        except:
            print('500', http_proxy)
        count += 1
    else:
        redis_conn.delete(name="http_proxy", key='{}:{}'.format(host, port))


@cele.task
def clean_proxy():
    """
    从数据库加载代理ip数据，进行验证。如果失败则删除此条数据
    :return:
    """
    try:
        ip_set = redis_conn.all(name="http_proxy")[1]
        for http_proxy, score in ip_set:
            host, port = http_proxy.decode("utf8").split(":")
            valid_proxy.delay(host, port)
    except:
        traceback.print_exc()

