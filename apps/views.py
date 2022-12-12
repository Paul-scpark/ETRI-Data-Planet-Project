from django.shortcuts import render, redirect

import json, bcrypt, jwt, re

from django.views import View
from django.http import JsonResponse, HttpResponse

from .models import User
import environ
env = environ.Env()
environ.Env.read_env()

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
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password_check = request.POST['password_check']

        if User.objects.filter(email=email) .exists():
            # return JsonResponse({'message': 'ALREADY_EXISTS'}, status=400)
            return HttpResponse("<script>alert('이미 존재하는 이메일입니다.\\n회원 가입 페이지로 돌아갑니다.');"
                                "location.href='/signup';</script>")

        regex_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(regex_email, email):
            # return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)
            return HttpResponse("<script>alert('이메일 형식에 일치하지 않습니다.\\n회원 가입 페이지로 돌아갑니다.');"
                                "location.href='/signup';</script>")

        if password != password_check:
            # return JsonResponse({'message': '비밀번호 불일치!'}, status=400)
            return HttpResponse("<script>alert('비밀번호 불일치!\\n회원 가입 페이지로 돌아갑니다.');"
                                "location.href='/signup';</script>")

        password_encode = password.encode('utf-8')
        password_crypt = bcrypt.hashpw(password_encode, bcrypt.gensalt()).decode('utf-8')

        User.objects.create(name=name, email=email, password=password_crypt)
        # return JsonResponse({'message': 'SUCCESS!'}, status=201)
        return HttpResponse("<script>alert('회원가입 완료.\\n메인 페이지로 돌아갑니다.');"
                            "location.href='/';</script>")

    elif request.method == 'GET':
        return render(request, 'apps/signup.html')