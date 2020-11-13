from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser, models.Model):
    cart = models.ManyToManyField("index.Items", related_name = "cart")

class Items(models.Model):
    seller = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "seller")
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 5000)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now = True)
    price = models.IntegerField()
    likes = models.ManyToManyField(User, related_name= "likes")
    image = models.ImageField(upload_to= 'item_image/%Y/%B/%d/')