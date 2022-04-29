import cx_Oracle as Oracle
import pymysql
from DBUtils.PooledDB import PooledDB
import threading
import json
import time
import sys




class Triple:

    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='demo',charset='utf8')
        self.cursor = self.conn.cursor()

    def check_triple(self, source, target):
        sql = "select count(1) from graph where source='%s' and target='%s'" % (source, target)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data[0][0]

    def triple_operate(self, entity_exits, data):
        if entity_exits == 0:
            sql = "insert into graph(source, rela, target, text, get_time) values('%s', '%s', '%s','%s', '%s')" % (
                data['entity1'], data['relationship'], data['entity2'], data['sentence'], data['get_time'])
            self.cursor.execute(sql)
        return

    def rela_operate(self, relationship):
        times = time.strftime("%Y-%m-%d")
        sql = "insert into relationship(relationship, intime) values('%s','%s')" %(relationship, times)
        self.cursor.execute(sql)
        return

    def check_entity(self, entity):
        sql = "select count(1) from entity where entity='%s'" % entity
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data[0][0]

    def entity_operate(self, entity_exits, entity, classify):
        times = time.strftime("%Y-%m-%d")
        if entity_exits == 0:
            sql = "insert into entity(entity, classify, intime) values('%s', '%s','%s')" % (entity, classify, times)
            self.cursor.execute(sql)
        return

    def triple_submit(self, all_data):
        flag = 0
        for data in all_data:
            try:
                triple_exits = self.check_triple(data['entity1'], data['entity2'])
                self.triple_operate(triple_exits, data)
                entity1_is_exits = self.check_entity(data['entity1'])
                self.entity_operate(entity1_is_exits, data['entity1'], data['classify1'])
                entity2_is_exits = self.check_entity(data['entity2'])
                self.entity_operate(entity2_is_exits, data['entity2'], data['classify2'])
                self.rela_operate(data['relationship'])
                flag += 1
                if flag % 2000 == 0:
                    self.conn.commit()
                    print('提交了2000')
            except Exception as e:
                print(e)
                pass
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        return


class myThread (threading.Thread):

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    def run(self):
        Triple().triple_submit(self.data)


if len(sys.argv) == 1:
    print('输入路径!')
    exit(0)
filepath = sys.argv[1]


all_data = []
with open(filepath, 'rb') as f:
    file_data = f.readlines()
    for row in file_data:
        data = {}
        row = json.loads(row)
        if len(row['spo_list']) != 0:
            data['entity1'] = row['spo_list']['subject']
            data['classify1'] = row['spo_list']['subject_type']
            data['relationship'] = row['spo_list']['predicate']
            data['entity2'] = row['spo_list']['object']
            data['classify2'] = row['spo_list']['object_type']
            data['sentence'] = row['text']
            if row['date'] == 'unknown':
                data['get_time'] = ''
            elif type(row['date']) is list :
                data['get_time'] = row['date'][0]
            else:
                data['get_time'] = row['date']
            all_data.append(data)
thread_num = 10
num = len(all_data)//thread_num
a = [all_data[j * num:(j + 1) * num] for j in range(thread_num)]
a.append(all_data[thread_num*num:])
threads = []
print('正在执行，请勿关闭')
for j in range(thread_num+1):
    threads.append(myThread(a[j]))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print('执行完成')

