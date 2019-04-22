# 请求参数
# 获取城市数据以及详细数据
# 若参数失效使用chrome开发者工具重新获取
# uri: https://map.baidu.com/
search_param_city = {
    'reqflag': "pcmap",
    'biz': "1",
    'da_par': "direct",
    'pcevaname': "pc4.1",
    'qt': "s",
    'da_src': "searchBox.button",
    'wd': "",
    'c': "131",
    'src': "0",
    'pn': "0",
    'sug': "0",
    'l': "12",
    'b': "(12897798.56,4811331.47;13020678.56,4839363.47)",
    'from': "webmap",
    'biz_forward': "{\"scaler\"1,\"styles\"\"pl\"}",
    'auth': "U1BWfQG71eLGgLaYDRwGGOPB86KDdAyQuxHHHBzxRzHtxjhNwzWWvy1uVtcvY1SGpuBtGIiyRWF=9Q9K=xXw1cv3uVtGccZcuVtPWv3GuBEtdHvtWjat2JKMPS7Y=ceGcEWe1GD8zv7u@ZPuxVxtfvA7uegvcguxHHHBxBBNxtosSSE2b1Bggc1GH",
    'device_ratio': "1",
    'tn': "B_NORMAL_MAP",
    'nn': "0",
    'u_loc': "12623006,2623259",
    'ie': "utf-8",
    't': "1555321873216",
}


data = {'newmap': "1",
        'reqflag': "pcmap",
        'biz': "1",
        'da_par': "direct",
        'pcevaname': "pc4.1",
        'qt': "s",
        'da_src': "searchBox.button",
        'wd': "",
        'c': "131",
        'src': "0",
        'pn': "1",
        'sug': "0",
        'l': "5",
        'b': "(3742035.2200000007,2875227.879999999;19470675.22,6463323.879999999)",
        'from': "webmap",
        'biz_forward': "{\"scaler\"1,\"styles\"\"pl\"}",
        'auth': "a90PN45XaKNLgNGEW5PzRdS5vwyKHgz1uxHHHBVRETLtxjhNwzWWvy1uVt1GgvPUDZYOYIZuVt1cv3uVtGccZcuVtcvY1SGpuLtT@BOKAEYz@1qo6f8oDF2ILOSUY9=CcEWe1GD8zv7u@ZPuztgw4vjlBhlADMMMGZZ5YEzpt66FHcEBggc1H",
        'device_ratio': "1",
        'tn': "B_NORMAL_MAP",
        'nn': "0",
        'u_loc': "12623006,2623259",
        'ie': "utf-8",
        't': "1555308685869",}




uas = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

def headers():
    import random
    _headers = {
        'Referer': 'https://map.baidu.com/@12959238.56,4825347.47,12z',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    _headers['User-Agent'] = random.choice(uas)
    return _headers.copy()