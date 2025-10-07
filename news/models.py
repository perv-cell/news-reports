from django.db import models

data_from_parser_page = [...]

class NewsDate(models.Model):
    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=500, unique=True)
    image_url = models.CharField(max_length=500, default='', blank=True)
    main_text = models.TextField(blank=True, default='')
    author = models.CharField(max_length=500, default='Неизвестен')
    source = models.CharField(max_length=200, default='mk.ru')
    views = models.IntegerField(default=0)
    topic = models.CharField(max_length=100, default='general')
    save_peaple_id = models.CharField(max_length=100, default='parser')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserNews(models.Model):
    id = models.AutoField(primary_key=True)
    mail = models.CharField(max_length=100)
    password = models.CharField(max_length=500)
    news_ids = models.CharField()

