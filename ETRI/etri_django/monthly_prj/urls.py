"""monthly_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, re_path, path
from app.views import (
    get_data,
    get_data_eda,
    get_data_search,
    get_data_search_result,
    get_data_platform_search,
    get_community,
    get_data_search_detail1,
    get_data_search_detail2,
)

urlpatterns = [
    path("data_schema/", get_data),
    path("data_eda/", get_data_eda),
    path("data_search/", get_data_search),
    path("data_search_result/", get_data_search_result),
    path("data_search_detail1/", get_data_search_detail1),
    path("data_search_detail2/", get_data_search_detail2),
    path("data_platform_search/", get_data_platform_search),
    path("community/", get_community),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^app/", include("app.urls")),
    re_path(r"^", include("app.urls")),
]
