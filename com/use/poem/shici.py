# -*- coding: utf-8 -*-
# 解析诗词页面


import re
from urllib import request
from html.parser import HTMLParser
import redis


class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies = []
        self.st = False

    def __getUrl(self, num):
        return 'https://so.gushiwen.org/authors/authorvsw_3b99a16ff2ddA' + ('%0d' % num) + '.aspx'

    def getHtml(self, num):
        self.movies = []
        return request.urlopen(self.__getUrl(num)).read().decode('utf-8')

    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname, reg):
            for each in attrlist:
                if attrname == each[0] and reg.match(each[1]):
                    return True
            return None

        if tag == 'textarea' and _attr(attrs, 'id', re.compile('txtare\d+')):
            self.st = True

    def handle_data(self, data):
        if self.st:
            self.movies.append(data)

    def handle_endtag(self, tag):
        if tag == 'textarea':
            self.st = False


if __name__ == "__main__":
    import time as t
    cout = 0
    p = Parser()
    r = redis.Redis(host="localhost", port=6379, db=0)
    start=t.time()
    for i in range(r.llen('sushi')):
        print(i,r.lindex("sushi",i).decode('utf-8'))
    print('cost (s) %f'%(t.time()-start))
    # for i in range(1, 100):
    #     data = p.getHtml(i)
    #     p.feed(data)
    #     print('page:%s' % i)
    #     for a in p.movies:
    #         r.lpush("sushi", a)
    #         cout += 1
            # print(cout, a)
        # print("over")
