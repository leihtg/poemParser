# -*- coding: utf-8 -*-
txType = {1: '过场动画', 2: '魔法效果'}


class Tx:
    def __init__(self):
        self.txType = None  # 类型
        self.no = None  # 序号
        self.zs = None  # 帧数
        self.maxNo = None  # 最大图号
        self.start = None  # 起始帧
        self.end = None  # 终止帧
        self.z = []

    def __repr__(self) -> str:
        s = '类型:{0},序号:{1},帧数:{2},最大图号:{3}'.format(txType[self.txType], self.no, self.zs, self.maxNo)
        s += '\n起始帧:{0},终止帧:{1}'.format(self.start, self.end)
        z = ''
        for i, v in enumerate(self.z):
            z += '\n帧号:%s,%s' % (i, v)
        return s + z

    def parseZ(self, data):
        z = self.Z()
        z.x = data[0]
        z.y = data[1]
        z.show = data[2]
        z.nshow = data[3]
        z.picNo = data[4]
        self.z.append(z)

    class Z:
        '''
        帧
        '''

        def __init__(self):
            self.x = None
            self.y = None
            self.show = None
            self.nshow = None
            self.picNo = None

        def __repr__(self):
            s = 'x:{0},y:{1},show:{2},nshow:{3},picNo:{4}'.format(self.x, self.y, self.show, self.nshow, self.picNo)
            return '(%s)' % s


picType = {1: '头像类', 2: '界面显示', 3: '战斗主角', 4: '战斗背景', 5: '剧情显示'}
sjjType = {7: 'TITLE图片', 8: '角色图片', 9: '道具图片', 10: '特效图片', 11: '杂类图片'}


class Pic:
    def __init__(self):
        self.type = None
        self.sjj = None
        self.no = None
        self.width = None
        self.height = None

    def parse(self, data):
        self.type = data[0]
        self.seq = data[1]
        self.width = data[2]
        self.height = data[3]
        self.num = data[4]

    def __repr__(self):
        s = 'type:{0},seq:{1},width:{2},height:{3},num:{4}'.format(self.type, self.seq, self.width, self.height, self.num)
        return s


def parsetx(data):
    '''
    特效
    :return:
    '''
    tx = Tx()
    tx.txType = data[0]
    tx.no = data[1]
    tx.zs = data[2]
    tx.maxNo = data[3]
    tx.start = data[4]
    tx.end = data[5]
    c = 6
    step = 5
    for i in range(tx.start, tx.end + 1):
        tx.parseZ(data[c:c + step])
        c += step
    print(c)
    print(data[c:])
    return tx


# path = r'E:\游戏\rpgKf\资源数据\伏魔记图片\游戏中的图片\特效图片\剧情\游戏结束\a.srs'
# f = open(path, 'rb')
# t = parsetx(f.read())
# print(t)
path = r'E:\游戏\rpgKf\资源数据\伏魔记图片\游戏中的图片\道具图片\8001.pic'
p = Pic()
d = open(path, 'rb').read()
p.parse(data=d)
print(p)
print(d)
