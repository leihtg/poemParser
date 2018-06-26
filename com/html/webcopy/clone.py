from com.html.parse import *
import urllib.request as req

import os


class CopyWeb:
    maxDeep = 3
    linkDir = 'styles'
    scriptDir = 'scripts'
    imgDir = 'images'

    def __init__(self, savePath, url, deep=0):
        self.savePath = savePath
        self.url = url
        self.deep = deep  # 复制深度
        pass

    # 需要转换的字段
    def __transfer(self):
        return (('link', 'href'), ('script', 'src'), ('a', 'href'), ('iframe', 'src'), ('img', 'src'))

    def doCopy(self):
        if self.deep > self.maxDeep:
            return
        parser = self.parser = HtmlDomParser(self.url)
        dom = parser.parse()
        fname = jQuery(dom).find('title').text()

        # 保存主网页
        if not fname:
            fname = self.url[self.url.rfind('/') + 1:]
        if fname.rfind('.') == -1:
            fname += '.html'
        self.__doTransfer(dom)
        self.__write(fname, dom.toHtml())

    # 转换标签引用链接的路径
    def __doTransfer(self, dom):
        urls = []
        jq = jQuery(dom)
        for tr in self.__transfer():
            tag, attr = tr[0], tr[1]
            for f in jq.find(tag):
                u = f.attr(attr)
                if not u or u.startswith('http'):
                    continue
                if tag == 'a' and u.find(':') > 0:
                    continue
                # 不同资源保存到不同文件里面
                suffix = ''
                if tag == 'link':
                    suffix = self.linkDir
                elif tag == 'script':
                    suffix = self.scriptDir
                elif tag == 'img':
                    suffix = self.imgDir

                realUrl = self.parser.getRealUrl(u)
                ph = ''
                if u[0] == '/':
                    if u[1] and u[1] == '/':  # 对于 `//`开头的用协议头
                        f.attr(attr, self.url[:self.url.find(':') + 1] + u)
                        realUrl = None  # 不需要下载
                    else:
                        ph = './%s%s' % (suffix, u)
                        f.attr(attr, ph)
                elif u[0] == '#':
                    realUrl = None
                    pass
                else:
                    ph = './%s/%s' % (suffix, u)
                    f.attr(attr, ph)

                if realUrl:
                    # tuple(tagType,url,savePath)
                    urls.append((tag, realUrl, ph[1:]))
        # 保存链接网页
        self.__saveSource(urls)

    # 保存资源
    def __saveSource(self, urls):
        for u in urls:
            tag, url, path = u[0], u[1], u[2]
            if tag == 'img' or tag == 'link' or tag == 'script':
                try:
                    data = req.urlopen(url).read()
                    self.__write(path, data)
                except req.HTTPError as args:
                    print('error:[%s],url:[%s]' % (args, url))
            else:
                dir = os.path.dirname(path)
                CopyWeb(self.savePath + os.path.sep + dir, url, self.deep + 1).doCopy()

    def __write(self, fname, data):
        path = self.savePath + os.path.sep + fname
        dirname = os.path.dirname(path)
        if os.path.exists(dirname):
            if not os.path.isdir(dirname):
                raise BaseException('[%s]不是目录' % dirname)
        else:
            os.makedirs(dirname)

        if isinstance(data, bytes):
            open(path, 'wb').write(data)
        else:
            f = open(path, mode='w', encoding='utf8')
            f.write(data)


url = 'http://www.vimregex.com/'
cw = CopyWeb(r'C:\Users\leihuating\Desktop\copy', url)
cw.doCopy()

from redis import *

# r = Redis(host="172.29.97.155")
# conn=r.pubsub()
# conn.psubscribe("copyWeb")
# conn.listen()
# while True:
#     sb=conn.parse_response()
#     print(sb)
