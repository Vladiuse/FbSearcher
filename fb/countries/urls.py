from django.urls import path
from . import views
app_name = 'countries'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:pk>/', views.country, name='country'),
    path('fb_adslib/show_key', views.ShowLibrary.as_view(), name='fb_adslib_show'),
    path('vocabulary/<str:pk>/update', views.CountryLanguageUpdateView.as_view(),name='vocabulary-update'),

    path('country-comment/create/', views.CountryCommentCreateView.as_view(), name='country-comment-create'),
    path('country-comment/<int:pk>/delete/', views.CountryCommentDeleteView.as_view(), name='country-comment-create'),
]