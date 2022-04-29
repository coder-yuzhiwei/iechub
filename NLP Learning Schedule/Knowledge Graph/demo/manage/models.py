from django.db import models
from common.test import OraclePool
# Create your models here.
import time
import json


class Triple:

    def __init__(self, flag):  # flag代表是否是模型识别0 还是 人工标注1
        self.orcl = OraclePool()
        self.flag = flag

    def check_triple(self, source, target):
        sql = "select count(1) from graph where source='%s' and target='%s'" % (source, target)
        data = self.orcl.fetch_all_array(sql)
        if data:
            return data[0][0]
        return 0

    def triple_operate(self, entity_exits, data):
        if entity_exits == 0:
            sql = "insert into graph(source, rela, target, text, get_time) values('%s', '%s', '%s','%s', '%s')" % (
                    data['entity1'], data['relationship'], data['entity2'], data['sentence'], data['get_time'])
            self.orcl.execute_sql(sql)
        else:
            if self.flag == 1:
                sql = "update graph set rela='%s',text='%s',get_time='%s' where source='%s' and target='%s'" % (
                            data['relationship'], data['sentence'], data['get_time'], data['entity1'], data['entity2'])
                self.orcl.execute_sql(sql)
                self.orcl.commit()
        return

    def rela_operate(self, relationship):
        times = time.strftime("%Y-%m-%d")
        sql = "insert into relationship(relationship, intime) values('%s','%s')" %(relationship, times)
        self.orcl.execute_sql(sql)
        return

    def check_entity(self, entity):
        sql = "select count(1) from entity where entity='%s'" % entity
        data = self.orcl.fetch_all_array(sql)
        if data:
            return data[0][0]
        return 0

    def entity_operate(self, entity_exits, entity, classify):
        times = time.strftime("%Y-%m-%d")
        if entity_exits == 0:
            sql = "insert into entity(entity, classify, intime) values('%s', '%s','%s')" % (entity, classify, times)
            self.orcl.execute_sql(sql)
        else:
            if self.flag == 1:
                sql = "update entity set entity='%s', classify='%s', intime='%s' where entity='%s'" % (
                        entity, classify, times, entity)
                self.orcl.execute_sql(sql)
                self.orcl.commit()
        return

    def triple_submit(self, all_data):
        for data in all_data:
            triple_exits = self.check_triple(data['entity1'], data['entity2'])
            self.triple_operate(triple_exits, data)
            entity1_is_exits = self.check_entity(data['entity1'])
            self.entity_operate(entity1_is_exits, data['entity1'], data['classify1'])
            entity2_is_exits = self.check_entity(data['entity2'])
            self.entity_operate(entity2_is_exits, data['entity2'], data['classify2'])
            self.rela_operate(data['relationship'])
            file_sentence = {"spo_list": {"predicate": data['relationship'], "subject": data['entity1'], "subject_type": data['classify1'], "object": data['entity2'], "object_type": data['classify2'], "confidence": ''}, "text": data['sentence'], "source": "", "url": "该条为标注数据，暂未添加url链接，后续版本将更新。", "date": data['get_time']}
            with open('./data/knowledgegraph.json', 'a', encoding='utf-8') as f:
                f.write('\n')
                f.write(json.dumps(file_sentence,ensure_ascii=False))
        self.orcl.commit()
        self.orcl.close_conn()
        return


