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
        self.conn.begin()
        rows = cursor.execute(sql)
        self.conn.commit()
        return rows



if __name__ == "__main__":
    conn = Mysql("172.29.97.155", "root", "root", "springboot")
    conn.exec("insert Poem values('asdk','z','kk',null,null)")
    data = conn.query("select * from Author")
    print(data)
