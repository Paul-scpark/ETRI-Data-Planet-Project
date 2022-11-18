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