from django.db import models

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=200) # ユーザーネーム
    password = models.CharField(max_length=200) # パスワード
    full_name = models.CharField(max_length=200) # 氏名
    birth = models.IntegerField(default=0) # 生年月日
    address = models.CharField(max_length=200) # 住所
    post = models.CharField(max_length=200) # 郵便番号
    tel = models.CharField(max_length=200) # 携帯番号
    mail = models.EmailField(max_length=200) # メールアドレス
    points = models.IntegerField(default=0) # ポイント残高
