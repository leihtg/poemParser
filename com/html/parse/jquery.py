'''
仿jQuery查询方式
'''
from com.html.parse.dom import *


class jQuery:
    _dom = 0

    def __init__(self, dom):
        self.list = [dom]
        self.dom = dom
        pass

    # 获取标签内容
    def getText(self):
        txt = self.dom.text
        for c in self.dom.children:
            if c.tagName == 'text':
                txt += c.text
            else:
                txt += c.getText()
        return txt

    def toHtml(self):
        _dom = self.dom
        if (_dom.tagName == 'text'):
            return _dom.getText()
        txt = '<%s' % _dom.tagName
        for attr in _dom.attrs:
            txt += ' %s="%s"' % (attr[0], attr[1])
        txt += '>'
        for c in _dom.children:
            txt += c.toHtml()
        txt += '</%s>' % _dom.tagName
        return txt

    def attr(self, name):
        _dom=self.dom
        for a in _dom.attrs:
            if a[0] == name:
                return a[1]

    def __findAttr(self, an, av, q=[]):
        if self.hasAttr(an, av):
            q.append(self)
        else:
            for c in self.children:
                c.__findAttr(an, av, q)
        return q

    def __findTag(self, tn, q=[]):
        if self.tagName == tn:
            q.append(self)
        else:
            for c in self.children:
                c.__findTag(tn, q)
        return q

    def find(self, selector=""):
        q = []
        ret = quickSpeci(selector)
        if ret:
            t, v = ret[0], ret[1]
            if t == StorType.ID:
                self.__findAttr('id', v, q)
            elif t == StorType.TAG:
                self.__findTag(v, q)
            elif t == StorType.CLASS:
                self.__findAttr('class', v, q)
        if len(q) > 0:
            dom = q.pop(0)
            # dom.children = q
        else:
            dom = Dom()
        return dom
    # id , tag or class


rquickExpr = re.compile(r'^#([\w-]+)|(\w+)|\.([\w-]+)$')


def quickSpeci(selector):
    ret = rquickExpr.match(selector)
    if ret.group(1):
        return (StorType.ID, ret.group(1))
    elif ret.group(2):
        return (StorType.TAG, ret.group(2))
    elif ret.group(3):
        return (StorType.CLASS, ret.group(3))
    return None
