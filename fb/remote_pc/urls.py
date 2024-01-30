from django.urls import path
from . import views

app_name = 'remote_pc'
urlpatterns = [
    path('', views.index, name='index'),
    path('active/', views.active, name='active'),
    path('parse-stat', views.parse_stat, name='parse_stat'),
    path('ping-ds/<str:ds_name>/', views.ping_ds,),
]