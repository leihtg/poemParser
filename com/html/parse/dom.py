'''
解析DOM树
'''


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

    def addChild(self, dom):
        self.children.append(dom)

    def setText(self, text):
        self.text += text

    def hasAttr(self, name, value):
        for a in self.attrs:
            if name == a[0] and value == a[1]:
                return True
        return False

    def __find(self, selector=""):
        if "#" == selector[:1]:
            if self.hasAttr('id', selector[1:]):
                return self
            else:
                for c in self.children:
                    dest = c.__find(selector)
                    if dest:
                        return dest
            return None
        return None

    def find(self, selector=""):
        if selector == "":
            return None
        return self.__find(selector)
