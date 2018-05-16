import pymysql as mysql


class Mysql:
    def __init__(self, *args, **kwargs):
        self.conn = mysql.connect(*args, **kwargs)

    def query(self, sql):
        list = []
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        fields = []
        for i in cursor.description:
            fields.append(i[0])
        for row in result:
            data = {}
            for i, v in enumerate(fields):
                data[v] = row[i]
            list.append(data)
        return list

    def insert(self, sql):
        pass

    def exec(self, sql):
        cursor = self.conn.cursor()
        try:
            # self.conn.begin()
            rows = cursor.execute(sql)
            # self.conn.commit()
        except BaseException as args:
            # self.conn.rollback()
            raise Exception(args)

        return rows

    def commit(self):
        self.conn.commit()


if __name__ == "__main__":
    import redis
    import time as tt

    conn = Mysql("172.29.97.155", "root", "root", "springboot", charset="utf8")


    def saveAuthor(id, name):
        conn.exec("insert into Author(id,name) values('%d','%s')" % (id, name))


    def savePoem(id, title, authorId, content=""):
        content = content.replace("'", "''")
        conn.exec(
            "insert into Poem(id,title,authorId,content) values ('%d','%s','%s','%s')" % (id, title, authorId, content))


    start = tt.time()
    r = redis.Redis(host="localhost", port=6379)
    count = 0
    t = 0
    for a in r.keys():
        if r.type(a) == b'list':
            count += 1
            saveAuthor(count, bytes(a).decode())
            for i in range(r.llen(a)):
                t += 1
                data = bytes(r.lindex(a, i)).decode()

                pos = data.index("——")
                s = data.index("《", pos)
                e = data.rindex("》")
                title = data[s + 1:e]
                content = data[:pos]
                savePoem(t, title, count, content)
            conn.commit()

    print('cost (s) %f' % (tt.time() - start))
