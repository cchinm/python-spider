# -*- coding:UTF-8 -*-
import io
import requests
from fontTools.ttLib import TTFont
# pymaoyanfont a tools to parse maoyan's font
#
# init object.
# from pymaoyanfont.parsefont import MaoyanFont
#
# p = MaoyanFont()
#
# # use local woff file, compared with the base woff file.
# file = 'Local WOFF file path'
# result = p.load(file)
# print(result)
# >> > {'uniE631': 6, 'uniE659': 0, 'uniE715': 9, 'uniE923': 7, 'uniF024': 8, 'uniF255': 4, 'uniF467': 3, 'uniF4E8': 2,
#       'uniF533': 5, 'uniF7A7': 1}
#
# # Download online content and compared with base woff files
# from base64 import b64decode
#
# s = 'webpage base64 encoded content'
# s = b64decode(s)
#
# result = p.loads(s)
# print(result)
# >> > {'uniE188': 7, 'uniE7CA': 8, 'uniE7F2': 0, 'uniE8E6': 2, 'uniE8F1': 1, 'uniEB56': 3, 'uniECDF': 5, 'uniED63': 9,
#       'uniF1FA': 4, 'uniF8A6': 6}
#
# # Get the page source code
# p.uni_to_raw()
# >> > {'&#e188;': 7, '&#e7ca;': 8, '&#e7f2;': 0, '&#e8e6;': 2, '&#e8f1;': 1, '&#eb56;': 3, '&#ecdf;': 5, '&#ed63;': 9,
#       '&#f1fa;': 4, '&#f8a6;': 6}
# # Convert character code to decimal
# p.uni_to_int()
# >> > {57736: 7, 59338: 8, 59378: 0, 59622: 2, 59633: 1, 60246: 3, 60639: 5, 60771: 9, 61946: 4, 63654: 6}


import os
_t = os.path.join(os.path.realpath(__file__), '..')
data_dir = os.path.abspath(os.path.join(_t, './data/base.woff'))

class MaoyanFont(object):

    def __init__(self):
        # 基准字体
        self._glyphs_map = None
        self._baseValue = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        self._baseCode = ('uniECF6', 'uniF619', 'uniF624', 'uniF67D', 'uniF6A8',
            'uniF807', 'uniE701', 'uniE9D7', 'uniF836', 'uniE25B')


    @property
    def glyphs(self):
        return self._glyphs_map


    @property
    def basecode(self):
        return self._baseCode

    @property
    def basevalue(self):
        return self._baseValue

    @basecode.setter
    def basecode(self, *args):
        self._baseCode = args

    @basevalue.setter
    def basevalue(self, *args):
        self._baseValue = args

    # Parse the font compared with base font and returns a dict .
    def _parseFont(self, parse_font, base_font):
        """

        :param parse_font:
        :param base_font:
        :return:
        """
        glynames = parse_font.getGlyphNames()[1:-1]

        # Define a dict to store ``code`` and ``value``.
        glyph = {}

        for code in glynames:
            tmp_glyph = parse_font['glyf'][code]

            for i in range(len(self._baseCode)):
                if tmp_glyph == base_font['glyf'][self._baseCode[i]]:
                    # glyph["&#%d;"  % eval("0x"+code[3:])] = baseValue[i]
                    glyph[code] = self._baseValue[i]
                    break
        return glyph


    # input a file dir and return reflect table.
    def load(self, file, base_file=None, base_font=None):
        """

        :param file:
        :param base_file:
        :return:
        """
        parse_font = TTFont(file)
        if base_font is None:
            if base_file is None:
                base_file = data_dir
            base_font = TTFont(base_file)
        self._glyphs_map = self._parseFont(parse_font, base_font)
        return self._glyphs_map

    # input text content and return reflect table.
    def loads(self, s, base_file=None, base_font=None):
        """

        :param s:
        :param base_file:
        :return:
        """
        parse_font = TTFont(io.BytesIO(s))
        if base_font is None:
            if base_file is None:
                base_file = data_dir
            base_font = TTFont(base_file)
        self._glyphs_map = self._parseFont(parse_font, base_font)
        return self._glyphs_map


    # unicode to source-page code.
    def uni_to_raw(self):
        if self._glyphs_map is None:return None

        tmp = {}
        for _ in self._glyphs_map:
            tmp['&#%s;' % _[3:].lower()] = self._glyphs_map[_]
        return tmp

    # unicode to int
    def uni_to_int(self):
        if self._glyphs_map is None:return None

        tmp = {}
        for _ in self._glyphs_map:
            tmp[eval('0x'+_[3:])] = self._glyphs_map[_]
        return tmp


    def __del__(self):
        del self

