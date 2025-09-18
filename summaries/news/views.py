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

class SaveNews(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/save-news.html'
        )        