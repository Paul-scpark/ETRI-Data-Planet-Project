from django.shortcuts import render
from django.http import HttpResponse

import bcrypt
from .models import User

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
    if request.method == "GET":
        return render(request, 'apps/signup.html')
    
    elif request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['rePassword']
        
        ### 1. 회원가입 과정에서 이상 여부 확인
        ## 이메일 중복 확인
        if User.objects.filter(email=email).exists():
            return HttpResponse(
                "<script>alert('이미 존재하는 이메일입니다.\\n회원 가입 페이지로 돌아갑니다.');"
                "location.href='/signup';</script>"
            )
        
        ## 패스워드 일치 여부 확인
        if password != re_password:
            return HttpResponse(
                "<script>alert('비밀번호 불일치!\\n회원 가입 페이지로 돌아갑니다.');"
                "location.href='/signup';</script>"
            )
        
        ### 2. 패스워드 해쉬 처리
        password = password.encode('utf8')
        password_bcrypt = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf8')
        
        ### 3. 위 로직에서 특이사항 없었으면, DB에 데이터 적재
        User.objects.create(name=name, email=email, password=password_bcrypt).save()
        return HttpResponse(
            "<script>alert('회원가입 완료.\\n메인 페이지로 돌아갑니다.');"
            "location.href='/';</script>"
        )