from django.urls import path
from . import views
app_name = 'fb_templates'
urlpatterns = [
    path('', views.index, name='index'),
    path('view/<int:tmp_id>/', views.view_template, name='view_template'),
]