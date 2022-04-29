from django.shortcuts import render,HttpResponse,redirect
from django.http.response import StreamingHttpResponse
from django.http import JsonResponse
from . import model
from django.views.decorators.csrf import csrf_exempt


def index(req):
    tips = model.get_tips()
    return render(req, 'index1.html', {'tips':tips})


@csrf_exempt
def get_kgdata(request):
    entity = request.POST.get('entity')
    attribute = request.POST.getlist('attribute[]')
    if len(attribute) == 0:
        attribute = None
    kgdata = model.get_data(entity, attribute)
    return JsonResponse({'kgdata': kgdata})


def get_relation(request):
    key = request.GET.get('key')
    relation = model.get_relation(key)
    return JsonResponse({'relation': relation})


def get_attribute(request):
    entity = request.GET.get('entity')
    data = model.get_attribute(entity)
    strs = ''
    if data:
        for i in data:
            strs += '('+i['source']+', '+i['rela']+', '+i['target']+')<br>'
    else:
        strs = 'NULL'
    return JsonResponse({'data': strs})


def login(req):
    try:
        if req.COOKIES['username'] is not None:
            return redirect(req, '/index')
    except:
        return render(req, 'login.html')


def register(req):
    return render(req, 'register.html')


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
