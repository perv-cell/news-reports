from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from news.models import NewsDate, SaveNews, LikeNews, VeiwsNews
from django.core.paginator import Paginator
from news.utilits import generate_pagination_urls
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
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

        
@method_decorator(csrf_exempt, name='dispatch')
class OpenNews(View):
    def post(self, request, *args, **kwargs):
        try:
            raw_body = request.body.decode('utf-8')
            
            data = json.loads(request.body)
            
            id = data.get("id")
            topic = data.get("topic")
            page = data.get("page")

            news_object = NewsDate.objects.filter(id=id).first()

            if news_object is None:
                logger.warning(f'Новость с ID {id} не найдена')
                return JsonResponse({'error': 'Статья не найдена'}, status=404)
            
            session_data = {
                'news_id':id,
                'title': news_object.title,
                'image_url': news_object.image_url,
                'main_text': news_object.main_text,
                'author': news_object.author,
                'source': news_object.source,
                'views': news_object.views,
                'topic': news_object.topic,
                'page': page,
            }

            if news_object.created_at:
                session_data['created_at'] = news_object.created_at.isoformat()
            else:
                session_data['created_at'] = None
                           
            request.session['news_card'] = session_data

            redirect_url = reverse('open_news')
            
            response_data = {
                'success': True,
                'redirect_url': redirect_url  
            }
            
            return JsonResponse(response_data)
            
        except json.JSONDecodeError as e:
            logger.error(f'Ошибка парсинга JSON: {e}')
            return JsonResponse({'error': 'Неверный формат данных'}, status=400)
        
        except Exception as e:
            logger.error(f'Неожиданная ошибка: {e}', exc_info=True)
            return JsonResponse({'error': 'Внутренняя ошибка сервера'}, status=500)

class NewsCardOpen(View):
    def get(self, request ,*args, **kwargs):

        news_card = request.session.get('news_card', {})

        if 'news_card' in request.session:

            news = NewsDate.objects.filter(id=news_card.get('news_id',1)).first()            

            likes_count = LikeNews.objects.filter(news=news).all()

            return render(
                request,
                'pages-html/more-information-new.html', 
                context={
                'news_id':news_card.get('news_id',1),   
                'title' : news_card.get('title',"Специальный выпуск"),
                'image_url' : news_card.get('image_url',"К сожалению картинка не сохранилась"),
                'main_text' :news_card.get('main_text',"Новость не найдена"),
                'author' : news_card.get('author',"Автор не орпеделён"),
                'source' : news_card.get('source',"Неизвестный источник"),
                'views' : int(news_card.get('views',0)),
                'topic' : news_card.get('topic',""),
                'created_at' :news_card.get('created_at',"дата публикации неизвестна"),
                'page': news_card.get('page',"/"),
                'likes_count':len(likes_count),
                })
        else:
            return render(
                request,
                'pages-html/not-more-information-news.html'
            )


class NewsLike(View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            news_id = data.get('news_id')
            action = data.get('action')

            news = NewsDate.objects.filter(id=news_id).first()
            if not news:
                return JsonResponse({'status': 'error', 'message': 'News not found'}, status=404)

            if action == 'like':
                logger.debug(f"новость {news_id} лайкнули")
                LikeNews.objects.create(users=request.user, news=news)
            else:
                logger.debug(f"новость {news_id} дизлайкнули")
                LikeNews.objects.filter(users=request.user, news=news).delete()
            
            likes_count = news.like_news.count()
            
            return JsonResponse({
                'status': 'success', 
                'likes_count': likes_count,
                'action': action
            })
            
        except Exception as e:
            logger.error(f"Error in like view: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

class NewsSave(View):
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