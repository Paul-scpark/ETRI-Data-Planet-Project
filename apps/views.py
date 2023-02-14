from django.shortcuts import render, redirect
import bcrypt, re
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .models import User, Data, DataPlatform

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from .text import message
from django.views import View
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator

import torch
from sentence_transformers import util

import environ
env = environ.Env()
environ.Env.read_env()

import torch
from sentence_transformers import SentenceTransformer, util

# Create your views here.

def main(request):
    if request.method == 'POST':
        ###### (1) 검색바를 통한 데이터 검색
        if request.POST.get("search") != None:
            model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
            des_emb = torch.load("data/title_emb_SBERT.pt")
            search_value = request.POST['search']
            emb = model.encode(search_value)
            distance = util.cos_sim(emb, des_emb)
            sort_distance = distance[0].sort().indices[-11:-1].tolist()

            search_data = []
            [search_data.append(Data.objects.get(pk=i)) for i in sort_distance]
            
            return render(
                request,
                'apps/search_detail.html',
                {
                    'search_value': search_value,
                    'search_data': search_data,
                }
            )
            
        ###### (2) 로그인
        elif request.POST.get('name') == None:
            ### 1. 로그인 페이지에서 기입되는 정보들을 request.POST에 등록
            input_email = request.POST['email']
            input_password = request.POST['password']
            
            ## 모든 칸에 정보가 채워졌는지 확인
            if not (input_email and input_password):
                return HttpResponse(
                    "<script>alert('올바르게 입력해주세요.');"
                    "location.href='/';</script>"
                ) 

            ## DB에 이메일이 존재하는지 확인
            if User.objects.filter(email=input_email).exists():
                user = User.objects.get(email=input_email)
            else:
                return HttpResponse(
                    "<script>alert('존재하지 않는 이메일입니다.');"
                    "location.href='/';</script>"
                )

            ## 이메일 인증 여부를 확인
            if user.is_authenticated == False:
                return HttpResponse(
                    "<script>alert('이메일 인증이 필요합니다.');"
                    "location.href='/';</script>"
                )

            ## 패스워드 일치 여부 확인
            if not bcrypt.checkpw(input_password.encode('utf-8'), user.password.encode('utf-8')):
                return HttpResponse(
                    "<script>alert('비밀번호 불일치!');"
                    "location.href='/';</script>"
                )
            else:
                request.session['user'] = user.name
                request.session['email'] = user.email

            return HttpResponse(
                "<script>alert('로그인 성공.\\n메인 페이지로 돌아갑니다.');"
                "location.href='/';</script>"
            )

        ###### (3) 회원가입
        else:
            ### 1. 회원가입 페이지에서 기입되는 정보들을 request.POST에 등록
            name, email = request.POST.get('name'), request.POST.get('email')
            password = request.POST.get('password')
            password_check = request.POST.get('password_check')
            
            ## 아이디 (이메일) 중복 체크
            if User.objects.filter(email=email).exists():
                return HttpResponse(
                    "<script>alert('이미 존재하는 이메일입니다.\\n회원 가입 페이지로 돌아갑니다.');"
                    "location.href='/';</script>"
                )

            ## 정규표현식으로 아이디 (이메일) 형식 체크
            regex_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(regex_email, email):
                return HttpResponse(
                    "<script>alert('이메일 형식에 일치하지 않습니다.\\n회원 가입 페이지로 돌아갑니다.');"
                    "location.href='/';</script>"
                )

            ## 첫 번째, 두 번째 입력 패스워드가 일치하는지 확인
            if password != password_check:
                return HttpResponse(
                    "<script>alert('비밀번호 불일치!\\n회원 가입 페이지로 돌아갑니다.');"
                    "location.href='/';</script>"
                )

            ### 2. bcrypt를 통해 패스워드르 디코딩해서 DB에 저장하기
            password_encode = password.encode('utf-8')
            password_crypt = bcrypt.hashpw(password_encode, bcrypt.gensalt()).decode('utf-8')

            ### 3. 입력 받은 정보들을 통해서 User를 create 하기
            user = User.objects.create(name=name, email=email, password=password_crypt)

            ### 4. 이메일 인증
            current_site = get_current_site(request)
            domain = current_site.domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            message_data = message(domain, uidb64, token)

            mail_title = "[DataPlanet] 회원가입 이메일 인증을 완료해주세요."
            mail = EmailMessage(mail_title, message_data, to=[email])
            mail.send()

            ### 5. 회원가입 완료 (이메일 인증 후, 로그인 가능)
            return HttpResponse(
                "<script>alert('인증 메일이 발송되었습니다. 메일을 확인해주세요.\\n메인 페이지로 돌아갑니다.');"
                "location.href='/';</script>"
            )
            
    best_view = Data.objects.all().order_by('-view')[:5]
    best_like = Data.objects.all().order_by('-like')[:5]
    
    return render(
        request, 'apps/main.html', {
            'best_view': best_view, 
            'best_like': best_like
        }
    )

