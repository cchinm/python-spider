#!/usr/bin/env python

import os
import sys
import time
import random
import socket


from http.cookiejar import LWPCookieJar
from urllib.request import Request, urlopen
from urllib.parse import quote_plus, urlparse, parse_qs

from bs4 import BeautifulSoup

# Default use USER-AGENT , unless you change it
USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36')
# Default Request Headers
HEADERS = {
'Accept': 'text/html,application/xhtml+xml,application/xml',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',}

# Define the default cookie file storage path
fold_dir = os.getenv('HOME')
if not fold_dir :
    fold_dir = os.getenv('USERHOME')
    if not fold_dir:
        fold_dir = '.'


# Request the given URL, PARAMS and returns the response page, using the cookie jar
def get_page(url, data=None, user_agent=None, cookie_jar=None,
             timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
             **headers):
    """

    :param url:
    :param data:
    :param user_agent:
    :param cookie_jar:
    :param timeout:
    :param headers:
    :return:
    """

    if user_agent is None:
        user_agent = USER_AGENT

    request = Request(url=url, data=data)
    request.add_header('User-Agent', user_agent)
    if not headers:
        headers = HEADERS
    for k, v in headers.items():
        request.add_header(k, v)

    if cookie_jar:
        cookie_jar.add_cookie_header(request)

    response = urlopen(url=request, timeout=timeout)
    if cookie_jar:
        cookie_jar.extract_cookies(response, request)

    html = response.read()
    response.close()
    try:
        cookie_jar.save()
    except:
        pass
    return html


# Return the standard time format
def standard_timeformat(time_string):
    pass



