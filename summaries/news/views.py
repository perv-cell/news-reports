from django.shortcuts import render
from django.views import View 


class MainPage(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/main.html'
        )

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