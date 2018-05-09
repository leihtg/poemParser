# -*- coding: utf-8 -*-

from com.html.parse import *
import time as t


def scan(dom, indent=""):
    print(indent, dom)
    for c in dom.children:
        indent += "--"
        scan(c, indent)
    pass


url = 'https://so.gushiwen.org/authors/authorvsw_3b99a16ff2ddA01.aspx'
url = 'https://so.gushiwen.org/authors/'
# data = open(r'C:\Users\Thinkpad\Desktop\a.txt', encoding="utf-8").read()
start = t.time()
a = HtmlDomParser(url)
a.parse()
print("parser cost(s) %f" % (t.time() - start))

start = t.time()

rd = a.getDom()
# f = rd.find('#txtare71144')
# f = rd.find('.sonspic')
# scan(f)
# f = rd.find('.pages')
f=rd.find('span')
scan(f)

print("find dom cost(s) %f" % (t.time() - start))
