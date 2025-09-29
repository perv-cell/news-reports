from django.shortcuts import render
from django.views import View
from django.urls import reverse
from news.models import NewsDate 
from django.core.paginator import Paginator
from news.utilits import generate_pagination_urls
from django.utils import timezone
from datetime import timedelta
import math


class MainPage(View):
    def get(self,request,news_page=None,*args ,**kwargs):
        current_path = request.path
        page_number = news_page or 1
        all_news = NewsDate.objects.all().order_by('-created_at','-views')
        count_news = 15
        paginator = Paginator(all_news,count_news)
        count_page = paginator.count
        page_obj =paginator.get_page(page_number)
        
        pagination_urls = generate_pagination_urls(page_obj, paginator.num_pages)

        return render(
        request,
        'pages-html/main.html',
        context={
            'title': 'Главные новости',
            'all_news':page_obj,
            'current_page': page_number,
            'total_pages':count_page,
            'pagination_urls': pagination_urls,
        })
       

# --------------- новости по датам  ---------------------- 

class FinancNews(View):
    def get(self, request, news_page=None, *args, **kwargs):
        current_path = request.path
        page_number = news_page or 1
        all_news = NewsDate.objects.filter(topic='economics').order_by('-created_at','-views')
        count_news = 15
        paginator = Paginator(all_news,count_news)
        count_page = paginator.count
        page_obj =paginator.get_page(page_number)
        
        pagination_urls = generate_pagination_urls(page_obj, paginator.num_pages,'finans_news', 'finans_news_index')
        return render(
            request,
            'pages-html/finans-news.html',
            context={
            'title': 'Финансовые новости',
            'all_news':page_obj,
            'current_page': page_number,
            'total_pages':count_page,
            'pagination_urls': pagination_urls,
        })    
        

class PopularNews(View):
    def get(self, request, news_page=None, *args, **kwargs):
        page_number = news_page or 1
        all_news = NewsDate.objects.all().order_by('-views','-created_at')
        count_news = 15
        paginator = Paginator(all_news,count_news)
        count_page = paginator.count
        page_obj =paginator.get_page(page_number)
        
        pagination_urls = generate_pagination_urls(page_obj, paginator.num_pages,'popular_news','popular_news_index' )
        return render(
            request,
            'pages-html/popular-news.html',
            context={
            'title': 'Популярные новости',
            'all_news':page_obj,
            'current_page': page_number,
            'total_pages':count_page,
            'pagination_urls': pagination_urls,
        })    
    
class YestardayNews(View):
    def get(self, request, news_page=None, *args, **kwargs):
        page_number = news_page or 1
        yesterday = timezone.now().date() - timedelta(days=1)
        today = timezone.now().date()
        all_news = NewsDate.objects.filter(created_at__date__range=[yesterday,today]).order_by('-created_at')
        count_news = 15
        paginator = Paginator(all_news,count_news)
        count_page = paginator.count
        page_obj =paginator.get_page(page_number)
        
        pagination_urls = generate_pagination_urls(page_obj, paginator.num_pages, 'yestarday_news', 'yestarday_news_index')
        return render(
            request,
            'pages-html/yestarday-news.html',
            context={
            'title': 'Новости за предыдущий день',
            'all_news':page_obj,
            'current_page': page_number,
            'total_pages':count_page,
            'pagination_urls': pagination_urls
        })   
    
class TodayNews(View):
    def get(self, request, news_page=None, *args, **kwargs):
        page_number = news_page or 1
        today = timezone.now().date()
        all_news = NewsDate.objects.filter(created_at__date=today).order_by('-created_at')
        count_news = 15
        paginator = Paginator(all_news,count_news)
        count_page = paginator.count
        page_obj =paginator.get_page(page_number)
        
        pagination_urls = generate_pagination_urls(page_obj, paginator.num_pages, 'today_news','today_news_index')
        return render(
            request,
            'pages-html/today-news.html',
            context={
            'title': 'Новости на сегодня',
            'all_news':page_obj,
            'current_page': page_number,
            'total_pages':count_page,
            'pagination_urls': pagination_urls
        }) 
 
