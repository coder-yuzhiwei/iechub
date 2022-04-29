import json
from demo.settings import BASE_DIR
from py2neo import Graph,Node,Relationship


def get_tips():
    jsonfile = BASE_DIR + '/data/entity_file.json'  # 生成的json地址
    with open(jsonfile,encoding='utf-8') as f:
        data=[]
        tmp_row=f.readline()
        while tmp_row:
            data.append(json.loads(tmp_row))
            tmp_row=f.readline()
        entity_array = []
        for row in data:
            entity_array.append(row['spo_list']['subject'])  # 添加实体名
        entity_array = list(set(entity_array))
    return entity_array


def get_contact(data, key, relation=None, relate=False):
    kf_data = []
    for row in data:
        row_data = row['spo_list']
        if row_data['subject'] == key:
            if (relation is not None and row_data['predicate'] in relation) or relation is None:
                tmp_dict = {'source': row_data['subject'], 'target': row_data['object'], 'rela': row_data['predicate'],
                            'type': 'resolved'}
                kf_data.append(tmp_dict)
                if relate is True:
                    if row_data['object'] != key:
                        tmp_kf_data = get_contact(data, row_data['object'],relation=None, relate=True)
                        kf_data.extend(tmp_kf_data)
    return kf_data


def get_data(key, relation=None):
    jsonfile = BASE_DIR + '/data/entity_file.json'  # 生成的json地址
    with open(jsonfile,encoding='utf-8') as f:
        data = []  # 读取文件保存数据
        tmp_row = f.readline()
        while tmp_row:
            data.append(json.loads(tmp_row))
            tmp_row = f.readline()
        kf_data = get_contact(data, key, relation, True)
        return kf_data


def get_relation(key):
    kf_data = get_data(key)
    relation =[]
    for i in kf_data:
        if i['source'] == key:
            relation.append(i['rela'])
    return list(set(relation))


def get_attribute(entity):
    jsonfile = BASE_DIR + '/data/attribute_file.json'
    with open(jsonfile,encoding='utf-8') as f:
        data = []  # 读取文件保存数据
        tmp_row = f.readline()
        while tmp_row:
            data.append(json.loads(tmp_row))
            tmp_row = f.readline()
        attribute_data = get_contact(data, entity, relation=None, relate=False)
        return attribute_data

