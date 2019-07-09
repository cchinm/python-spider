# author: Z.M Z

from crawler import cele

import requests
import lxml.html
from crawler import redis_conn
import time
import traceback
import re

HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
           # "Cookie":'_ga=GA1.2.914577764.1561213321; OUTFOX_SEARCH_USER_ID_NCOO=834227477.8411206; OUTFOX_SEARCH_USER_ID="2076912312@10.168.11.11"; JSESSIONID=aaatO8n_MFD71fbGNnZUw; ___rl__test__cookies=1562080308876',
}



@cele.task
def valid_proxy(host, port, queue, tpe='http'):
    """
    验证ip是否有效，如果有效插入数据库，否则在数据库删除此记录
    :param host:
    :param port:
    :return:
    """
    if port is None:
        http_proxy = host
    else:
        proxy = re.sub("^[^\d]+|[^\d]+$", '', '{}:{}'.format(host, port))
        http_proxy = '{}://{}'.format(tpe, proxy)

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
                redis_conn.add(name=queue,
                               key=http_proxy,
                               value=int(time.time()))
            break
        except:
            print('500 %s' % http_proxy)
        count += 1
    else:
        redis_conn.delete(name=queue, key=http_proxy)


@cele.task
def clean_proxy(queue):
    """
    从数据库加载代理ip数据，进行验证。如果失败则删除此条数据
    :return:
    """
    try:
        ip_set = redis_conn.all(name=queue)
        for proxy in ip_set:
            tpe = proxy[:proxy.find(":")]
            valid_proxy.delay(proxy, None, queue, tpe)
    except:
        traceback.print_exc()

