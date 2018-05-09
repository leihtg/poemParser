# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from com.html.parse.dom import *
from urllib import parse as ps
import urllib.request as req

"""
解析DOM标签
"""


# 解析主类
class HtmlDomParser(HTMLParser):
    st = False

    def __init__(self, url=""):
        HTMLParser.__init__(self)
        self.url = url
        self.curDom = self.rootDom = Dom()
        self.domQueue = []
        self.data = ""

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
        if self.data == "":
            self.data = req.urlopen(self.url).read().decode("utf-8")
        self.feed(self.data)

    # Overridable -- finish processing of start+end tag: <tag.../>
    def handle_startendtag(self, tag, attrs):
        self.curDom.addChild(Dom(tag, attrs))
        pass

    # Overridable -- handle start tag
    def handle_starttag(self, tag, attrs):
        self.st = True
        self.domQueue.append(self.curDom)
        dom = Dom(tag, attrs)
        self.curDom.addChild(dom)
        self.curDom = dom
        pass

    # Overridable -- handle end tag
    def handle_endtag(self, tag):
        self.st = False
        self.curDom = self.domQueue.pop()
        pass

    # Overridable -- handle character reference
    def handle_charref(self, name):
        pass

    # Overridable -- handle entity reference
    def handle_entityref(self, name):
        pass

    # Overridable -- handle data
    def handle_data(self, data):
        if self.st:
            self.curDom.setText(data)
        pass

    # Overridable -- handle comment
    def handle_comment(self, data):
        pass

    # Overridable -- handle declaration
    def handle_decl(self, decl):
        pass

    # Overridable -- handle processing instruction
    def handle_pi(self, data):
        pass

    def getDom(self):
        return self.rootDom
