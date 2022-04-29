from django.shortcuts import render,redirect
from django.http.response import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def loginout(req):
    try:
        req.COOKIES.pop('username')
        return redirect(req, '/login')
    except Exception as e:
        print(e)
        return redirect('/login')


def user_login(req):
    username = req.POST['username']
    password = req.POST['passwd']
    database_pas = get_password(username)
    jsons = {
        'code': 0,
        'msg': '用户名或密码错误',
        'result': {'username': username}
    }
    if database_pas:
        if password == database_pas[0][0]:
            jsons = {
                'code': 1,
                'msg': "登录成功",
                'result': {'username': username}
            }
    response = JsonResponse(jsons, json_dumps_params={'ensure_ascii':False})
    if jsons['code'] == 1:
        response.set_cookie('username', username)
    return response


@csrf_exempt
def user_register(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['passwd']
        password2 = req.POST['passwd2']
        checks = check_user(username)
        if checks:
            if checks[0][0] == 1:
                return JsonResponse({'code':'0', 'msg':'用户名存在!'}, safe=False, json_dumps_params={'ensure_ascii':False})
        if password != password2:
            return JsonResponse({'code': 0, 'msg':'两次密码不一致!'}, safe=False, json_dumps_params={'ensure_ascii':False})
        try:
            register_user(username, password)
            return JsonResponse({'code': 1, 'msg':'注册成功!'}, safe=False, json_dumps_params={'ensure_ascii':False})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 0, 'msg': 'error'}, safe=False, json_dumps_params={'ensure_ascii': False})


