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
    def __init__(self, tagName="", attrs=(), text=""):
        self.children = []
        self.attrs = list(attrs)
        self.tagName = tagName
        self.text = text
        self.parent = None

    def __str__(self):
        return "tagName[%s],attrs:%s" % (self.tagName, self.attrs)

    def __repr__(self):
        return self.tagName

    def setAttrs(self, attrs):
        self.attrs = attrs

    def setChildren(self, cs):
        self.children = cs

    def addChild(self, dom):
        self.children.append(dom)

    # 去除属性
    def removeAttr(self, name):
        for attr in self.attrs:
            if attr[0] == name:
                self.attrs.remove(attr)
        return self

    def addAttr(self, name, value):
        self.attrs.append((name, value))
        return self

    # 如果传name和value则表示要修改属性
    def attr(self, name, value=None):
        _dom = self
        _find = False
        ret = False
        for a in _dom.attrs:
            if name == a[0]:
                if value:
                    _find = True
                else:
                    ret = a[1]
                    break
        if _find:
            _dom.removeAttr(name).addAttr(name, value)
        elif value:  # 新增属性
            _dom.addAttr(name, value)

        return ret

    def toHtml(self):
        _dom = self
        if (_dom.tagName == 'text'):
            return _dom.getText()
        txt = ''
        for c in _dom.children:
            txt += c.toHtml()

        if _dom.tagName:
            tag = '<%s' % _dom.tagName
            for attr in _dom.attrs:
                tag += ' %s="%s"' % (attr[0], attr[1])
            tag += '>'
            txt = tag + txt + '</%s>' % _dom.tagName
        return txt

    # 获取标签内容
    def getText(self):
        txt = self.text
        for c in self.children:
            if c.tagName == 'text':
                txt += c.text
            else:
                txt += c.getText()
        return txt
