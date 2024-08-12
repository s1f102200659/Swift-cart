from django.db import models

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200) # 商品名
    category = models.IntegerField(default=0) # カテゴリー (1:食品, 2:衣類, 3:小物, 4:生活用品, 5:デバイス)
    price = models.IntegerField(default=0) # 値段
    image = models.ImageField(upload_to='img/') # 商品画像
    seller_id = models.IntegerField(default=0) # 出品者ID
    comment = models.TextField(null=True) # 出品者コメント
    buyer_id = models.IntegerField(default=0) # 購入者ID
    review = models.TextField(null=True) # 購入者レビュー
    like = models.IntegerField(default=0) # いいね数

class Like(models.Model):
    product_id = models.IntegerField(default=0) # 商品ID
    user_id = models.IntegerField(default=0) # ユーザーID
    is_liked = models.BooleanField(default=False) #　いいね有無

class Chat(models.Model):
    product_id = models.IntegerField(default=0) # 商品ID
    writter_id = models.IntegerField(default=0) # コメント投稿したユーザーID
    writter_name = models.CharField(max_length=200)# コメント投稿したユーザーネーム
    comment = models.TextField(null=True) # コメント
