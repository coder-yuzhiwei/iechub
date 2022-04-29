from django.urls import path
from . import views

app_name = 'manage'

urlpatterns = [
    path('download', views.download, name='download'),
    path('generate_triple', views.generate_triple, name='generate_triple'),
    path('generate_triple_submit', views.generate_triple_submit, name='generate_triple_submit'),
    path('mark_triple_file', views.mark_triple_file, name='mark_triple_file'),
    path('mark_triple_submit', views.mark_triple_submit, name='mark_triple_submit'),
]
