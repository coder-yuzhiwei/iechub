from django.db import models
from common.database import OraclePool
# Create your models here.
from common.test import OraclePool as oracle

orcl = OraclePool()


def overview_query_entity():
    # orcl = oracle()
    entity_category_sql = 'select count(distinct classify) from entity'
    entity_sum_sql = 'select count(distinct entity) from entity'
    entity_sql = 'select distinct classify from entity'
    entity_category = orcl.fetch_all_array(entity_category_sql)[0][0]
    entity_sum = orcl.fetch_all_array(entity_sum_sql)[0][0]
    data = orcl.fetch_all_array(entity_sql)
    entity = []
    for i in data:
        entity.append(i[0])
    # orcl.close_conn()
    return entity_category, entity_sum, entity


def overview_query_rela():
    # orcl = oracle()
    rela_category_sql = 'select count(distinct relationship) from relationship'
    rela_sum_sql = 'select count(1) from relationship'
    rela_sql = 'select distinct relationship from relationship'
    rela_category = orcl.fetch_all_array(rela_category_sql)[0][0]
    rela_sum = orcl.fetch_all_array(rela_sum_sql)[0][0]
    data = orcl.fetch_all_array(rela_sql)
    relationship = []
    for i in data:
        relationship.append(i[0])
    # orcl.close_conn()
    return rela_category, rela_sum, relationship


def get_update_time():
    # orcl = oracle()
    sql = "select date_format(intime,'%Y-%m-%d') from entity order by intime desc"
    data = orcl.fetch_all_array(sql)
    # orcl.close_conn()
    return data


def overview_add():
    # orcl = oracle()
    add_time = get_update_time()
    if add_time:
        add_time = add_time[0][0]
    add_entity_sql = "select count(distinct entity) from entity where intime='%s'" % add_time
    add_rela_sql = "select count(1) from relationship where intime='%s'" % add_time
    add_entity = orcl.fetch_all_array(add_entity_sql)[0][0]
    add_rela = orcl.fetch_all_array(add_rela_sql)[0][0]
    # orcl.close_conn()
    return add_entity, add_rela, add_time


def query_entity_triple(entity, limit=0):
    # orcl = oracle()
    if limit==0:
        sql = "select id,source,rela,target,rela_stars as stars,get_time " \
              "from graph where source='%s' and target !='%s'" % (entity, entity)
    else:
        sql = "select id,source,rela,target,rela_stars as stars,get_time " \
              "from graph where source='%s' and target !='%s' limit %s" % (entity, entity, limit)
    triple = orcl.fetch_all_dict(sql)
    relationship = set()
    for i in triple:
        relationship.add(i['rela'])
    relationship = list(relationship)
    # orcl.close_conn()
    return triple, relationship


def query_entity_rela(entity):
    # orcl = OraclePool()
    sql = "select distinct rela from graph where source='%s'" % entity
    data = orcl.fetch_all_array(sql)
    relationship = []
    if data:
        for i in data:
            relationship.append(i[0])
    return relationship


def query_entity_to_entity(entity1, entity2):
    # orcl = oracle()
    sql = "select id,source,rela,target,rela_stars as stars,get_time" \
          " from graph where (source='%s' and target='%s') or (target='%s' and source='%s')" % (entity1, entity2, entity1, entity2)
    triple = orcl.fetch_all_dict(sql)
    # orcl.close_conn()
    return triple


def query_entity_attribute(entity, limit=0):
    # orcl = OraclePool()
    if limit == 0:
        sql = "select id,entity as source,attribute as rela,value as target from attribute where entity='%s'" % (entity)
    else:
        sql = "select id,entity as source,attribute as rela,value as target from attribute where entity='%s' limit %s" % (entity, limit)
    data = orcl.fetch_all_dict(sql)
    return data


def query_attributes(entity):
    # orcl = OraclePool()
    sql = "select distinct attribute from attribute where entity='%s'" % entity
    data = orcl.fetch_all_array(sql)
    result = []
    if data:
        for i in data:
            result.append(i[0])
    return result


def source_data(entity1, entity2):
    # orcl = OraclePool()
    if entity2 is None or entity2 == '':
        sql = "select id,source,rela,target,text from graph where source='%s'" % entity1
    else:
        sql = "select id,source,rela,target,text from graph where source='%s' and target='%s'" % (entity1, entity2)
    triple = orcl.fetch_all_dict(sql)
    return triple


def get_entity_stars(entity1, entity2):
    # orcl = OraclePool()
    if entity2 is None or entity2 == '':
        sql = "select stars from entity_stars where object_entity='%s'" % entity1
    else:
        sql = "select rela_stars from graph where source='%s' and target='%s'" % (entity1, entity2)
    stars = orcl.fetch_all_array(sql)
    if stars:
        if stars[0][0] is not None:
            return stars[0][0]
    return ''


