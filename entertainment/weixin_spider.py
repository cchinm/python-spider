from urllib.error import URLError, HTTPError
import requests
from urllib import parse
from bs4 import BeautifulSoup
import time

DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
WECHAT_ATICLE_URL = "https://weixin.sogou.com/weixin?" \
                    "type=2&s_from=input&query={query}&ie=utf8&_sug_=y" \
                    "&_sug_type_=&sst0={timestamp}&lkt=0%2C0%2C0"
WECHAT_OFFICIAL_PLARFORM_URL = "https://weixin.sogou.com/weixin?" \
                    "type=1&s_from=input&query={query}&ie=utf8&_sug_=y" \
                    "&_sug_type_=&w=01019900&sut=207796&sst0={timestamp}&lkt=0%2C0%2C0"


class WeixinUrlTypeError(URLError):
    pass

def _get_page(query:str, type:int, page:int=1):
    """

    :param url:
    :param query:
    :param proxies: {'http':'http://xxxxx', 'https':'https://xxxx'}
    :return:
    """
    _quote_query = parse.quote(query)
    _timestamp = int(time.time()*1000)-12
    if type == 2:
        _url = WECHAT_ATICLE_URL.format(query=_quote_query, timestamp=_timestamp)
    elif type == 1:
        _url = WECHAT_OFFICIAL_PLARFORM_URL.format(query=_quote_query, timestamp=_timestamp)
    else:
        raise WeixinUrlTypeError('no such type ``%d``' % type)
    if page > 1:
        _url += "&page=%d" % page
    try:
        print(_url)
        response = requests.get(url=_url, headers={'User-Agent':DEFAULT_USER_AGENT,
                                                   'Refer':'https://weixin.sogou.com/',
                                                   'Cookie': 'SUV=1556978097446544; ABTEST=7|1556978096|v1; weixinIndexVisited=1;'})
        return response
    except URLError as e:
        print(e.reason)


class WeXinOpener(object):
    def __init__(self, proxies:dict=None, headers:dict=None, cookie:dict=None, timeout:int=30):
        self.proxies = proxies
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
                        'q=0.8,application/signed-exchange;v=b3',
                        'Host': 'weixin.sogou.com',}
        if headers :
            self.headers.update(headers)
        else:
            self.headers.update({'User-Agent':DEFAULT_USER_AGENT})
        self.cookie = cookie
        self.timeout = timeout
        self.opener = None
        self._article_list = 'ul.news-list > li > div.txt-box > h3 > a'
        self._official_paltform_list = ''


    def weixin_article_extract(self, query, page=1):
        response = _get_page(query, 2, page)
        soup = BeautifulSoup(response.content.decode("utf-8", "ignore"))
        a = soup.select(self._article_list)
        return soup

    def weixin_official_platform_extract(self, query, page=1):
        response = _get_page(query, 1, page)
        soup = BeautifulSoup(response.content.decode("utf-8", "ignore"))
        a = soup.select('ul.news-list2 > li')

        for i in a:
            _info = i.select('dl > dd')
            for i, k in enumerate(_info):
                print(i, k.text)
        return soup

if __name__ == '__main__':
    p = WeXinOpener()
    p.weixin_official_platform_extract('白丁')
