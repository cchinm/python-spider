from entertainment.douban.settings import *
import lxml.html
import json
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://accounts.douban.com',
    'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie':'bid=7YU41WKOe3s; douban-fav-remind=1; ll="118281"; _ga=GA1.2.1575560614.1540523513; _vwo_uuid_v2=D05CCAFCD68BE1C9DC7FB21E9FE7B35FF|16087fb87c881e565b8ec9699b6b6424; douban-profile-remind=1; push_noty_num=0; push_doumail_num=0; __utmv=30149280.19156; ct=y; dbcl2="191560132:YvqJlLQtZNQ"; last_login_way=account; ck=tRmd; ap_v=0,6.0; __utma=30149280.1575560614.1540523513.1562746345.1562911263.27; __utmc=30149280; __utmz=30149280.1562911263.27.15.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login_popup; __utmt=1; __utmb=30149280.94.10.1562911263; _pk_ref.100001.2fad=%5B%22%22%2C%22%22%2C1562916715%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2F191560132%2F%22%5D; _pk_id.100001.2fad=49af184cce4fa284.1549958086.6.1562916715.1562745800.; _pk_ses.100001.2fad=*; login_start_time=1562916792612'
}
textt = {"blocks":[{"key":"10pp6","text":"asdf ","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{}}

def douBanWriteMsg(uid, text, ck, sess):
    """
    写留言
    :param uid:
    :param text:
    :param ck:
    :param sess:
    :return:
    """
    print(sess.cookies.get_dict())
    url = DOUBAN_WRITE_MSG_URL % vars()
    formdata = DOUBAN_WRITE_MSG_DATA
    formdata['ck'] = ck
    formdata['pb_text'] = text
    req = sess.post(url=url, data=formdata, headers=headers)
    return req

def douBanPublishNote(article_id, text, title, sess):
    print(sess.cookies.get_dict())
    url = DOUBAN_PUBLISH_NOTE_URL
    formdata = DOUBAN_WRITE_NOTE_DATA
    formdata['note_id'] = int(article_id)
    formdata['note_text'] = json.dumps(textt)
    formdata['note_title'] = title
    douBanParse(sess)
    req = sess.post(url=url, data=formdata, headers=headers)
    print(formdata, req.cookies.get_dict())
    return req

def douBanAutoSaveNote(article_id, text, title, sess):
    print(sess.cookies.get_dict())
    url = DOUBAN_AUTOSAVE_NOTE_URL
    formdata = DOUBAN_WRITE_NOTE_DATA
    formdata['note_id'] = int(article_id)
    formdata['note_text'] = json.dumps(text)
    formdata['note_title'] = title
    req = sess.post(url=url, data=formdata, headers=headers)
    print(formdata)
    return req


def douBanCreateNote(sess):
    print(sess.cookies.get_dict())
    url = DOUBAN_CREATE_NOTE_URL
    req = sess.get(url, headers=headers)
    if 'login' in req.url:
        print('running login function!')
        douBanLogin(sess)
    print(req.url)
    resp = lxml.html.fromstring(req.content)
    print(resp.text)
    note_id = resp.xpath(node_id)
    print(note_id)
    return note_id.pop(0) if note_id else None



def douBanLogin(sess):
    print(sess.cookies.get_dict())
    login_url = "https://accounts.douban.com/j/mobile/login/basic"
    formdata = {
        'ck':'tRmd',
        'name': '3125243748@qq.com',
        'password': 'iimedia',
        'remember': 'false',
        'ticket':''
    }
    req = sess.post(url=login_url, data=formdata, headers=headers)
    print(req.url, '---> url')
    return req


def douBanParse(sess):
    url = DOUBAN_PARSE_URL
    formdata = DOUBAN_PARSE_DATA
    req = sess.post(url=url, data=formdata, headers=headers)
    return req