# особая логика   
class SearcNews(View):
    def get(self, request, news_page=None, *args, **kwargs):
        page_number = news_page or 1
        today = timezone.now().date()
        all_news = NewsDate.objects.filter(created_at__date=today).order_by('-created_at')
        count_news = 15
        paginator = Paginator(all_news,count_news)
        count_page = paginator.count
        page_obj =paginator.get_page(page_number)
        
        pagination_urls = generate_pagination_urls(page_obj, paginator.num_pages,'search_news','search_news_index')
        return render(
            request,
            'pages-html/searchPage.html',
            context={
            'title': 'Поиск новостей',
            'all_news':page_obj,
            'current_page': page_number,
            'total_pages':count_page,
            'pagination_urls': pagination_urls
        }) 

# --------------- категории ----------------------   

class PoliticalNews(View):
    def get(self, request, news_page=None, *args, **kwargs):
        page_number = news_page or 1
        all_news = NewsDate.objects.filter(topic='politics').order_by('-created_at','-views')
        count_news = 15
        paginator = Paginator(all_news,count_news)
        count_page = paginator.count
        page_obj =paginator.get_page(page_number)
        
        pagination_urls = generate_pagination_urls(page_obj, paginator.num_pages,'political_news','political_news_index')
        return render(
            request,
            'pages-html/political-news.html',
            context={
            'title': 'Политика',
            'all_news':page_obj,
            'current_page': page_number,
            'total_pages':count_page,
            'pagination_urls': pagination_urls
        })  


# при парсе  ещё одного сайта, добавить topic 
class TechnologicalNews(View):
    def get(self, request, news_page=None, *args, **kwargs):
        page_number = news_page or 1
        all_news = NewsDate.objects.filter(topic='auto').order_by('-created_at','-views')
        count_news = 15
        paginator = Paginator(all_news,count_news)
        count_page = paginator.count
        page_obj =paginator.get_page(page_number)
        
        pagination_urls = generate_pagination_urls(page_obj, paginator.num_pages,'tetechnological_news','tetechnological_news_index')
        return render(
            request,
            'pages-html/technologies.html',
            context={
            'title': 'Новости в области технологий',
            'all_news':page_obj,
            'current_page': page_number,
            'total_pages':count_page,
            'pagination_urls': pagination_urls
        }) 
    
class SportsNews(View):
    def get(self, request, news_page=None, *args, **kwargs):
        page_number = news_page or 1
        all_news = NewsDate.objects.filter(topic='sport').order_by('-created_at','-views')
        count_news = 15
        paginator = Paginator(all_news,count_news)
        count_page = paginator.count
        page_obj =paginator.get_page(page_number)
        
        pagination_urls = generate_pagination_urls(page_obj, paginator.num_pages, 'sports_news','sports_news_index')
        return render(
            request,
            'pages-html/sports.html',
            context={
            'title': 'Новости в области спорта',
            'all_news':page_obj,
            'current_page': page_number,
            'total_pages':count_page,
            'pagination_urls': pagination_urls
        }) 
# --------------- при входи порльзователя при сохранении в избранное ссылки на новости будут сохраняться  ----------------------   
class SaveNews(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/save-news.html',
            context={
                'title': 'Сохранённые новости'
                }
        )
# --------------- для входа ----------------------     
class SignIn(View):
    def get(self,request ,*args ,**kwargs):
        return render(
            request,
            'pages-html/signin.html',
            context={
                'title': 'Страница входа'
                }
            
        )

class LogIn(View):
    def get(self,request ,*args ,**kwargs):
        return render(
            request,
            'pages-html/login.html',
            context={
                'title': 'Страница регистрации'
                }
        )      

# -------------------футер ------------------------
class Contact(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/contact.html',
            context={
                'title': 'Политические новости'
                }
        )  

class Support(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/support.html',
            context={
                'title': 'Политические новости'
                }
        )     
class PoliticalConf(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/political-conf.html',
            context={
                'title': 'Политические новости'
                }
        )                        