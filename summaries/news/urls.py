from django.urls import path
from . import views

urlpatterns = [    
    path("", views.MainPage.as_view(), name='MainPage'),
    path('popular-news',views.PopularNews.as_view(), name='popular_news' ),
    path('today-news', views.TodayNews.as_view(), name="today_news"),
    path('yestarday-news', views.YestardayNews.as_view(), name="yestarday_news"),
    path('technological-news', views.TechnologicalNews.as_view(), name='tetechnological_news'),
    path('political-news', views.PoliticalNews.as_view(), name='political_news'),
    path('sports-news', views.SportsNews.as_view(), name='sports_news'),
    path('search-news', views.SearcNews.as_view(), name='search_news'),
    path('save-news', views.SaveNews.as_view(), name='save_news'),
    path('contact', views.Contact.as_view(), name='contact'),
    path('support', views.Support.as_view(), name='support'),
    path('political-conf', views.PoliticalConf.as_view(), name='political_conf'),
    path('signin', views.SignIn.as_view(), name='signin'),
    path('login', views.LogIn.as_view(), name='login'),
    path('finans-news', views.FinancNews.as_view(), name='finans_news')  
]