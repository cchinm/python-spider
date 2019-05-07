#! /usr/bin/env/python

# import os
# import sys
# dir = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
# sys.path.append(dir)
# import pybrowser


from entertainment import pybrowser


# Default sogo selector



class SogoEngine(object):

    def __init__(self):
        self.default_sogo_headers = None
        self.url_home = "https://%(tpe)s.sogou.com/%(tpe)s?query=%(query)s&type=2&ie=utf8"
        self.selectorLinks = 'div.txt-box > h3 > a'
        self.selectorTimestring = 'span.s2'

    # Return a Generator that yield URLs, using the given query string.
    def search(self, query, pause=2.0, user_agent=None, tpe='', num=10, start=0,
               end=None, tbs='', only_current_page=False, allow_domains=None, deny_domains=None,
               selector_links=None):
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
        :return: A generator that yields URLs.
        """

        # url-encode given query string
        query = pybrowser.quote_plus(query)

        url = self.url_home % {'query':query, 'tpe':tpe}
        print(url)
        response = pybrowser.get_page(url=url,
                                      user_agent=user_agent,
                                      Cookie='SUV=00000000000000000000000000000000;')
        soup = pybrowser.BeautifulSoup(response)
        links = soup.select(selector_links)
        for link in links:
            yield link

if __name__ == '__main__':
    p =SogoEngine()
    for i in p.search(query='it may', tpe='zhihu', selector_links='div.result-about-list > h4 > a'):
        print(i)

