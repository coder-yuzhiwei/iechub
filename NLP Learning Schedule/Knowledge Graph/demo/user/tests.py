from django.test import TestCase
from common.test import OraclePool
import json
# Create your tests here.
import difflib
# import jieba
import Levenshtein
import requests
import time
import datetime
import threading
from manage.models import Triple
filepath = 'D:\\ICE实验室\\demo\\data\\knowledgegraph.json'


class Submit(threading.Thread):

    def __init__(self, array):
        threading.Thread.__init__(self)
        self.array = array

    def run(self):
        for row in self.array:
            row = json.loads(row)
            data = {}
            data['entity1'] = row['spo_list']['subject']
            data['classify1'] = row['spo_list']['subject_type']
            data['relationship'] = row['spo_list']['predicate']
            data['entity2'] = row['spo_list']['object']
            data['classify2'] = row['spo_list']['object_type']
            data['sentence'] = row['text']
            data['get_time'] = row['date']
            Triple().triple_submit(data, file_sentence=row)


with open(filepath,'r',encoding='utf-8') as f:
    row = f.read()
    datas = row.split('\n')

thread_num = 20
nums = len(datas)//thread_num
a = [datas[j*nums:(j+1)*nums] for j in range(thread_num)]
threads = []
for j in range(thread_num):
    threads.append(Submit(a[j]))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print("退出主线程")


# from paddle_serving_client import Client
#
# client = Client()
# client.load_client_config("uci_housing_client/serving_client_conf.prototxt")
# client.connect(["222.20.73.99:9292"])
# data = [0.0137, -0.1136, 0.2553, -0.0692, 0.0582, -0.0727,
#         -0.1583, -0.0584, 0.6283, 0.4919, 0.1856, 0.0795, -0.0332]
# fetch_map = client.predict(feed={"x": data}, fetch=["price"])
# print(fetch_map)
# data = {"feed":[{"x": ["0.0137", "-0.1136", "0.2553", "-0.0692", '0.0582', '-0.0727', '-0.1583', '-0.0584', '0.6283', '0.4919', '0.1856', '0.0795', '-0.0332']}], "fetch":["price"]}
# res = requests.post('http://222.20.73.99:9292/uci/prediction', data=data, headers = {"Content-Type":"application/json"})
# print(res.status_code)
# res = requests.get('http://192.168.1.103:8000/manage/generate_triple_submit?stars=100&rands=1607311156.5499103')
# print(res.content)
# print(res.cookies)
# print(10/100)
# filepath = 'D:\\ICE实验室\\weapon_kg.json'
# orcl = OraclePool()
# flag = 0
# # a = []
# with open(filepath,'rb') as f:
#     row = f.readline()
#     while row:
#         flag += 1
#         data = json.loads(row)['spo_list']
#         subject = data['subject']
#         subject_type = data['subject_type']
#         # a.append(subject)
#         predicate = data['predicate']
#         object = data['object']
#         sql = "insert into attribute(entity, entitycategory, attribute, value) values('%s', '%s', '%s', '%s')" %(subject, subject_type, predicate, object)
#         orcl.execute_sql(sql)
#         row = f.readline()
#         if flag%1000 == 0:
#             print('执行了'+str(flag)+'行')
# a = set(a)
# orcl = OraclePool()
# sql = 'select source,target from graph'
# entity = set()
# for i in orcl.fetch_all_array(sql):
#     entity.add(i[0])
#     entity.add(i[1])
# for data in entity:
#     for normal in a:
#         if data != normal:
#             ignore_list = [' ', '/', '-', '“', '”', '（', '）', '(', ')']
#             # seq = difflib.SequenceMatcher(lambda x: x in ignore_list, data, normal)
#             # ratio = seq.ratio()
#             sim = Levenshtein.jaro_winkler(data, normal)
#             if sim > 0.950:
#                 # sql = "update graph_copy1 set source='%s' where source='%s'" % (normal, data)
#                 # sql1 = "update graph_copy1 set target='%s' where target='%s'" % (normal, data)
#                 # sql2 = "update entity_copy1 set entity='%s' where target='%s'" % (normal, data)
#                 # orcl.execute_sql(sql)
#                 # orcl.execute_sql(sql1)
#                 # orcl.execute_sql(sql2)
#                 print(normal, '     ', data,'  ', sim)




# print(len(a))
# with open('D:\\test.txt', 'a', encoding='gbk') as f:
#     for j in a:
#         try:
#             f.write(j+'\n')
#         except:
#             pass



#计算相似度



# str1 = "歼-20战斗机"
# str2 = "J-20"
#
# # difflib 去掉列表中不需要比较的字符
# ignore_list = [' ', '/', '-', '“', '”', '（', '）', '(', ')']
# seq = difflib.SequenceMatcher(lambda x: x in ignore_list, str1,str2)
# ratio = seq.ratio()
# print ('difflib similarity2: ', ratio)
#
# # 4.计算莱文斯坦比
# sim = Levenshtein.ratio(str1, str2)
# print ('Levenshtein.ratio similarity: ', sim)
#
# # 5.计算jaro距离
# sim = Levenshtein.jaro(str1, str2 )
# print ('Levenshtein.jaro similarity: ', sim)
#
# # 6. Jaro–Winkler距离
# sim = Levenshtein.jaro_winkler(str1 , str2 )
# print ('Levenshtein.jaro_winkler similarity: ', sim)
#
# str1 = "J-16战斗机"
# str2 = "J-20战斗机"
#
# # difflib 去掉列表中不需要比较的字符
# ignore_list = [' ', '/', '-', '“', '”', '（', '）', '(', ')']
# seq = difflib.SequenceMatcher(lambda x: x in ignore_list, str1,str2)
# ratio = seq.ratio()
# print ('difflib similarity2: ', ratio)
#
# # 4.计算莱文斯坦比
# sim = Levenshtein.ratio(str1, str2)
# print ('Levenshtein.ratio similarity: ', sim)
#
# # 5.计算jaro距离
# sim = Levenshtein.jaro(str1, str2 )
# print ('Levenshtein.jaro similarity: ', sim)
#
# # 6. Jaro–Winkler距离
# sim = Levenshtein.jaro_winkler(str1 , str2 )
# print ('Levenshtein.jaro_winkler similarity: ', sim)
# test = {"spo_list": {"predicate": "位于", "subject": "美空军第12太空预警中队", "subject_type": "部队", "object": "格陵兰岛西北海岸", "object_type": "地域", "confidence": 0}, "text": "图勒空军基地位于格陵兰岛西北海岸，是美军最北端的基地，也是北极圈以北的唯一美军军用设施。它是美空军第12太空预警中队的所在地，其利用尺寸巨大的AN/FPS-132相控阵雷达实施全天候导弹预警和太空监视。", "source": "2019-08-01%5830", "url": "该条为标注数据，暂未添加url链接，后续版本将更新。", "date": "2019-08-08 12:58:27"},
# data = json.dumps(test, ensure_ascii=False)
# print(data)