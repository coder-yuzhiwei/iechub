from django.shortcuts import HttpResponseRedirect

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class SimpleMiddleware(MiddlewareMixin):

    def process_request(self, request):
        paths = ['/login', '/register', '/user/login/user_login', '/user/register/user_register']
        if request.path not in paths:
            try:
                if request.COOKIES['username'] is not None:
                    print(request.COOKIES['username'])
                    pass
            except:
                return HttpResponseRedirect('/login')
