from django.db import models

data_from_parser_page = [...]

class NewsDate(models.Model):
    id = models.AutoField(primary_key=True)  
    views = models.IntegerField()
    img = models.CharField(max_length=500)
    title = models.CharField(max_length=500, unique=True)
    main_text = models.TextField()
    author = models.CharField(max_length=100)
    source = models.CharField(max_length=200)
    topic = models.CharField(max_length=100)
    time_ad = models.CharField(max_length=100)
    save_peaple = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserNews(models.Model):
    id = models.AutoField(primary_key=True)
    mail = models.CharField(max_length=100)
    password = models.CharField(max_length=500)

def save_news_in_db(data_from_parser_page:list):
    news_will_add = [
        NewsDate(
            views = data[0],
            img = data[1],
            title = data[2],
            main_text = data[3],
            author = data[5],
            source = data[4],     
        ) for data in data_from_parser_page
    ]
    NewsDate.objects.bulk_create(news_will_add)
