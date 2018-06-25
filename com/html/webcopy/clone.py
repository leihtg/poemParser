from com.html.parse import *
import os


class CopyWeb:
    def __init__(self, savePath, url):
        self.savePath = savePath
        self.url = url
        pass

    # 需要转换的字段
    def __transfer(self):
        return (('link', 'href'), ('script', 'src'), ('a', 'href'), ('iframe', 'src'))

    def doCopy(self):
        urls = []
        parser = HtmlDomParser(self.url)
        dom = parser.parse()
        jq = jQuery(dom)
        fname = jq.find('title').text()
        for tr in self.__transfer():
            for f in jq.find(tr[0]):
                u = f.attr(tr[1])
                if u and u[0] == '/':
                    f.attr(tr[1], '.%s' % u)
                    urls.append((parser.getRealUrl(u), u))
            pass
        self.__write(fname, dom.toHtml())

    def __write(self, fname, data):
        if not os.path.exists(self.savePath):
            os.makedirs(self.savePath)
        f = open('%s/%s.html' % (self.savePath, fname), mode='w',encoding='utf8')
        f.write(data)


cw = CopyWeb(r'C:\Users\Thinkpad\Desktop\copy', 'https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_18119813560590364103%22%7D&n_type=0&p_from=1')
cw.doCopy()

from redis import *

# r = Redis(host="172.29.97.155")
# conn=r.pubsub()
# conn.psubscribe("copyWeb")
# conn.listen()
# while True:
#     sb=conn.parse_response()
#     print(sb)
