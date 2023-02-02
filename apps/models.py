from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='사용자 이름')
    email = models.EmailField(max_length=128, verbose_name='사용자 이메일')
    password = models.CharField(max_length=300, verbose_name='비밀번호')
    is_admin = models.BooleanField(default=False, verbose_name='관리자')
    create_dt = models.DateField(auto_now_add=True, verbose_name='가입 날짜')
    is_authenticated = models.BooleanField(default=False, verbose_name='이메일 인증 여부')

    class Meta:
        # 테이블 이름 설정
        db_table = 'User'

class DataPlatform(models.Model):
    data_platform_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='플랫폼 이름')
    des = models.CharField(max_length=1024, verbose_name='플랫폼 설명')
    url = models.CharField(max_length=1024, verbose_name='사이트 주소')
    total_num = models.IntegerField(default=0)

    class Meta:
        db_table = 'DataPlatform'

class Data(models.Model):
    data_id = models.AutoField(primary_key=True)
    data_platform = models.ForeignKey("DataPlatform", on_delete=models.CASCADE)
    title = models.CharField(max_length=512 ,verbose_name='데이터 이름')
    des = models.CharField(max_length=10000, verbose_name='데이터 설명')
    url = models.CharField(max_length=1024, verbose_name='데이터 주소')
    type = models.CharField(max_length=64, verbose_name='데이터 타입')
    source = models.CharField(max_length=300, verbose_name='source')
    ori_label = models.CharField(max_length=32, verbose_name='ori_label')
    ori_source = models.CharField(max_length=32, verbose_name='ori_source')
    label = models.CharField(max_length=32, verbose_name='label')
    view = models.IntegerField(default=0)

    class Meta:
        db_table = 'Data'

