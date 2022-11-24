from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='사용자 이름')
    email = models.EmailField(max_length=128, verbose_name='사용자 이메일')
    password = models.CharField(max_length=64, verbose_name='비밀번호')
    is_admin = models.BooleanField(default=False, verbose_name='관리자')
    create_dt = models.DateField(auto_now_add=True, verbose_name='가입 날짜')

    class Meta:
        # 테이블 이름 설정
        db_table = 'User'