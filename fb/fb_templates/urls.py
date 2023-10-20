from django.urls import path
from . import views
app_name = 'fb_templates'
urlpatterns = [
    path('', views.index, name='index')
]