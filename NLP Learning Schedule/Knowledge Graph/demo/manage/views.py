from django.shortcuts import render
from django.http import JsonResponse
from .models import Triple
import json
import time
import os
import sys
from django.http.response import StreamingHttpResponse
import traceback
import threading
# Create your views here.


def generate_triple(req):
    jsons = dict()
    if req.method == 'POST':
        csv_file = req.FILES.get('file')
        rands = time.time()
        rands = str(rands)  # 文件名的随机数
        csv_filename = "./data/csv/%s.csv" % rands
        destination = open(csv_filename, 'wb+')
        for chunk in csv_file.chunks():  # 写文件
            destination.write(chunk)
        destination.close()
        # 模型识别
        sys.path.append('../')
        os.chdir('./DuIe_baseline')
        # 是否设置不显示输出
        # path = '../data/keyword_extract_file.csv'
        # os.system(r'python -u ./ernie/run_predict.py --test_save {}'.format(rands))
        os.system(u'python -u ./ernie/run_duie.py \
                           --use_cuda true \
                           --do_train false \
                           --do_val false \
                           --do_test true \
                           --batch_size 8 \
                           --init_checkpoint ./checkpoints/step_10201/ \
                           --num_labels 118 \
                           --label_map_config ./data/re4.json \
                           --spo_label_map_config ./data/lab4.json \
                           --test_set ../data/csv/{}.csv \
                           --test_save ../data/tmp/{} \
                           --vocab_path ./pretrained_model/vocab.txt \
                           --ernie_config_path ./pretrained_model/ernie_config.json \
                           --use_fp16 false \
                           --max_seq_len 128 \
                           --skip_steps 10 \
                           --random_seed 1'.format(rands, rands))
        # os.system(r'sh ./script/predict.sh')
        os.chdir('../')
        os.remove(path=csv_filename)
        try:  # 识别生成的文件读取
            jsons['code'] = 1
            jsons['msg'] = '识别成功'
            triple = []
            with open('./data/tmp/%s.json' % rands) as f:
                row = f.readline()
                while row:
                    row = json.loads(row)
                    if row['date'] == 'unknown':
                        row['date'] = ''
                    else:
                        row['date'] = row['date'][0]
                    triple.append(row)
                    row = f.readline()
            with open('./data/tmp/%s.txt' % rands) as f:
                row = f.readline()
                nums, times = row.split(' ')
            filepath = "./data/tmp/%s.txt" % rands
            os.remove(path=filepath)
            jsons['triple'] = triple
            jsons['rands'] = rands
            jsons['time'] = round(float(times),2)
            jsons['num'] = nums
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


class myThread (threading.Thread):

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    def run(self):
        Triple(0).triple_submit(self.data)


def generate_triple_submit(req):
    rands = req.GET.get('rands')
    jsons = {}
    filepath = "./data/tmp/%s.json" % rands
    try:
        all_data = []
        with open(filepath, 'r', encoding='utf-8') as f:
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
                    elif type(row['date']) is list:
                        data['get_time'] = row['date'][0]
                    else:
                        data['get_time'] = row['date']
                    all_data.append(data)
        thread_num = 10
        num = len(all_data) // thread_num
        a = [all_data[j * num:(j + 1) * num] for j in range(thread_num)]
        a.append(all_data[thread_num * num:])
        threads = []
        for j in range(thread_num + 1):
            threads.append(myThread(a[j]))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
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
            req_data = json.loads(req.body)
            req_data['get_time'] = ''
            data = []
            data.append(req_data)
            Triple(1).triple_submit(data)
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
