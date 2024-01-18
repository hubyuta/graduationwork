from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator, MinValueValidator ,MaxValueValidator
from django.urls import reverse
from django import forms


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    slug = models.SlugField()
    area = models.CharField(max_length=100, default=None)
    productor = models.CharField(max_length=30, default=None)
    xvalue = models.IntegerField(validators=[MinValueValidator(-10), MaxValueValidator(10)], default=None)
    yvalue = models.IntegerField(validators=[MinValueValidator(-10), MaxValueValidator(10)], default=None)
    description = models.TextField()
    image1 = models.ImageField(upload_to='images')
    image2 = models.ImageField(upload_to='images', default=None)
    image3 = models.ImageField(upload_to='images', default=None)

    def __str__(self):
        return self.title
    
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    def __str__(self):
        return f'{self.item.title}:{self.quantity}'
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True) #注文日
    ordered_date = models.DateTimeField() #注文完了日
    ordered = models.BooleanField(default=False) #注文完了確認フラグ
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total #注文の合計金額
 
    def get_total_quantity(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.quantity
        return total #注文の点数
    
    def __str__(self):
        return self.user.email
    
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

class ContactModel(models.Model):
    name = models.CharField('氏名', max_length=30)
    email = models.EmailField('メールアドレス')
    product_name = models.CharField('商品名', max_length=30)
    subject = models.CharField('件名', max_length=30)
    message = models.CharField('メッセージ', validators=[MinLengthValidator(10)], max_length=500)
    timestamp = models.DateTimeField('投稿日時', auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app:contactcheck', kwargs={'pk': self.pk})
    