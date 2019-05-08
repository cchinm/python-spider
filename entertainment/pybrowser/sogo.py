#! /usr/bin/env/python

# import os
# import sys
# dir = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
# sys.path.append(dir)
# import pybrowser


from entertainment import pybrowser
from entertainment.pybrowser import *
from urllib.error import URLError

# Default sogo selector


def RetryRequest(func):
    def wrapper(*args, **kwargs):
        retry_count = 3
        while retry_count > 0:
            try:
                return func(*args, **kwargs)
            except URLError:
                time.sleep(2.0)
        else:
            raise URLError("<urlopen error [WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。>")
    return wrapper

class SogoEngine(object):

    def __init__(self):
        self.default_sogo_headers = None
        self.url_home = "https://%(tpe)s.sogou.com/%(tpe)s?query=%(query)s&type=2&ie=utf8"
        self.url_next_page = "https://%(tpe)s.sogou.com/%(tpe)s?query=%(query)s&type=2&ie=utf8&page=%(page)s"
        self._cookie_jar = None
        self._cookie = None
        self.selectorLinks = 'div.txt-box > h3 > a'
        self.selectorTimestring = 'span.s2'

    # Return a Generator that yield URLs/SelectorOBJs, using the given query string.
    def search(self, query, pause=5.0, user_agent=None, tpe='', num=10, start=0,
               end=10, tbs='', only_current_page=False, allow_domains=None, deny_domains=None,
               selector_links=None, attrs=None):
        """

        :param str query: Query String. Must not be URLencode
        :param float pause: A Lapse to wait between HTTP Request.
            A long Lapse can cause the search slow. A short Lapse will make the Sogo to block
            your IPs.
        :param str user_agent: Use the Default USER-AGENT for None.
        :param str tpe: Search Type (i.e web, weixin, news, videos, zhihu, pics->images ...)
        :param int num: Number of result per page
        :param int start: Offset of the first result to retrieve
        :param int/None end: Last of result to retrieve.
            Keep searching forever if None
        :param str tbs: Time limits
            (i.e d:1 last 1 day, d:2 last 2 days,
                m:1 last 1 month, y:1 last 1 year,
                '' No Time Limit)
        :param bool only_current_page: Use True to prove searching in this page /
            and Not Request next page.
        :param tuple allow_domains: Allow domains.
        :param tuple deny_domains: Deny domains.
        :return: A generator that yields URLs.
        """

        # Count the num of yields links
        count = 0

        # Using Default selector , unless you change it.
        selector_links = selector_links or self.selectorLinks

        # url-encode given query string
        query = pybrowser.quote_plus(query)

        url = self.url_home % {'query':query, 'tpe':tpe}

        soup = self._parse_page(url=url, user_agent=user_agent)
        links = soup.select(selector_links)
        for link in links:
            count += 1
            if attrs:
                yield link[attrs]
            else:
                yield link


        while not only_current_page:

            # Set a lapse to wait.
            time.sleep(pause)
            url = self.url_next_page % {'query':query, 'tpe':tpe, 'page':11}

            soup = self._parse_page(url=url, user_agent=user_agent)
            links = soup.select(selector_links)


            # If no Links, break this loop.
            if len(links) == 0:break

            for link in links:
                count += 1
                if attrs:
                    yield link[attrs]
                else:
                    yield link

    # save cookie in the local file
    def build_cookie(self, *args, **kwargs):
        self._cookie_jar = LWPCookieJar(os.path.join(fold_dir, '.sogo-cookie'))
        try:
            self._cookie_jar.load()
        except Exception:
            pass


    # Add your cookies. -> ((name, value, name1, val1, name2, val2))
    def add_cookie(self,*args):
        if len(args) > 1:
            cookie = map(lambda x:"{}={}".format(x[0], x[1]), args)
            cookies = "; ".join(cookie)
        else:
            cookies = args[0]
        self._cookie = cookies





    # Request using the given URL and returns the Selector Object.
    @RetryRequest
    def _parse_page(self, url, user_agent=None, pause=2.0):
        print(self._cookie_jar, 'cookie_jar')
        if not self._cookie_jar:
            print('Fail')
        response = pybrowser.get_page(url=url,
                                      user_agent=user_agent,
                                      cookie_jar=self._cookie_jar,
                                      Cookie=self._cookie or 'SUV=00000000000000000000000000000000;')
        soup = pybrowser.BeautifulSoup(response)
        print(soup)
        return soup



