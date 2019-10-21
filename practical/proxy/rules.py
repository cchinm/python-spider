# author: Z.M Z

# QueueName

HTTP_PROXY = 'http_proxy'
HTTPS_PROXY = 'https_proxy'
SOCKS_PROXY = 'socks_proxy'


RULES = [
    {
        'urls':['http://www.atomintersoft.com/high_anonymity_elite_proxy_list',
                'http://www.atomintersoft.com/anonymous_proxy_list'],
        'name':'atomintersoft.com',
        'parse_rules':{
            'method':'xpath',
            'host':'//table//tr/td[1]/text()[1]',
            'port':'//noexist',
        },
        'queue':HTTP_PROXY,
        'type':'http'
    },
    {
        'urls':['https://www.xicidaili.com/wt/',],
        'name':'xicidaili.com',
        'parse_rules':{
            'method':'xpath',
            'host':'//*[@id="ip_list"]//tr/td[2]/text()',
            'port':'//*[@id="ip_list"]//tr/td[3]/text()',
        },
        'queue':HTTP_PROXY,
        'type':'http',
    },
    {
        'urls':['https://www.xicidaili.com/wn/',],
        'name':'xicidaili.com',
        'parse_rules':{
            'method':'xpath',
            'host':'//*[@id="ip_list"]//tr/td[2]/text()',
            'port':'//*[@id="ip_list"]//tr/td[3]/text()',
        },
        'queue':HTTPS_PROXY,
        'type':'https'
    },
    {
        'urls':['http://www.89ip.cn/index_%d.html' % i for i in range(1, 10)],
        'name':'89ip.cn',
        'parse_rules':{
            'method':'xpath',
            'host':'//table/tbody/tr/td[1]/text()',
            'port':'//table/tbody/tr/td[2]/text()',
        },
        'queue':HTTP_PROXY,
        'type':'http'
    },
    {
        'urls':['https://ip.ihuan.me/?page=a42g5985d',
                'https://ip.ihuan.me/?page=2d28bd81a',
                'https://ip.ihuan.me/?page=1'],
        'name':'ihuan.me',
        'parse_rules':{
            'method':'xpath',
            'host':'//table//tr/td[1]/a/text()',
            'port':'//table//tr/td[2]/text()',
        },
        'queue':HTTP_PROXY,
        'type':'http'
    },
    {
        'urls':['http://www.data5u.com/',],
        'name':'data5u.com',
        'parse_rules':{
            'method':'xpath',
            'host':'//ul/li[2]/ul[position()>1]/span[1]/li/text()',
            'port':'//ul/li[2]/ul[position()>1]/span[2]/li/text()',
        },
        'queue':HTTP_PROXY,
        'type':'http'
    },
]


