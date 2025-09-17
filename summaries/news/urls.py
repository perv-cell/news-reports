from django.urls import path
from . import views

urlpatterns = [    
    path("", views.MainPage.as_view(), name='MainPage'),
    path('/popular-news',views.PopularNews.as_view(), name='popular_news' ),
    path('/today-news', views.TodayNews.as_view(), name="today_news"),
    path('/yestarday-news', views.YestardayNews.as_view(), name="yestarday_news"),
    path('/search-news', views.SearcNews.as_view(), name='search_news')
]