# author: Z.M Z

import requests
import lxml.html
import valid_celery
import time
from crawler import redis_conn
import random, traceback
from rules import RULES

HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
           # "Cookie":'_ga=GA1.2.914577764.1561213321; OUTFOX_SEARCH_USER_ID_NCOO=834227477.8411206; OUTFOX_SEARCH_USER_ID="2076912312@10.168.11.11"; JSESSIONID=aaatO8n_MFD71fbGNnZUw; ___rl__test__cookies=1562080308876',
}


def crawl_proxy(rules):
    url = rules['url']
    host = rules['host']
    port = rules['port']
    try:
        ip_sets = redis_conn.all("http_proxy")[1]
        ip_random = {"http":"http://%s" % random.choice(ip_sets)[0].decode("utf8")}
    except Exception as e:
        print(e)
        ip_random = None

    try:
        req = requests.get(url, headers=HEADERS, proxies=ip_random)
        print(req.status_code, ip_random)
        resp = lxml.html.fromstring(req.text)
        host_text = resp.xpath(host)
        port_text = resp.xpath(port)
        print(host_text)
        print(port_text)
        for i in range(len(host_text)):
            valid_celery.valid_proxy.delay(host_text[i], port_text[i])
    except:
        traceback.print_exc()


def clean_proxy():
    valid_celery.clean_proxy.delay()


if __name__ == '__main__':
    count = 0
    while True:
        for i in RULES:
            crawl_proxy(i)
        time.sleep(300)
        count += 1
        if count == 3:
            count = 0
            valid_celery.clean_proxy.delay()



