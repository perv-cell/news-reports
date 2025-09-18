from django.shortcuts import render
from django.views import View 


class MainPage(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/main.html'
        )

# --------------- новости по датам  ---------------------- 

class PopularNews(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'pages-html/popular-news.html'
        )
    
class YestardayNews(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'pages-html/yestarday-news.html'
        )    
    
class TodayNews(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/today-news.html'
        )    
 
class SearcNews(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/searchPage.html'
        )

# --------------- категории ----------------------   

class PoliticalNews(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/political-news.html'
        )

class TechnologicalNews(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/technologies.html'
        )
    
class SportsNews(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/sports.html'
        ) 
# --------------- при входи порльзователя при сохранении в избранное ссылки на новости будут сохраняться  ----------------------   
class SaveNews(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/save-news.html'
        )
# --------------- для входа ----------------------     
class SignIn(View):
    def get(self,request ,*args ,**kwargs):
        return render(
            request,
            'pages-html/signin.html'
        )

class LogIn(View):
    def get(self,request ,*args ,**kwargs):
        return render(
            request,
            'pages-html/login.html'
        )      

# -------------------футер ------------------------
class Contact(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/contact.html'
        )  

class Support(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/support.html'
        )     
class PoliticalConf(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/political-conf.html'
        )                        