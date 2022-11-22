from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def main(request):
    return render(
        request,
        'apps/main.html'
    )

def overview(request):
    return render(
        request,
        'apps/overview.html'
    )

def overview_platform(request):
    return render(
        request,
        'apps/overview_platform.html'
    )

def overview_eda(request):
    return render(
        request,
        'apps/overview_eda.html'
    )

def login(request):
    return render(
        request,
        'apps/login.html'
    )

def search_category(request):
    return render(
        request,
        'apps/search_category.html'
    )

def search_detail(request):
    return render(
        request,
        'apps/search_detail.html'
    )

def profile(request):
    return render(
        request,
        'apps/profile.html'
    )

def community(request):
    return render(
        request,
        'apps/community.html'
    )

def community_create(request):
    return render(
        request,
        'apps/community_create.html'
    )

def support(request):
    return render(
        request,
        'apps/support.html'
    )

def signup(request):
    return render(
        request,
        'apps/signup.html'
    )