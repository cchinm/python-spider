from lxml.html import fromstring
from lxml.html import HtmlComment
import re
import cchardet
import traceback

REGEXES = {
    'positiveRe': re.compile(
        ('article|arti|body|content|entry|hentry|main|page|'
         'artical|zoom|context|message|editor|'
         'pagination|post|txt|text|blog|story'), re.I),
    'negativeRe': re.compile(
        ('copyright|combx|comment|com-|contact|foot|footer|footnote|decl|copy|'
         'notice|masthead|media|meta|outbrain|promo|related|scroll|link|pagebottom|bottom|'
         'other|shoutbox|sidebar|sponsor|shopping|tags|tool|widget'), re.I),
}


class MainContent:

    def __init__(self):
        # 非文本内容标签
        self.non_content_tag = {
            'head', 'meta', 'script', 'style', 'object',
            'iframe', 'marquee', 'select', 'embed'}

        self.title = ''
        self.p_space = re.compile(r'\s')

        # 文本结尾
        self.p_content_stop = re.compile(r'正文.*结束|正文下|相关阅读|声明')
        self.p_clean_tree = re.compile(r'author|post-add|copyright')


    def get_title(self, doc, xrule=None):
        if xrule is not None:
            title = doc.xpath(xrule)
            return title[0].text_content() if title else None

        title = doc.xpath("//title")
        title = title[0].text_content() if title else None
        if len(title) < 6:
            ti = doc.xpath("//meta[@name=\"title\"]")
            title = ti[0].text_content() if ti else title

        if len(title) < 6:
            ti = doc.xpath('//*[contains(@id, "title")] or //*[contains(@class, "title")]')
            for t in ti:
                if len(t) > title and t in title:
                    title = t
                    break

        return title

    def clean_title(self, title):
        regaxes_clean_title = re.compile(" - |–|—|-|\||::")
        ti = regaxes_clean_title.split(title)
        if len(ti) > 1:
            return ti[0].strip()
        return title

    def calc_node_weight(self, node):
        weight = 1
        attr = '%s %s %s' % (
            node.get('class', ''),
            node.get('id', ''),
            node.get('style', '')
        )
        if attr:
            mm = REGEXES['negativeRe'].findall(attr)
            weight -= 2 * len(mm)
            mm = REGEXES['positiveRe'].findall(attr)
            weight += 4 * len(mm)
        if node.tag in ['div', 'p', 'table']:
            weight += 2
        return weight



    def find_main_content(self, url, text, clean_title = True):

        if isinstance(text, bytes):
            _encode = cchardet.detect(text)['encoding']
            text = text.decode(_encode, "ignore")

        try:
            doc = fromstring(text)
            # 给出html中的绝对链接
            doc.make_links_absolute(base_url=url)

        except:
            traceback.print_exc()
            return None, None

        title = self.get_title(doc=doc)
        body = doc.xpath('//body')

        if clean_title:
            title = self.clean_title(title)

        if not body:
            return title,

        # 采用广度优先进行节点遍历
        nodes = body[0].getchildren()
        while nodes:
            node = nodes.pop(0)
            childrens = node.getchildren()
            tlen = 0

            for child in childrens:
                if isinstance(child, HtmlComment):
                    continue
                # 大多数文本内容已经不在此标签下面
                if child.tag in self.non_content_tag:
                    continue
                elif child.tag == 'a':
                    continue
                elif child.tag == 'textarea':
                    # FIXME: 对于文本框内容应该不被纳入内容范围
                    continue

                nodes.append(child)
                if child.tag == 'p':
                    weight = 3
                else:
                    weight = 1

                # 标签内容
                textlen = '' if child.text else child.text

                # 标签外文本内容
                taillen = '' if child.tail else child.tail
                tlen += (len(textlen) + len(taillen)) * weight

            if tlen < 10:
                continue

            weight = self.calc_node_weight(node)










if __name__ == '__main__':
    from lxml.html import tostring
    p = MainContent()
    t = fromstring("<html><body>TEXT<br>TAIL helloword</html>")
    t = t.getchildren()[0]
    print(t.getchildren())
    # t.tail = "12"
    print(t.tail)
    print(t.text)
    print(tostring(t))