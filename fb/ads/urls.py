from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register('group_list', views.FbGroupMAssCreateView, basename='group-list')


urlpatterns = [
    # path('', include(router.urls)),
    path('', views.index, name='index'),
    path('update_from_csv/', views.UpdateFbGroupFromCsv.as_view(), name='update-from-csv'),
    path('update_from_zip/', views.UpdateFbGroupFromZip.as_view(), name='update-from-zip'),
    path('groups_update/',  views.FbGroupUpdateOrCreateView.as_view(), name='group-update-list'),
    path('groups_stat/', views.groups_stat, name='groups_stat'),
    path('mark_mail_services/', views.mark_mail_services, name='mark_mail_services'),
    path('download_page/', views.download_page, name='download_page'),
    path('key_words/', views.key_words, name='key_words'),
    path('load_actual_mails/', views.load_actual_mails, name='load_actual_mails'),
    path('sleep_10/', views.sleep_10, )
]