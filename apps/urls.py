from django.urls import path
from . import views
# from .views import activate

urlpatterns = [
    path('', views.main),
    path('service/', views.service),
    path('login/', views.login),
    path('logout/', views.logout),
    path('search/detail/', views.search_detail, name='search_detail'),
    path('search/detail/<int:pk>/', views.data_detail, name='data_detail'),
    path('search/detail/<int:pk>/like/', views.data_like, name='like'),
    path('search/detail/<int:pk>/dislike/', views.data_dislike, name='dislike'),
    path('contact/', views.contact),
    path('signup/', views.signup),
    path('activate/<str:uidb64>/<str:token>', views.activate.as_view()),
]