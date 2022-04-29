﻿import cx_Oracle as Oracle
import pymysql
from DBUtils.PooledDB import PooledDB


class OraclePool:
    """
    1) 这里封装了一些有关oracle连接池的功能;
    2) sid和service_name，程序会自动判断哪个有值，
        若两个都有值，则默认使用service_name；
    3) 关于config的设置，注意只有 port 的值的类型是 int，以下是config样例:
        config = {
            'user':         'maixiaochai',
            'password':     'maixiaochai',
            'host':         '192.168.158.1',
            'port':         1521,
            'sid':          'maixiaochai',
            'service_name': 'maixiaochai'
        }
    """

    def __init__(self):
        """
        获得连接池
        :param config:      dict    Oracle连接信息
        """
        config = {
            'user': 'root',
            'password': '123456',
            'host': '127.0.0.1',
            'port': 3306,
            'db': 'demo'
        }
        self.__pool = self.__get_pool(config)

    @staticmethod
    def __get_pool(config):
        """
        :param config:        dict    连接Oracle的信息
        ---------------------------------------------
        以下设置，根据需要进行配置
        maxconnections=6,   # 最大连接数，0或None表示不限制连接数
        mincached=2,        # 初始化时，连接池中至少创建的空闲连接。0表示不创建
        maxcached=5,        # 连接池中最多允许的空闲连接数，很久没有用户访问，连接池释放了一个，由6个变为5个，
                            # 又过了很久，不再释放，因为该项设置的数量为5
        maxshared=0,        # 在多个线程中，最多共享的连接数，Python中无用，会最终设置为0
        blocking=True,      # 没有闲置连接的时候是否等待， True，等待，阻塞住；False，不等待，抛出异常。
        maxusage=None,      # 一个连接最多被使用的次数，None表示无限制
        setession=[],       # 会话之前所执行的命令, 如["set charset ...", "set datestyle ..."]
        ping=0,             # 0  永远不ping
                            # 1，默认值，用到连接时先ping一下服务器
                            # 2, 当cursor被创建时ping
                            # 4, 当SQL语句被执行时ping
                            # 7, 总是先ping
        """
        dsn = None
        host, port = config.get('host'), config.get('port')

        # if 'db' in config:
        #     dsn = Oracle.makedsn(host, port, service_name=config.get('db'))
        #
        # elif 'sid' in config:
        #     dsn = Oracle.makedsn(host, port, sid=config.get('sid'))

        pool = PooledDB(
            pymysql,
            mincached=5,
            maxcached=20,
            user=config.get('user'),
            password=config.get('password'),
            host=host,
            port=port,
            db=config.get('db'),
            ping=0,
            maxconnections=30,
            charset='utf8'
        )

        return pool

    def __get_conn(self):
        """
        从连接池中获取一个连接，并获取游标。
        :return: conn, cursor
        """
        conn = self.__pool.connection()
        cursor = conn.cursor()

        return conn, cursor

    @staticmethod
    def __reset_conn(conn, cursor):
        """
        把连接放回连接池。
        :return:
        """
        cursor.close()
        conn.close()

    def __execute(self, sql, args=None):
        """
        执行sql语句
        :param sql:     str     sql语句
        :param args:    list    sql语句参数列表
        :param return:  cursor
        """
        conn, cursor = self.__get_conn()
        try:
            if args:
                cursor.execute(sql, args)
            else:
                cursor.execute(sql)
        except:
            print('error sql   ' + sql)

        return conn, cursor

    def fetch_all_dict(self, sql, args=None):
        """
        获取全部结果
        :param sql:     str     sql语句
        :param args:    list    sql语句参数
        :return:        tuple   fetch结果
        """
        conn, cursor = self.__execute(sql, args)
        result = cursor.fetchall()
        cur_desc = cursor.description
        data = []
        self.__reset_conn(conn, cursor)
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

    def fetch_all_array(self, sql, args=None):
        """
        获取全部结果
        :param sql:     str     sql语句
        :param args:    list    sql语句参数
        :return:        tuple   fetch结果
        """
        conn, cursor = self.__execute(sql, args)
        result = cursor.fetchall()
        data = []
        if result:
            for i in result:
                data.append(list(i))
        return data

    def fetch_one(self, sql, args=None):
        """
        获取全部结果
        :param sql:     str     sql语句
        :param args:    list    sql语句参数
        :return:        tuple   fetch结果
        """
        conn, cursor = self.__execute(sql, args)
        result = cursor.fetchone()
        self.__reset_conn(conn, cursor)
        return result

    def execute_sql(self, sql, args=None):
        """
        执行SQL语句。
        :param sql:     str     sql语句
        :param args:    list    sql语句参数
        :return:        tuple   fetch结果
        """
        conn, cursor = self.__execute(sql, args)
        conn.commit()
        self.__reset_conn(conn, cursor)

    def __del__(self):
        """
        关闭连接池。
        """
        try:
            self.__pool.close()
        except Exception as e:
            print(e)


def demo():
    sql = "select password from users where username='lp'"
    orcl = OraclePool()
    result = orcl.fetch_all_array(sql)
    if not result:
        print('null')
