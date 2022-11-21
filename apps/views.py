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

def login(request):
    return render(
        request,
        'apps/login.html'
    )

def search_list(request):
    return render(
        request,
        'apps/search_list'
    )

def search_result(request):
    return render(
        request,
        'apps/serach_result'
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

def support(request):
    return render(
        request,
        'apps/support.html'
    )