'''
仿jQuery查询方式
'''
from com.html.parse.dom import *


class jQuery:

    def __init__(self, dom):
        if isinstance(dom, list):
            self.list = dom
        else:
            self.list = [dom]
        pass

    def __repr__(self):
        return str(self.list)

    def attr(self, name, value=None):
        q = []
        for item in self.list:
            if item.attr(name, value):
                q.append(item)
            for c in item.children:
                tq = jQuery(c).attr(name, value)
                if tq:
                    q.extend(tq.list)
        return jQuery(q)

    def __findAttr(self, an, av, q=[]):
        for item in self.list:
            if item.attr(an) == av:
                q.append(item)
            for c in item.children:
                jQuery(c).__findAttr(an, av, q)
        return q

    def __findTag(self, tn, q=[]):
        for item in self.list:
            if item.tagName == tn:
                q.append(self)
            for c in item.children:
                jQuery(c).__findTag(tn, q)
        return q

    def toHtml(self):
        if len(self.list):
            return self.list[0].toHtml()

    def text(self):
        if len(self.list):
            return self.list[0].getText()

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
        return jQuery(q)


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
