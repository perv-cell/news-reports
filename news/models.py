from django.db import models
from django.contrib.auth.models import User
import random

data_from_parser_page = [...]

class NewsDate(models.Model):
    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=500, unique=True)
    image_url = models.CharField(max_length=500, default='', blank=True)
    main_text = models.TextField(blank=True, default='')
    author = models.CharField(max_length=500, default='Неизвестен')
    source = models.CharField(max_length=200, default='mk.ru')
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    topic = models.CharField(max_length=100, default='general')
    save_peaple_id = models.CharField(max_length=100, default='parser')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SaveNews(models.Model):
    id = models.AutoField(primary_key=True)
    news = models.ForeignKey(
        NewsDate,
        on_delete=models.CASCADE,
        related_name='save_news'
    )
    users = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='save_users')
    
class LikeNews(models.Model):
    users = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='like_users')
    news = models.ForeignKey(
        NewsDate,
        on_delete=models.CASCADE,
        related_name='like_news'
    )
    class Meta:
        unique_together = ['users', 'news']

class VeiwsNews(models.Model):
    users = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='view_users')
    news = models.ForeignKey(
        NewsDate,
        on_delete=models.CASCADE,
        related_name='view_news'
    )
    class Meta:
        unique_together = ['users', 'news']

