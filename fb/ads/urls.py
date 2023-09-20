from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register('group_list', views.FbGroupMAssCreateView, basename='group-list')


urlpatterns = [
    # path('', include(router.urls)),
    path('', views.index, name='index'),
    path('update_from_csv/', views.UpdateFbGroupFromCsv.as_view(), name='update-from-csv'),
    path('groups_update/',  views.FbGroupUpdateOrCreateView.as_view(), name='group-update-list'),
    path('sleep_10/', views.sleep_10, )
]