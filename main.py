# -*- coding: utf-8 -*-

from com.html.parse import *
import time as t

url = 'https://so.gushiwen.org/authors/authorvsw_3b99a16ff2ddA01.aspx'
url = 'https://so.gushiwen.org/authors/'
# data = open(r'C:\Users\Thinkpad\Desktop\a.txt', encoding="utf-8").read()
start = t.time()
a = HtmlDomParser(url)
a.parse()
print("parser cost(s) %f" % (t.time() - start))

start = t.time()
rd = a.getDom()
f=rd.find('#txtare71144')
f=rd.find('.pages')
for e in f:
   print(e,e.text)
   for c in e.children:
      print(c,c.text,c.attr('href'))
print("find dom cost(s) %f" % (t.time() - start))

