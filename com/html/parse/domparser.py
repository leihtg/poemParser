# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from com.html.parse.dom import *
from urllib import parse as ps
import urllib.request as req

"""
解析DOM标签
"""
debug = None


# 解析主类
class HtmlDomParser(HTMLParser):

    def __init__(self, url=""):
        print('parse:', url)
        HTMLParser.__init__(self)
        self.url = req.quote(url,'/:&?_')
        self.curDom = self.rootDom = Dom()
        self.domQueue = []
        self.data = ""
        self.st = False

    def setUrl(self, url):
        self.url = url

    def getRealUrl(self, urlSuffix=""):
        if urlSuffix == "":
            return self.url
        elif "http" == urlSuffix[:4]:
            return urlSuffix
        hurl = ps.urlparse(self.url)
        _url = "%s://%s" % (hurl.scheme, hurl.hostname)
        if hurl.port:
            _url += ":" + str(hurl.port)
        if "/" == urlSuffix[:1]:
            _url += urlSuffix
        else:
            _url += hurl.path[:hurl.path.rindex('/') + 1] + urlSuffix
        return _url

    def setData(self, data=""):
        self.data = data

    def parse(self):
        try:
            if self.data == "":
                resp = req.urlopen(self.url)
                encode = 'iso-8859-1'
                for h in resp.headers._headers:
                    if h[0] == 'Content-Type':
                        for val in h[1].split(';'):
                            if val.find('charset=') > 0:
                                encode = val.split('charset=')[1]
                                break
                    pass
                self.data = resp.read().decode(encode)
            self.feed(self.data)
            if len(self.domQueue):
                self.rootDom.addChild(self.domQueue.pop())
        except req.HTTPError as args:
            print('error:[%s],url:[%s]' % (args, self.url))
        return self.rootDom

    # Overridable -- finish processing of start+end tag: <tag.../>
    def handle_startendtag(self, tag, attrs):
        if debug:
            print("start_end: %s" % tag)
        self.curDom.addChild(Dom(tag, attrs))
        pass

    # Overridable -- handle start tag
    def handle_starttag(self, tag, attrs):
        if debug:
            print("start: %s" % tag)
        self.st = True
        dom = Dom(tag, attrs)
        self.curDom.addChild(dom)
        if tag == "html":
            self.rootDom = dom
        else:
            dom.parent = self.curDom

        # 对于不存在内容的元素如br、img等
        if oneTag(tag):
            pass
        else:
            self.domQueue.append(self.curDom)
            self.curDom = dom
            if debug:
                print("%-8s" % repr(self.curDom), self.domQueue)
        pass

    # Overridable -- handle end tag
    def handle_endtag(self, tag):
        if debug:
            print("end: %s" % tag)
        self.st = False
        # 一些网页不规范,不该有关闭标签的忽略
        if oneTag(tag) and self.curDom.tagName != tag:
            self.curDom.addChild(Dom(tag))
            return
        elif self.curDom.tagName != tag:  # 没有对应的开始标签
            self.curDom.addChild(Dom(tag))
            return
        try:
            self.curDom = self.domQueue.pop()
            if debug:
                print("%-8s" % repr(self.curDom), self.domQueue)
        except BaseException as a:
            if not debug:
                print(self.data)
            print("tag[%s],no next" % tag)
            raise a

        pass

    # Overridable -- handle character reference
    def handle_charref(self, name):
        if debug:
            print("charref: %s" % name)
        pass

    # Overridable -- handle entity reference
    def handle_entityref(self, name):
        if debug:
            print("entityref: %s" % name)
        pass

    # Overridable -- handle data
    def handle_data(self, data):
        if self.st:
            self.curDom.addChild(Dom("text", text=data))
        pass

    # Overridable -- handle comment
    def handle_comment(self, data):
        pass

    # Overridable -- handle declaration
    def handle_decl(self, decl):
        pass

    # Overridable -- handle processing instruction
    def handle_pi(self, data):
        if debug:
            print("pi: %s" % data)
        pass

    def getDom(self):
        return self.rootDom


onlyOneTag = ("br", "hr", "img", "link", "meta", "input")


def oneTag(tag):
    return tag in onlyOneTag


if __name__ == "__main__":
    debug = False
    path = r"C:\Users\leihuating\Desktop\a"
    path = r"C:\Users\Thinkpad\Desktop\a.txt"
    ps = HtmlDomParser()
    ps.setData(open(path, encoding="utf-8").read())
    dom = ps.parse()
    print(dom.find('html').toHtml())
