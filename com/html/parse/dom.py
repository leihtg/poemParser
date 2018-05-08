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

    def attr(self, name):
        for a in self.attrs:
            if a[0] == name:
                return a[1]

    def hasAttr(self, name, value):
        for a in self.attrs:
            if name == a[0] and value == a[1]:
                return True
        return False

    def __find(self, an, av, q=[]):
        if self.hasAttr(an, av):
            q.append(self)
        else:
            for c in self.children:
                c.__find(an, av, q)
        return q

    def find(self, selector=""):
        q = []
        if selector == "":
            return q
        if "#" == selector[:1]:
            return self.__find('id', selector[1:], q)
        elif "." == selector[:1]:
            return self.__find('class', selector[1:], q)

        return q
