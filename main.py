# -*- coding: utf-8 -*-

from com.html.parse import *
import time as t

start = t.time()

p = HtmlDomParser('https://blog.csdn.net/u013055678/article/details/78364774')
dom = p.parse()
jq = jQuery(dom)
print(jq.toHtml())
print("find dom cost(s) %f" % (t.time() - start))
