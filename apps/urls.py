from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('overview/', views.overview),
    path('login/', views.login),
    path('search_list', views.search_list),
]