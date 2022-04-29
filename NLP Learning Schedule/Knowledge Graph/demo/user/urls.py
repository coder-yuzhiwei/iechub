

from django.urls import path,re_path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/user_login', views.user_login, name='user_login'),
    path('register/user_register', views.user_register,name = 'user_register'),
    path('login/loginout', views.loginout, name='loginout'),
]