from django.shortcuts import render
from django.http import JsonResponse
from .models import Triple
import json
import time
import os
from django.http.response import StreamingHttpResponse
# Create your views here.


def generate_triple(req):
    jsons = dict()
    if req.method == 'POST':
        text = req.FILES.get('file')
        try:  # 模型识别
            jsons['code'] = 1
            jsons['msg'] = '识别成功'
            jsons['triple'] = [{"spo_list": {"predicate": "位于", "subject": "美空军第12太空预警中队", "subject_type": "部队", "object": "格陵兰岛西北海岸", "object_type": "地域", "confidence": 0}, "text": "图勒空军基地位于格陵兰岛西北海岸，是美军最北端的基地，也是北极圈以北的唯一美军军用设施。它是美空军第12太空预警中队的所在地，其利用尺寸巨大的AN/FPS-132相控阵雷达实施全天候导弹预警和太空监视。", "source": "2019-08-01%5830", "url": "该条为标注数据，暂未添加url链接，后续版本将更新。", "date": "2019-08-08 12:58:27"},
                               {"spo_list": {"predicate": "停泊", "subject": "CF-18战机", "subject_type": "飞机", "object": "图勒基地", "object_type": "基地", "confidence": 0}, "text": "临时在图勒基地休整的加拿大空军CF-18战机。", "source": "2019-08-01%5830", "url": "该条为标注数据，暂未添加url链接，后续版本将更新。", "date": "2019-08-08 12:58:27"}]
            rands = time.time()
            filename = "./data/tmp/%sfile.json" % rands
            with open(filename, 'w') as f:
                for i in jsons['triple']:
                    f.write(json.dumps(i, ensure_ascii=False)+'\n')
            jsons['rands'] = rands
            jsons['time'] = '13:23:10'
            return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            print(e)
            jsons['code'] = 0
            jsons['msg'] = '识别失败'
            jsons['triple'] = []
            jsons['time'] = '0'
            return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
    else:
        jsons['code'] = '0'
        jsons['msg'] = '请求错误'
        return JsonResponse(jsons)


def generate_triple_submit(req):
    rands = req.GET.get('rands')
    stars = req.GET.get('stars')
    jsons = {}
    filepath = "./data/tmp/%sfile.json" % rands
    try:
        with open(filepath, 'r') as f:
            row = f.readline()
            while row:
                row = json.loads(row)
                data = {}
                data['entity1'] = row['spo_list']['subject']
                data['classify1'] = row['spo_list']['subject_type']
                data['relationship'] = row['spo_list']['predicate']
                data['entity2'] = row['spo_list']['object']
                data['classify2'] = row['spo_list']['object_type']
                data['sentence'] = row['text']
                data['get_time'] = row['date']
                Triple().triple_submit(data, file_sentence=row, stars=stars)
                row = f.readline()
        os.remove(path=filepath)
        jsons['code'] = 1
        jsons['msg'] = '保存成功'
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        print(e)
        jsons['code'] = 0
        jsons['msg'] = '保存失败'
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})


def mark_triple_file(req):
    jsons = dict()
    if req.method == 'POST':
        try:
            text = req.FILES.get('upload_file').read()
            jsons['code'] = 1
            jsons['msg'] = '识别成功'
            jsons['text'] = text
            return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            print(e)
            jsons['code'] = 0
            jsons['msg'] = '识别失败'
            jsons['text'] = ''
            return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
    else:
        jsons['code'] = '0'
        jsons['msg'] = '请求错误'
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})


def mark_triple_submit(req):
    jsons = dict()
    if req.method == 'POST':
        try:
            data = json.loads(req.body)
            Triple().triple_submit(data)
            jsons['code'] = 1
            jsons['msg'] = '标注成功'
            return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            print(e)
            jsons['code'] = 0
            jsons['msg'] = '标注失败'
            return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})
    else:
        jsons['code'] = 0
        jsons['msg'] = '请求错误'
        return JsonResponse(jsons, json_dumps_params={'ensure_ascii': False})


def file_iterator(file_name, chunk_size=512):
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def download(req):
    path = './data/knowledgegraph.json'
    file = file_iterator(path)
    response = StreamingHttpResponse(file)
    response['Content-Type'] = 'application/txt'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format('knowledgegraph.json')
    return response
