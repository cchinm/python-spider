# -*- coding:UTF-8 -*-
import lxml.html
from entertainment.douban import text, publish_data
from entertainment.douban import douban_spider


edit_url = 'https://www.douban.com/j/note/publish'
login_url = "https://accounts.douban.com/j/mobile/login/basic"
comment_url = "https://www.douban.com/people/174682501/"
op_url = ""
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://accounts.douban.com',
    'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie':'DC7FB21E9FE7B35FF|16087fb87c881e565b8ec9il_num=0; __utmv=30149280.19lLQtZNQ"; last_login_way=amd; ap_v=0,6.0; __utma=30149280.1575560614.1540523513.1562746345.1562911263.27; __utmc=30149280; __utmz=30149280.1562911263.27.15.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login_popup; __utmt=1; __utmb=30149280.94.10.1562911263; _pk_ref.100001.2fad=%5B%22%22%2C%22%22%2C1562916715%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2F191560132%2F%22%5D; _pk_id.100001.2fad=49af184cce4fa284.1549958086.6.1562916715.1562745800.; _pk_ses.100001.2fad=*; login_start_time=1562916792612'
}
formdata = {
    'ck':'',
    'name': '31231128@qq.com',
    'password': '****',
    'remember': 'false',
    'ticket':''
}

commentdata = {
    "ck":"xtiu",
    "bp_text":"I'M spider.",
    "bp_submit":"留言",
}

def loginDouban(sess:object) -> object:
    pass


if __name__ == '__main__':
    import requests
    sess = requests.Session()

    # loginDouban(sess)
    # sess.post(url=login_url, data=formdata, headers=headers)
    # req = sess.get(url="https://www.douban.com", headers=headers)
    # note_id = douban_spider.douBanCreateNote(sess)
    # douban_spider.douBanAutoSaveNote(article_id=note_id, text="Lihaile 我的国！\n豆瓣机器人第一次尝试",
    #                                 title="声明文",
    #                                 sess=sess)
    req = douban_spider.douBanPublishNote(article_id=725683984, text="Lihaile 我的国！\n豆瓣机器人第一次尝试",
                                          title="声明文",
                                          sess=sess)
    # print(validreq.status_code, validreq.url)
    # doc = lxml.html.fromstrin
    # req = sess.post(url=comment_url, data=commentdata, headers=headers)
    print(req.url)
    sess.close()
    print(req.status_code)
