from com.html.parse import *
import os

path = r"C:\Users\leihuating\Desktop\hehe\a.html"
print(os.path.exists(path))
os.makedirs(path)


class CopyWeb:
    def __init__(self, savePath, context, url):
        self.savePath = savePath
        self.context = context
        self.url = url
        pass

    # 需要转换的字段
    def __transfer(self):
        return (('link', 'href'), ('script', 'src'), ('a', 'href'), ('iframe', 'src'))

    def doCopy(self):
        urls=[]
        parser = HtmlDomParser(self.url)
        dom = parser.parse()
        jq = jQuery(dom)
        fname = jq.find('title').text()
        for tr in self.__transfer():
            pass

        pass

    def __write(self, fname, data):
        if not os.path.exists(self.savePath):
            os.makedirs(self.savePath)
        f = open(fname, mode='w')
        f.write(data)


from redis import *

# r = Redis(host="172.29.97.155")
# conn=r.pubsub()
# conn.psubscribe("copyWeb")
# conn.listen()
# while True:
#     sb=conn.parse_response()
#     print(sb)
