from django.shortcuts import render
from django.views import View 


class MainPage(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/main.html',
            context={
                'title': 'Важные новости'
                }
        )

# --------------- новости по датам  ---------------------- 

class FinancNews(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'pages-html/finans-news.html',
            context={
                'title': 'Финансовые новости'
                }
        )


class PopularNews(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'pages-html/popular-news.html',
            context={
                'title': 'Популярные новости'
                }
        )
    
class YestardayNews(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'pages-html/yestarday-news.html',
            context={
                'title': 'Новости за предыдущий день'
                }
        )    
    
class TodayNews(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/today-news.html',
            context={
                'title': 'Главные новости на сегодня'
                }
        )    
 
class SearcNews(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/searchPage.html',
            context={
                'title': 'Поиск новостей'
                }
        )

# --------------- категории ----------------------   

class PoliticalNews(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/political-news.html',
            context={
                'title': 'Политические новости'
                }
        )

class TechnologicalNews(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/technologies.html',
            context={
                'title': 'Новости в области спорта'
                }
        )
    
class SportsNews(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/sports.html',
            context={
                'title': 'Новости о спорте'
                }
        ) 
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