def service(request):
    return render(
        request,
        'apps/service.html'
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
    if request.method == "GET":
        return render(request, 'apps/login.html')

    elif request.method == "POST":
        input_email = request.POST['email']
        input_password = request.POST['password']
        
        # 모든 칸 채우기
        if not (input_email and input_password):
            return HttpResponse("<script>alert('올바르게 입력해주세요.'); location.href='/login';</script>")

        # DB에 이메일이 존재하는지 확인
        if User.objects.filter(email=input_email).exists():
            user = User.objects.get(email=input_email)
        else:
            return HttpResponse("<script>alert('존재하지 않는 이메일입니다.'); location.href='/login';</script>")

        if user.is_authenticated == False:
            return HttpResponse("<script>alert('이메일 인증이 필요합니다.'); location.href='/login';</script>")

        # 패스워드 일치 여부 확인
        if not bcrypt.checkpw(input_password.encode('utf-8'), user.password.encode('utf-8')):
            return HttpResponse("<script>alert('비밀번호 불일치!'); location.href='/login';</script>")
        else:
            request.session['user'] = user.name
            request.session['email'] = user.email

        return HttpResponse("<script>alert('로그인 성공.\\n메인 페이지로 돌아갑니다.');"
                            "location.href='/';</script>")

def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
        del(request.session['email'])

    return redirect('/')

def search_category(request):
    pass
    # best_view = Data.objects.all().order_by('-view')[:5]
    # best_like = Data.objects.all().order_by('-like')[:5]
    
    # return render(
    #     request,
    #     'apps/search_category.html',
    #     {
    #         'best_view': best_view,
    #         'best_like': best_like
    #     }
    # )

def search_detail(request):
    if request.method == 'GET':
        data_list = Data.objects.all().order_by('pk')
        paginator = Paginator(data_list, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(
            request,
            'apps/search_detail.html',
            {
                'data': data_list,
                'posts': posts
            }
        )
    elif request.method == 'POST':
        if request.POST.get('page_num'):
            page_num = int(request.POST['page_num'])
            if page_num < 1: page_num = 1
            return redirect(f'/search/detail/?page={page_num}')
        else:
            model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
            des_emb = torch.load("data/title_emb_SBERT.pt")
            search_value = request.POST['search']
            emb = model.encode(search_value)
            distance = util.cos_sim(emb, des_emb)
            sort_distance = distance[0].sort().indices[-11:-1].tolist()

            search_data = []
            [search_data.append(Data.objects.get(pk=i)) for i in sort_distance]

            return render(
                request,
                'apps/search_detail.html',
                {
                    'search_value': search_value,
                    'search_data': search_data,
                }
            )

def data_detail(request, pk):
    data = Data.objects.get(pk=pk)
    data.view = data.view + 1
    data.save()

    # 유사한 데이터 추천
    des_emb = torch.load("data/des_emb_SBERT.pt")
    distance = util.cos_sim(des_emb[pk], des_emb)
    sort_distance = distance[0].sort().indices[-6:-1].tolist()

    recommend = []
    [recommend.append(Data.objects.get(pk=i)) for i in sort_distance]


    return render(
        request,
        'apps/data_detail.html',
        {
            'data': data,
            'recommend': recommend,
        }
    )

def data_detail_distilbert(request, pk):
    data = Data.objects.get(pk=pk)
    data.view = data.view + 1
    data.save()

    # 유사한 데이터 추천
    des_emb = torch.load("data/des_emb_distilBERT.pt")
    distance = util.cos_sim(des_emb[pk], des_emb)
    sort_distance = distance[0].sort().indices[-6:-1].tolist()

    recommend = []
    [recommend.append(Data.objects.get(pk=i)) for i in sort_distance]


    return render(
        request,
        'apps/data_detail.html',
        {
            'data': data,
            'recommend': recommend,
        }
    )

def data_like(request, pk):
    if request.method == 'POST' and request.session.get('user'):
        data = Data.objects.get(pk=pk)
        data.like += 1
        data.save()
        messages.warning(request, "좋아요를 눌렀습니다.")
        return redirect('data_detail', data.pk)

def data_dislike(request, pk):
    if request.method == 'POST' and request.session.get('user'):
        data = Data.objects.get(pk=pk)
        data.like -= 1
        data.save()
        messages.warning(request, "싫어요를 눌렀습니다.")
        return redirect('data_detail', data.pk)


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

def contact(request):
    if request.method == 'POST':
        if not request.session.get('user'):
            return HttpResponse("<script>alert('로그인이 필요한 서비스입니다.');"
                                "location.href='/contact/';</script>")

        email = request.POST['email']
        name = request.POST['name']
        title = request.POST['title']
        content = request.POST['content']

        # 이메일 보내기
        mail_title = f"{name}({email})님의 문의사항: {title}"
        message_data = content
        mail = EmailMessage(mail_title, message_data, to=['project.dataplanet@gmail.com'])
        mail.send()

        return HttpResponse("<script>alert('문의 내역이 전달되었습니다.\\n메인 페이지로 돌아갑니다.');"
                            "location.href='/';</script>")
    else:
        return render(request, 'apps/contact.html')


def signup(request):
    pass
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         password = request.POST['password']
#         password_check = request.POST['password_check']

#         if User.objects.filter(email=email).exists():
#             # return JsonResponse({'message': 'ALREADY_EXISTS'}, status=400)
#             return HttpResponse("<script>alert('이미 존재하는 이메일입니다.\\n회원 가입 페이지로 돌아갑니다.');"
#                                 "location.href='/main';</script>")

#         regex_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
#         if not re.match(regex_email, email):
#             # return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)
#             return HttpResponse("<script>alert('이메일 형식에 일치하지 않습니다.\\n회원 가입 페이지로 돌아갑니다.');"
#                                 "location.href='/main';</script>")

#         if password != password_check:
#             # return JsonResponse({'message': '비밀번호 불일치!'}, status=400)
#             return HttpResponse("<script>alert('비밀번호 불일치!\\n회원 가입 페이지로 돌아갑니다.');"
#                                 "location.href='/main';</script>")

#         password_encode = password.encode('utf-8')
#         password_crypt = bcrypt.hashpw(password_encode, bcrypt.gensalt()).decode('utf-8')

#         user = User.objects.create(name=name, email=email, password=password_crypt)
#         # return JsonResponse({'message': 'SUCCESS!'}, status=201)

#         # 이메일 인증
#         current_site = get_current_site(request)
#         domain = current_site.domain
#         uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#         token = account_activation_token.make_token(user)
#         message_data = message(domain, uidb64, token)

#         mail_title = "[DataPlanet] 회원가입 이메일 인증을 완료해주세요."
#         mail = EmailMessage(mail_title, message_data, to=[email])
#         mail.send()

#         return HttpResponse("<script>alert('인증 메일이 발송되었습니다.메일을 확인해주세요.\\n메인 페이지로 돌아갑니다.');"
#                             "location.href='/';</script>")

#     elif request.method == 'GET':
#         return render(request, 'apps/signup.html')

class activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if account_activation_token.check_token(user, token):
                user.is_authenticated = True
                user.save()
                return HttpResponse("<script>alert('이메일 인증 완료!'); location.href='/';</script>")

            return JsonResponse({"message": "AUTH FAIL"}, status=400)

        except ValidationError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)