def post_stars(entity1, entity2, stars):
    # orcl = OraclePool()
    if stars == "":
        return
    if entity2 is None or entity2 == '':
        count = orcl.fetch_all_array("select count(1) from entity_stars where object_entity='%s'" % entity1)
        sql = "insert into entity_stars(object_entity, stars) values('%s', '%s')" % (entity1, int(stars)/100)
        if count:
            if count[0][0] != 0:
                sql = "update entity_stars set stars='%s' where object_entity='%s'" % (int(stars)/100, entity1)
    else:
        sql = "update graph set rela_stars='%s' where source='%s' and target='%s'" % (int(stars)/100, entity1, entity2)
    orcl.execute_sql(sql)
    return


def get_dim_entity(keyword):
    # orcl = OraclePool()
    sql = "select distinct source from graph where source like '%"+keyword+"%'"
    data = orcl.fetch_all_array(sql)
    entity = []
    if data:
        for i in data:
            entity.append(i[0])
    return entity


def overview_entity_attribute():
    entity_category_name = ['国家', '舰船', '飞机', '武器装备', '探测装备', '通信装备', '基地', '港口', '机场', '生产厂家', '部队', '人员', '卫星', '地域']
    # orcl = OraclePool()
    entity_to_attribute = {}
    for i in entity_category_name:
        sql = "select distinct attribute from attribute where entitycategory='%s'" % i
        num_sql = "select count(1) from entity where classify='%s'" % i
        tmp = {}
        attribute = []
        num = 0
        try:
            attribute = [j[0] for j in orcl.fetch_all_array(sql)]  # 查询到空数据则数组为空
            num = orcl.fetch_all_array(num_sql)[0][0]
        except:
            pass
        tmp['attribute'] = attribute
        tmp['num'] = num
        entity_to_attribute[i] = tmp
    return entity_category_name, entity_to_attribute


def overview_relationship_category():
    relationship_category_name = ['属性相似/相异', '时空关联', '指挥从属', '协同协作', '生产保障']
    relacategory_to_relationship = {
        '属性相似/相异': {'text': '同一种类型的实体之间的某一属性维度的相似或相异', 'num': 0, 'relationship': ['属性相似关系','属性相异关系']},
        '时空关联': {'text': '某一时间，地域实体与其他实体之间的关系', 'num': 0, 'relationship': ['位于关系','到达关系','离开关系','停留关系','穿过关系','侦测关系','被侦测关系']},
        '指挥从属': {'text': '高级别实体与低级别实体之间的关系', 'num': 0, 'relationship': ['编队协同关系','协同关系','即时协作关系','工作协同关系']},
        '协同协作': {'text': '具备工作能力的实体之间的协作关系', 'num': 0, 'relationship': ['隶属关系','包含关系','指挥关系','被指挥关系','操作关系','被操作关系','调用关系','被调用关系','雇佣关系','被雇佣关系']},
        '生产保障': {'text': '生产厂家、机场、港口等实体与其生产、保障、装配的实体之间的关系', 'num': 0, 'relationship': ['装配关系','所属关系','保障关系','被保障关系','停泊关系','被停泊关系','制造关系','被制造关系']}
    }
    # orcl = OraclePool()
    for key, value in relacategory_to_relationship.items():
        relationship = value['relationship']
        num = 0
        for i in relationship:
            i = i.replace('关系', '')
            sql = "select count(1) from relationship where relationship='%s'" % i
            data = orcl.fetch_all_array(sql)
            if data:
                try:
                    num += data[0][0]
                except:
                    pass
        relacategory_to_relationship[key]['num'] = num
    return relationship_category_name, relacategory_to_relationship


def overview_attribute_num():
    sql = 'select count(1) from attribute'
    data = orcl.fetch_all_array(sql)
    return data[0][0]


def get_triple_by_rela(relationship, limit):
    limit = limit.replace(' ', '')
    if limit is None or limit == '':
        limit = 5
    sql = "select id,source,rela,target,get_time from graph where rela = '%s' limit %s" %(relationship, limit)
    data = orcl.fetch_all_dict(sql)
    return data


def get_entity_autocomplete(in_entity):
    if in_entity is None or in_entity == '':
        sql = "select distinct entity from attribute"
    else:
        sql = "select distinct entity from attribute where entity like '%" + in_entity + "%'"
    try:
        entity = [i[0] for i in orcl.fetch_all_array(sql)]
    except:
        entity = []
    return entity


def get_atttibute_by_entity(entity, limit):
    sql = "select id,entity,attribute,value from attribute where entity = '%s' limit %s" % (entity, limit)
    print(sql)
    triple = orcl.fetch_all_dict(sql)
    return triple
