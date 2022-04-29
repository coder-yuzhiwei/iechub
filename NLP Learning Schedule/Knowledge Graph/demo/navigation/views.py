from django.shortcuts import render
from django.http.response import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.


def overview(req):
    jsons = {}
    try:
        entity_category_num, entity_num, entity = overview_query_entity()
        relationship_category_num, relationship_num, relationship = overview_query_rela()
        add_entity, add_relationship, add_times = overview_add()
        entity_category_name, entity_to_attribute = overview_entity_attribute()
        relationship_category_name, relacategory_to_relationship = overview_relationship_category()
        attribute_num = overview_attribute_num()
        jsons['code'] = 1
        jsons['message'] = '查询成功'
        data = {}
        data['entity_category'] = entity_category_num
        data['entity_num'] = entity_num
        data['relationship_category'] = relationship_category_num
        data['relationship_num'] = relationship_num
        data['add_entity'] = add_entity
        data['add_relationship'] = add_relationship
        data['entity_category_name'] = entity_category_name
        data['entity_to_attribute'] = entity_to_attribute
        data['relationship_category_name'] = relationship_category_name
        data['relacategory_to_relationship'] = relacategory_to_relationship
        data['attribute_num'] = attribute_num
        data['time'] = add_times
        jsons['data'] = data
        jsons['entity'] = entity
        jsons['relationship'] = relationship
        return JsonResponse(jsons, safe=False, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        print(e)
        jsons['code'] = 0
        jsons['msg'] = '查询失败'
        jsons['data'] = {}
        jsons['entity'] = []
        jsons['relationship'] = []
        return JsonResponse(jsons, safe=False, json_dumps_params={'ensure_ascii': False})


def entity_relationship(req):
    jsons = {}
    try:
        entity = req.GET['entity']
        entity = entity.replace('，', ',')
        limit = req.GET.get('limit')
        if ',' not in entity:
            triple, relationship = query_entity_triple(entity, limit)
            # relationship = query_entity_rela(entity, limit)
            jsons['relationship'] = relationship
        else:
            entity1, entity2 = entity.split(',')
            triple = query_entity_to_entity(entity1, entity2)
            jsons['relationship'] = []
        jsons['code'] = 1
        jsons['msg'] = '查询成功'
        jsons['triple'] = triple
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        print(e)
        jsons['code'] = 0
        jsons['msg'] = '查询失败'
        jsons['triple'] = []
        jsons['relationship'] = []
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})


def entity_attribute(req):
    jsons = {}
    try:
        entity = req.GET['entity']
        limit = req.GET['limit']
        triple = query_entity_attribute(entity, limit)
        attributes = query_attributes(entity)
        jsons['code'] = 1
        jsons['msg'] = '查询成功'
        jsons['triple'] = triple
        jsons['attributes'] = attributes
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        print(e)
        jsons['code'] = 0
        jsons['msg'] = '查询失败'
        jsons['triple'] = {}
        jsons['relationship'] = []
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})


def entity_table(req):
    jsons = {}
    try:
        entity = req.GET['entity']
        rela_triple,_ = query_entity_triple(entity)
        attribute_triple = query_entity_attribute(entity)
        jsons['code'] = 1
        jsons['msg'] = '查询成功'
        jsons['attribute'] = attribute_triple
        jsons['relationship'] = rela_triple
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        print(e)
        jsons['code'] = 0
        jsons['msg'] = '查询失败'
        jsons['attribute'] = []
        jsons['relationship'] = []
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})


#溯源数据
def source(req):
    jsons = {}
    try:
        entity1 = req.GET['entity1']
        entity2 = req.GET['entity2']
        # entity2 = req.GET['entity2']
        triple = source_data(entity1, entity2)
        star = get_entity_stars(entity1, entity2)
        jsons['code'] = 1
        jsons['msg'] = '查询成功'
        jsons['triple'] = triple
        jsons['stars'] = star
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        print(e)
        jsons['code'] = 0
        jsons['msg'] = '查询失败'
        jsons['triple'] = []
        jsons['stars'] = None
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})


# 评分 置信度打分
@csrf_exempt
def stars(req):
    jsons = {}
    if req.method == 'POST':
        try:
            data = json.loads(req.body)
            entity1 = data['entity1']
            entity2 = data['entity2']
            stars = data['stars']
            post_stars(entity1, entity2, stars)
            jsons['code'] = 1
            jsons['msg'] = '修改成功'
            return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            print(e)
            jsons['code'] = 0
            jsons['msg'] = '修改失败'
            return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
    else:
        jsons['code'] = '0'
        jsons['msg'] = '请求错误'
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})


# 自动补全查询
def autocomplete(req):
    jsons = {}
    try:
        jsons['code'] = 1
        jsons['msg'] = '查询成功'
        keyword = req.GET.get('keyword')
        jsons['entity'] = []
        if keyword == "" or keyword is None:
            return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
        entity = get_dim_entity(keyword)
        jsons['entity'] = entity
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        print(e)
        jsons['code'] = '0'
        jsons['msg'] = '请求错误'
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})


def relationship_search(req):
    jsons = {'code':0, 'msg':'请求错误','triple':[]}
    try:
        relationship = req.GET.get('relationship')
        limit = req.GET.get('limit')
        triple = get_triple_by_rela(relationship, limit)
        jsons['code'] = 1
        jsons['msg'] = '请求成功'
        jsons['triple'] = triple
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        print(e)
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})


def attribute_autocomplete(req):
    print(1)
    jsons = {'code': 0, 'msg': '请求错误', 'entity': []}
    in_entity = req.GET['entity']
    try:
        entity = get_entity_autocomplete(in_entity)
        jsons['code'] = 1
        jsons['msg'] = '请求成功'
        jsons['entity'] = entity
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        print(e)
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})


def attribute_search(req):
    jsons = {'code': 0, 'msg': '请求错误', 'entity': []}
    try:
        entity = req.GET.get('entity')
        limit = req.GET.get('limit')
        triple = get_atttibute_by_entity(entity, limit)
        jsons['code'] = 1
        jsons['msg'] = '请求成功'
        jsons['triple'] = triple
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        print(e)
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})

