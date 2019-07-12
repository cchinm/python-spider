DOUBAN_WRITE_MSG_URL = "https://www.douban.com/people/%(uid)s/"
DOUBAN_LOGIN_URL = ""

DOUBAN_WRITE_NOTE_URL = "https://www.douban.com/note/%(article_id)s/edit"
DOUBAN_CREATE_NOTE_URL = "https://www.douban.com/note/create" # 获取node_id
DOUBAN_AUTOSAVE_NOTE_URL = "https://www.douban.com/j/note/autosave"
DOUBAN_PUBLISH_NOTE_URL = "https://www.douban.com/j/note/publish"
DOUBAN_PARSE_URL = "https://m.douban.com/rexxar/api/v2/global_tag/parse"


DOUBAN_WRITE_MSG_DATA = {
    'ck':None,
    'pb_text':None,
    'pb_submit':'留言'}

DOUBAN_WRITE_NOTE_DATA = {
    'introduction':'',
    'note_privacy': 'P',
    'cannot_reply':'',
    'author_tags': '情感,社会',
    'accept_donation':'',
    'donation_notice':'',
    'is_original':'', # 原创声明
    'ck': 'tRmd',
    'action': 'new',
    'is_rich': 1,
    'note_id': '',
    'note_title': '',
    'note_text': '',
}

DOUBAN_PARSE_DATA = {
    'text': '',
    'target_type': 'note',
    'count': 40
}


## Xpath Rules
node_id = "//input[@name=\"note_id\"]/@value"