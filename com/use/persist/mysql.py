import random

import pymysql as mysql
import redis as redis


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


def savePoemToDb():
    global conn
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


def insertAccount():
    conn = Mysql("101.37.19.131", "root", "Dayee@1603", "oivib_test", port=3308, charset="utf8")
    for i in range(1, 50000):
        interviewId = int(i / 5 + 1)
        accountId = ('%05d' % i)
        role = [0, 1][random.randint(0, 1)]
        t = tt.strftime("%Y-%m-%d %H:%M:%S")
        # conn.exec(
        #     "insert into `t_interview_account` (`F_INTERVIEW_ID`, `F_ACCOUNT_ID`, `F_ROLE`, `F_UID`, `f_post_name`, `F_USER_NAME`, `F_ADD_TIME`, `F_UPDATE_TIME`) values('%s','%s','%s','%s','%s','%s','%s','%s');" % (
        #         interviewId, accountId, role, i, '测试', '张%s' % i, t, t))
        try:
            conn.exec(
                "insert into `t_interview_plan` (`f_id`, `f_corp_code`, `f_corp_name`, `f_start_time`, `f_end_time`, `f_mode`, `f_add_time`, `f_update_time`) values('%s','dayeesz','大易测试',now(),'2020-03-15 18:06:26','2',now(),now());" %
                interviewId)
        except:
            pass
        if (i % 1000 == 0):
            conn.commit()
        print(i)


if __name__ == "__main__":
    # import redis
    import time as tt

    # savePoemToDb()
    insertAccount()
