# -*- coding: utf-8 -*-

from com.html.parse import *

a = HtmlDomParser("https://so.gushiwen.org/authors/authorvsw_3b99a16ff2ddA01.aspx")
a.parse()
rd = a.getDom()
print(rd.tagName)
for i in rd.children:
    print("===%s" % i.tagName)
    for ii in i.children:
        print(ii.tagName, ii.children)

