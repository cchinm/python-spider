# -*- coding:UTF-8 -*-
import io
import requests
from fontTools.ttLib import TTFont





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
                base_file = './font/base.woff'
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
                base_file = "./font/base.woff"
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


