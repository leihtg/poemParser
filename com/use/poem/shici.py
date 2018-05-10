# -*- coding: utf-8 -*-
# 解析诗词页面

from com.html.parse import HtmlDomParser as HtmlParser
import redis
import time as t

r = redis.Redis(host="localhost", port=6379, db=0)


# 查询指定作者的诗词
def queryPoems(url, count=0):
    ps = HtmlParser(url)
    ps.parse()
    dom = ps.getDom()
    pages = dom.find('.pages')
    cp = pages.find('span').children[0]
    print("====第[%s]页===" % cp.text)
    print("poem url: %s" % url)
    txea = dom.find('.main3').find('.left').find('textarea')
    for t in txea.children:
        count += 1
        print(count, t.text)
    np = pages.find('a').children
    if np:
        na = np.pop()
        if "下一页" == na.text:
            # queryPoems(ps.getRealUrl(na.attr('href')), count)
            pass

    pass


# 查询所有作者
def queryAuthors(url, count=0):
    ps = HtmlParser(url)
    ps.parse()
    dom = ps.getDom()
    pages = dom.find('.pages')
    authors = dom.find(".sonspic")
    for a in authors.children:
        count += 1
        k = a.find('b').children[0]
        print(count, k.text)
        # 获取作者诗文链接
        swLink = a.find('.cont').find('a').children.pop().attr('href')
        queryPoems(ps.getRealUrl(swLink))
        # r.lpush("authors",k.text)
    nextPage = pages.find('a').children.pop()
    curPage = pages.find('span').children[0]
    print("=====第[%s]页完=====" % curPage.text)
    if nextPage and "下一页" == nextPage.text:
        _u = ps.getRealUrl(nextPage.attr('href'))
        queryAuthors(_u, count)


if __name__ == "__main__":
    start = t.time()

    # 作者首页
    url = "https://so.gushiwen.org/authors/"
    # url = "https://so.gushiwen.org/authors/Default.aspx?p=102&c="
    # queryAuthors(url)
    queryPoems('https://so.gushiwen.org/authors/authorvsw_b90660e3e492A41.aspx')
    print('cost (s) %f' % (t.time() - start))
