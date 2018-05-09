# -*- coding: utf-8 -*-
# 解析诗词页面

from com.html.parse import HtmlDomParser as HtmlParser
import redis
import time as t

r = redis.Redis(host="localhost", port=6379, db=0)

def queryPage(url, count=0):
    ps = HtmlParser(url)
    ps.parse()
    dom = ps.getDom()
    pages = dom.find('.pages')
    authors = dom.find(".sonspic")
    for a in authors.children:
        count += 1
        k = a.find('b').children[0]
        r.lpush("authors",k.text)
        print(count, k.text)
    nextPage = pages.find('a').children.pop()
    curPage = pages.find('span').children[0]
    print("=====第[%s]页完=====" % curPage.text)
    if nextPage and "下一页" == nextPage.text:
        _u = ps.getRealUrl(nextPage.attr('href'))
        queryPage(_u, count)


if __name__ == "__main__":
    start = t.time()

    # 作者首页
    url = "https://so.gushiwen.org/authors/"
    url="https://so.gushiwen.org/authors/Default.aspx?p=102&c="
    queryPage(url)
    print('cost (s) %f' % (t.time() - start))
