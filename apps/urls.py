from django.urls import path
from . import views
# from .views import activate

urlpatterns = [
    path('', views.main),
    path('overview/', views.overview),
    path('overview/platform_info/', views.overview_platform),
    path('overview/eda/', views.overview_eda),
    path('login/', views.login),
    path('logout/', views.logout),
    path('search/category/', views.search_category),
    path('search/detail/', views.search_detail),
    path('search/detail/<int:pk>/', views.data_detail, name='data_detail'),
    path('search/detail/<int:pk>/like/', views.data_like, name='like'),
    path('search/detail/<int:pk>/dislike/', views.data_dislike, name='dislike'),
    path('profile/', views.profile),
    path('community/', views.community),
    path('community/create', views.community_create),
    path('support/', views.support),
    path('signup/', views.signup),
    path('activate/<str:uidb64>/<str:token>', views.activate.as_view()),
]