# 프로그래머스 인공지능 데브코스 4기 파이널 프로젝트 📌

[프로그래머스 인공지능 데브코스](https://school.programmers.co.kr/learn/courses/16276/16276-5%EA%B8%B0-k-digital-training-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%A8%B8%EC%8A%A4-%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5-%EB%8D%B0%EB%B8%8C-%EC%BD%94%EC%8A%A4)에서 AI와 관련된 다양한 수업들을 수강한 후, 최종 프로젝트를 진행합니다. <br/>
이 프로젝트와 연계하여 [2022 ETRI OPEN API 활용사례 공모전](https://aiopen.etri.re.kr/viewNotice?id=106)에 참여하여 `우수상 (ETRI 원장상)`을 수상했습니다.

---

## ⌨️  코드 실행
- 주로 실행하는 스크립트를 `Makefile`을 통해 편리하게 관리함
- 아래 코드를 통해 환경 셋팅 및 실행에 필요한 스크립트 활용 가능

```
1. make run          # python manage.py runserver
2. make migrations   # python manage.py makemigrations
3. make migrate      # python manage.py migrate
4. make freeze       # pip freeze > requirements.txt
5. make install      # pip install -r requirements.txt
6. make dump         # python manage.py runscript load_data
```

## 🧭  Background
- 현재 검색할 수 있는 데이터 플랫폼 종류는 유형별, 지자체별로 나뉘어져 있음
  - 유형별: 금융, 헬스케어, 소방안전, 환경 빅데이터 플랫폼 등
  - 지자체별: 서울특별시 열린 데이터 광장, 인천광역시 인천데이터 포털, 부산광역시 공공데이터 포털 등
- 위와 같이 데이터가 많고, 서로 흩어져 있기 때문에 필요한 정보를 찾기 힘듦
- 데이터들이 서로 독립적 (관련 및 유사한 데이터들이 연결되어 있지 않음) 이고, 데이터의 질과 양이 부족함
- 즉, 다음과 같은 문제점이 있는 현 상황에서 `사용자들이 더욱 편하게 데이터를 사용할 수 있는 방법에 대한 고민`이 필요함
  - 분산성: 데이터를 제공하는 원천이 많고, 흩어져 있음
  - 독립성: 관련되거나, 유사한 데이터들이 정리되지 않음
  - 비구조화성: 데이터의 형태 (스키마) 등이 통일되어 있지 않음
  
## 🎁  Service
- 흩어진 여러 데이터 플랫폼 속에서 데이터를 수집하고, AI 기술을 통해 사용자의 경험을 개선시키고, 활용도를 증대시키는 서비스
  - 흩어진 데이터를 취합하고, 수집한 데이터들의 스키마를 통일시키기
  - 데이터 사이의 관계를 분석하여 유사한 데이터를 추천하기
  - 데이터의 설명을 기반으로 하여 데이터의 유형 (Label)을 자동으로 분류하기
- 서비스 아키텍쳐 <br/><br/>
![서비스 아키텍쳐](https://github.com/Paul-scpark/Data-planet/blob/main/apps/static/img/architecture.png)
  
## 🖇  Process
- 데이터 수집: 공공데이터 포털, 빅데이터 지도, AI Hub 등 데이터 플랫폼에서 데이터 크롤링
- 데이터 전처리 및 스키마 통일: 수집된 데이터에서 형태소 분리 및 워드 임베딩, 필수적 칼럼 통일시키기
- 데이터 유형 (Label) 분류기 모델 만들기: BERT 모델을 통해 데이터 Label 분류 모델 제작
- 유사 데이터 추천 모델 만들기: 코사인 유사도를 기반으로 유사한 데이터 추천 모델 개발
- 위 기능들을 포함한 웹사이트 형태의 플랫폼 만들기: [부트스트랩](https://themewagon.github.io/hostza/index.html)을 기반으로 웹 프로토타입 제작

## 👨‍👩‍👧‍👦  Makers
- 고은별, 박성찬, 송민석, 이상암, (이지윤, 하영아)

