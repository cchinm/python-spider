# author: Z.M Z

import requests
from requests.exceptions import ProxyError
import lxml.html
import json
import jsonpath

import valid_celery
import time
# from crawler import redis_conn
import random, traceback
from rules import RULES, HTTP_PROXY, HTTPS_PROXY, SOCKS_PROXY

HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
           # "Cookie":'_ga=GA1.2.914577764.1561213321; OUTFOX_SEARCH_USER_ID_NCOO=834227477.8411206; OUTFOX_SEARCH_USER_ID="2076912312@10.168.11.11"; JSESSIONID=aaatO8n_MFD71fbGNnZUw; ___rl__test__cookies=1562080308876',
}

def get_random_ip():
    req = requests.get('http://127.0.0.1:8000/api?sign=t').json()
    return random.choice(req)

def crawl_proxy(rules):
    global ip_random
    urls = rules['urls']
    rule = rules['parse_rules']
    queue = rules['queue']
    tpe = rules['type']
    print(rules)


    for url in urls:
        count = 0
        while count < 3:
            try:
                req = requests.get(url, headers=HEADERS, proxies=ip_random, timeout=10)
                print(req.status_code, ip_random)
                if rule['method'] == 'xpath':
                    resp = lxml.html.fromstring(req.text)
                    host_text = resp.xpath(rule['host'])
                    port_text = resp.xpath(rule['port']) or []
                elif rule['method'] == 'json':
                    resp = json.loads(req.text, encoding="utf8")
                    host_text = jsonpath.jsonpath(resp, rule['host'])
                    port_text = jsonpath.jsonpath(resp, rule['port']) or []
                else:
                    host_text = []
                    port_text = []

                while host_text and port_text:
                    host = host_text.pop().strip()
                    port = port_text.pop().strip()
                    print("%s:%s" % (host, port))

                    valid_celery.valid_proxy.delay(host, port, queue, tpe)

                while host_text:
                    host = host_text.pop().strip()
                    print(host)
                    valid_celery.valid_proxy.delay(host, '', queue, tpe)
                break
            except ProxyError:
                count += 1
                if count == 2:
                    ip_random = None
                else:
                    ip_random = {"http":get_random_ip()}


            except:
                traceback.print_exc()
                count += 1
                if count == 2:
                    ip_random = None
                else:
                    ip_random = {"http":get_random_ip()}


def clean_proxy():
    # valid_celery.clean_proxy.delay()
    return


if __name__ == '__main__':
    count = 0
    try:
        # ip_sets = redis_conn.all("http_proxy")
        valid_celery.clean_proxy.delay(HTTPS_PROXY)
        valid_celery.clean_proxy.delay(HTTP_PROXY)
        valid_celery.clean_proxy.delay(SOCKS_PROXY)
        ip_random = {"http":get_random_ip()}
    except Exception as e:
        print(e)
        ip_random = None

    while True:
        if ip_random is None:
            try:
                ip_random = {"http":get_random_ip()}
            except:
                ip_random = None

        if count == 2:
            valid_celery.clean_proxy.delay(HTTPS_PROXY)
            valid_celery.clean_proxy.delay(HTTP_PROXY)
            valid_celery.clean_proxy.delay(SOCKS_PROXY)

        for i in RULES:
            crawl_proxy(i)
        time.sleep(300)
        count += 1
        if count == 3:
            count = 0



