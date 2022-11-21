from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('overview/', views.overview),
    path('login/', views.login),
    path('search_list', views.search_list),
    path('serach_result', views.search_result),
    path('profile', views.profile),
    path('communiy', views.community),
    path('support', views.support),
]