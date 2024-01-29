from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('ping-ds/<str:ds_name>/', views.ping_ds,),
]