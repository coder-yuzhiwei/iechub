import cx_Oracle
import pymysql


class OraclePool:

    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='demo',charset='utf8')
        self.cur = self.conn.cursor()

    def execute_sql(self, sql):
        try:
            self.cur.execute(sql)
        except:
            print('error '+sql)

    def fetch_all_array(self, sql):
        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
            if result:
                data = []
                for i in result:
                    data.append(list(i))
                return data
            else:
                return []
        except:
            print(sql)

    def fetch_all_dict(self, sql):
        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
            cur_desc = self.cur.description
            data = []
            if result:
                for i in range(len(result)):
                    cos = {}
                    for j in range(len(cur_desc)):
                        x = i
                        rs = result[x][j]
                        cos[cur_desc[j][0]] = rs
                    data.append(cos)
                return data
            else:
                return []
        except:
            print(sql)

    def commit(self):
        self.conn.commit()

    def close_conn(self):
        self.cur.close()
        self.conn.close()
