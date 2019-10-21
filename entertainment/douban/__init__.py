

from urllib import parse
import json


text = {
    "blocks": [
        {
            "key": "524un",
            "text": "第二篇日记",
            "type": "unstyled",
            "depth": 0,
            "inlineStyleRanges": [],
            "entityRanges": [],
            "data": {}
        },
        {
            "key": "5fca4",
            "text": "",
            "type": "unstyled",
            "depth": 0,
            "inlineStyleRanges": [],
            "entityRanges": [],
            "data": {}
        },
        {
            "key": "5rqup",
            "text": " ",
            "type": "atomic",
            "depth": 0,
            "inlineStyleRanges": [],
            "entityRanges": [
                {
                    "offset": 0,
                    "length": 1,
                    "key": 0
                }
            ],
            "data": {}
        },
        {
            "key": "83lje",
            "text": "",
            "type": "unstyled",
            "depth": 0,
            "inlineStyleRanges": [],
            "entityRanges": [],
            "data": {}
        },
        {
            "key": "1gidq",
            "text": "",
            "type": "unstyled",
            "depth": 0,
            "inlineStyleRanges": [],
            "entityRanges": [],
            "data": {}
        }
    ],
    "entityMap": {
        "0": {
            "type": "IMAGE",
            "mutability": "IMMUTABLE",
            "data": {
                "width": 600,
                "thumb": "https://img1.doubanio.com/view/note/small/9q4wbRdMkZnTR1zsvlXkHw/191560132/x62984208.jpg",
                "seq": 2,
                "file_size": 53181,
                "url": "https://img1.doubanio.com/view/note/l/H6YSTRf5_0rSL5QJIg-Njw/191560132/x62984208.jpg",
                "file_name": "O19_[2~Z~KVY`8UJ$WLNUFA.png",
                "is_animated": "false",
                "id": "62984208",
                "height": 384,
                "entityKey": "2",
                "src": "https://img1.doubanio.com/view/note/l/H6YSTRf5_0rSL5QJIg-Njw/191560132/x62984208.jpg"
            }
        }
    }
}
publish_data = {
        'introduction':'',
        'note_privacy': 'P',
        'cannot_reply':'',
        'author_tags': '写作,情感,机器人,怕2展示端发斯蒂芬',
        'accept_donation':'',
        'donation_notice':'',
        'is_original':'',
        'ck': 'tRmd',
        'action': 'edit',
        'is_rich': 1,
        'note_id': 725684904,
        'note_title': '你好,SPIDER',
        'note_text': json.dumps(text),}