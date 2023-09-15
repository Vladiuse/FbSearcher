from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register('group_list', views.FbGroupMAssCreateView, basename='group-list')


urlpatterns = [
    # path('', include(router.urls)),
    path('group_list',  views.FbGroupMAssCreateView.as_view(), name='group-list')
]