from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from news.models import NewsDate 
from django.core.paginator import Paginator
from news.utilits import generate_pagination_urls
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json 
from django.http import JsonResponse,Http404, HttpResponse
import math
import logging

logger = logging.getLogger(__name__)


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

class ApiOpenNews(View):
    def post(self, request, *args, **kwargs):
        news_id = request.POST.get("news_id")

        

class OpenNews(View):
    def get(self, request,*args, **kwargs):
        return render(
                request,
                'not-more-info-news.html', 
            )
    
        data_id = request.GET.get('id')
        data_topic = request.GET.get('topic')
        current_page = request.GET.get('page')
        data_title = request.GET.get('title')
        
        if not data_id:
            raise Http404("ID новости не указан")   

        if title is None :
            pass

        news_object = NewsDate.objects.get(id=data_id)

        if news_object is None:
            logger.warning("объект не найден в бд")

        title = news_object.title
        image_url = news_object.image_url
        main_text = news_object.main_text
        author = news_object.author
        source = news_object.source
        views = news_object.views
        topic = news_object.topic
        created_at = news_object.created_at 

        if news_object is not None:
            return render(
                request,
                'more-information-new.html', 
                context={
                'title' : title,
                'image_url' : image_url,
                'main_text' :main_text,
                'author' : author,
                'source' : source,
                'views' : views,
                'topic' : topic,
                'created_at' : created_at,        
                }
            )
        else:
            return render(
                request,
                'not-more-info-news.html', 
            )

class NewsLikeView(View):
    def post(self, request):
        data = json.loads(request.body)
        news_id = data.get('news_id')
        action = data.get('action')
        
        return JsonResponse({'status': 'success'})

class NewsSaveView(View):
    def post(self, request):
        data = json.loads(request.body)
        news_id = data.get('news_id')
        action = data.get('action')
        
        return JsonResponse({'status': 'success'})

class NewsCommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        news_id = data.get('news_id')
        text = data.get('text')
        
        # Ваша логика комментариев
        return JsonResponse({'status': 'success'})        



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
 
class SearchNews(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        page_number = request.GET.get('page', 1)
        
        if query:
            all_news = NewsDate.objects.filter(
                Q(title__icontains=query) | 
                Q(main_text__icontains=query)
            ).order_by('-created_at')
            
            search_message = f'Результаты поиска для: "{query}"'
        else:
            all_news = NewsDate.objects.all().order_by('-created_at')
            search_message = 'Все новости'
        
        paginator = Paginator(all_news, 15) 
        page_obj = paginator.get_page(page_number)
        
       # pagination_urls = generate_pagination_urls(request, page_obj, paginator.num_pages, query)
        
        return render(
            request,
            'pages-html/searchPage.html',
            context={
                'title': 'Поиск новостей',
                'all_news': page_obj,
                'current_page': page_number,
                'total_pages': paginator.num_pages,
                #'pagination_urls': pagination_urls,
                'search_query': query,
                'search_message': search_message,
                'results_count': len(all_news)
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
    def post(self, request, *args, **kwargs):

        username= request.POST.get('username')
        password =  request.POST.get('password')
        remember_me = request.POST.get('remember')

        user = authenticate(request, username=username,password=password)

        if user is not None:

            login(request, user)

            if remember_me is not None:
                request.session.set_expiry(60*60*24*30)
                messages.success(request, "Вы успешно вошли! Ваша сессия сохранена на 30 дней")
            else:
                request.session.set_expiry(0)
            return redirect('MainPage')
        else:
            return render(
                request,
                'pages-html/signin.html',
                messages.error(request, "Неверное имя или пароль")
            )


class Redistration(View):
    def get(self,request ,*args ,**kwargs):
        return render(
            request,
            'pages-html/login.html',
            context={
                'title': 'Страница регистрации'
                }
        )
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        errors = []
        
        if not username:
            errors.append('Введите username')
        if not email:
            errors.append('Введите email')
        if not password1:
            errors.append('Поле пороля обязательно для заполнения')
        if password1 !=  password2:
            errors.append('Пороли не совпадают')
        if User.objects.filter(email=email):
            errors.append('Пользователь с таким email уже существует')  

        if errors:
            for error in errors:
                messages.error(request,error)
            return render(
                request,
                'pages-html/login.html',
                context={
                    'username': username,
                    'email': email,
                    'password1' : password1,
                    'password2' : password2,
                }
            )
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password2
            ) 

            login(request, user)
            messages.success(request, 'Регистрация прошла успешна!')
            
            return redirect('MainPage')
        except Exception as e:
            messages.error(request, f'Ошибка при регистрации: {str(e)}')
            return render(
                request,
                'pages-html/login.html',
                context={
                    'title': 'Страница регистрации',
                    'email': email,
                    'password1': password1,
                    'password2' : password2,
                }
            )              

class Logout(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('MainPage')

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