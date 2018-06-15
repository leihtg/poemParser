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
        self.attrs = attrs
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

    def hasAttr(self, name, value):
        _dom=self
        for a in _dom.attrs:
            if name == a[0] and value == a[1]:
                return True
        return False
