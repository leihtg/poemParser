# -*- coding: utf-8 -*-
# 解析诗词页面

from com.html.parse import HtmlDomParser as HtmlParser
# from com.use.persist.mysql import Mysql
import re
import redis
import time as t

r = redis.Redis(host="localhost", port=6379, db=0)
txtRe = re.compile(r'txtare\d+')


# 查询指定作者的诗词
def queryPoems(url, aId, next=False, count=0):
    ps = HtmlParser(url)
    # ps.setData(open(r"C:\Users\Thinkpad\Desktop\a.txt",encoding="utf-8").read())
    ps.parse()
    dom = ps.getDom()
    pages = dom.find('.pagesright')
    cp = pages.find('#putpage').children[0]
    print("====第[%s]页===" % cp.attr('value'))
    txea = dom.find('.main3').find('.left').find('textarea')
    if not r.zscore("poems", url):  # 没有保存过
        pipe = r.pipeline()
        pipe.multi()
        for t in txea.children:
            if txtRe.match(t.attr('id')):
                count += 1
                print(count)
                pipe.lpush(aId,t.text)
                # trimPoem(count, aId, t.text)
        pipe.execute()
    r.zadd("poems", url, count)  # 添加到保存列表
    nurl = nextPage(pages)
    if nurl:
        queryPoems(ps.getRealUrl(nurl), aId, next, count)
    pass


def nextPage(pages):
    np = pages.find('.amore').children
    if next and np:
        na = np.pop()
        if na.attr('href'):
            return na.attr('href')
    return None


# 查询所有作者
def queryAuthors(url, count=0):
    ps = HtmlParser(url)
    ps.parse()
    dom = ps.getDom()
    pages = dom.find('.pagesright')
    authors = dom.find(".sonspic")
    for a in authors.children:
        count += 1
        k = a.find('b').children[0]
        print(count, k.text)
        # 保存到数据库
        au = {}
        au['id'] = str(count)
        au['name'] = k.text
        saveAuthor(au)
        # 获取作者诗文链接
        swLink = a.find('.cont').find('a').children.pop().attr('href')
        if not r.zadd("authors", swLink, count):
            continue
        queryPoems(ps.getRealUrl(swLink), k.text, True)
        # r.lpush("authors",k.text)
    cp = pages.find('#putpage').children[0]
    print("=====第[%s]页完=====" % cp.attr('value'))
    nurl = nextPage(pages)
    if nurl:
        _u = ps.getRealUrl(nurl)
        queryAuthors(_u, count)


# 提取诗词标题作者朝代等
def trimPoem(id, aId, data=""):
    print(data)
    poem = {}
    pos = data.index("——")
    s = data.index("《", pos)
    e = data.rindex("》")
    poem['author'] = aId
    poem['title'] = data[s + 1:e]
    poem['content'] = data[:pos]
    savePoem(poem)


# mysql = Mysql("172.29.97.155", "root", "root", "springboot", charset="utf8")


def saveAuthor(data):
    sql = "insert Author(id,name) values ('%s','%s')" % (data['id'], data['name'])
    # mysql.exec(sql)
    # r.set(data['id'], data['name'])


def savePoem(data):
    # sql = "insert Poem (id,title,authorId,content) values('%s','%s','%s','%s')" % (
    #     data['id'], data['title'], data['authorId'], data['content'])
    r.lpush("%s" % data['author'], ("%s" % (data)))
    # mysql.exec(sql)


if __name__ == "__main__":
    start = t.time()

    # 作者首页
    url = "https://so.gushiwen.org/authors/"
    url = "https://so.gushiwen.org/authors/Default.aspx?p=10&c=%E4%B8%8D%E9%99%90"
    # url = "https://so.gushiwen.org/authors/Default.aspx?p=102&c="
    queryAuthors(url)
    # queryPoems('https://so.gushiwen.org/authors/authorvsw_6485481407d1A7.aspx',1)
    print('cost (s) %f' % (t.time() - start))
