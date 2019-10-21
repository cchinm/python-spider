import requests
import lxml.html
import cchardet
import re

class Xpath:
    title = '//h3[@class="c-title"]/a'
    abstract = '//div[contains(@class,"summary")]'
    source = '//p[@class="c-author"]'

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
           }

url = "https://www.baidu.com/s?ie=utf-8&cl=2&medium=0&rtt=1&bsst=1&rsv_dl=news_t_sk&tn=news&word=你好&rsv_sug3=13&rsv_sug4=1249&rsv_sug1=7&rsv_sug2=0&inputT=4261"
req = requests.get(url=url, headers=headers)
# print(req.text)
encoding = cchardet.detect(req.content)['encoding']
hcont = lxml.html.fromstring(req.content.decode(encoding=encoding, errors="ignore"))
title = hcont.xpath(Xpath.title)
abstract = hcont.xpath(Xpath.abstract)
source = hcont.xpath(Xpath.source)
print(len(title), len(abstract), len(source))
data = []
for i in range(len(title)):
    ttle = title[i].text_content().strip()
    abst = abstract[i].text_content().strip().split()
    soure = source[i].text_content().strip().split()
    short_summary = []
    print(ttle)
    print(abst)
    print(soure)
    for _ in abstract[i].text_content().strip().split():
        if _ in soure or re.search("^百度快照|^查看更多", _) or len(_) < 2:
            continue
        short_summary.append(_)
    tmp = dict(
        title=title[i].text_content().strip(),
        short_summary=" ".join(short_summary),
        post_author=soure[0],
        post_time=soure[1],
        tags="资讯",
        id=i,
        views="",
        is_priority=0,
        md5_id="#"
    )
    data.append(tmp)

print(data)
import pandas

df = pandas.DataFrame()
df.replace