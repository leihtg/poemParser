import re
from enum import Enum, unique

'''
解析DOM树
'''


# selectorType = Enum("ID", "TAG", "CLASS", "ATTR")


@unique
class StorType(Enum):
    ID = 0
    TAG = 1
    CLASS = 3
    ATTR = 4


class Dom:
    def __init__(self, tagName="text", attrs=()):
        self.children = []
        self.attrs = attrs
        self.tagName = tagName
        self.text = ""

    def __str__(self):
        return "tagName[%s],attrs:%s" % (self.tagName, self.attrs)

    def setAttrs(self, attrs):
        self.attrs = attrs

    def setChildren(self, cs):
        self.children = cs

    def addChild(self, dom):
        self.children.append(dom)

    def setText(self, text):
        self.text += text

    def attr(self, name):
        for a in self.attrs:
            if a[0] == name:
                return a[1]

    def hasAttr(self, name, value):
        for a in self.attrs:
            if name == a[0] and value == a[1]:
                return True
        return False

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
        dom = Dom()
        q = dom.children
        ret = quickSpeci(selector)
        if ret:
            t, v = ret[0], ret[1]
            if t == StorType.ID:
                self.__findAttr('id', v, q)
            elif t == StorType.TAG:
                self.__findTag(v, q)
            elif t == StorType.CLASS:
                self.__findAttr('class', v, q)
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


if __name__ == "__main__":
    a = rquickExpr.match("#id")
    print(a.group(1), a)
    a = rquickExpr.match("tag")
    print(a.group(1), a)
    a = rquickExpr.match(".class")
    print(a.group(3), a)
    print(type(a))
    print(StorType.ATTR)
