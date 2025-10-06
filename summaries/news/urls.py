from django.urls import path
from . import views

urlpatterns = [    
    path("", views.MainPage.as_view(), name='MainPage'),
    path("<int:news_page>/", views.MainPage.as_view(), name='MainPagePagination'),
    path("api/open/news", views.ApiOpenNews.as_view(), name="api_open_news"),
    path("open-news/",views.OpenNews.as_view(), name='open_news' ),
    path('popular-news',views.PopularNews.as_view(), name='popular_news' ),
    path('popular-news/<int:news_page>',views.PopularNews.as_view(), name='popular_news_index' ),
    path('today-news', views.TodayNews.as_view(), name="today_news"),
    path('today-news/<int:news_page>', views.TodayNews.as_view(), name="today_news_index"),
    path('yestarday-news', views.YestardayNews.as_view(), name="yestarday_news"),
    path('yestarday-news/<int:news_page>', views.YestardayNews.as_view(), name="yestarday_news_index"),
    path('technological-news', views.TechnologicalNews.as_view(), name='tetechnological_news'),
    path('technological-news/<int:news_page>', views.TechnologicalNews.as_view(), name='tetechnological_news_index'),
    path('political-news', views.PoliticalNews.as_view(), name='political_news'),
    path('political-news/<int:news_page>', views.PoliticalNews.as_view(), name='political_news_index'),
    path('sports-news', views.SportsNews.as_view(), name='sports_news'),
    path('sports-news/<int:news_page>', views.SportsNews.as_view(), name='sports_news_index'),
    path('search-news', views.SearchNews.as_view(), name='search_news'),
    path('search-news/<int:news_page>', views.SearchNews.as_view(), name='search_news_index'),
    path('save-news', views.SaveNews.as_view(), name='save_news'),
    path('save-news/<int:news_page>', views.SaveNews.as_view(), name='save_news_index'),
    path('contact', views.Contact.as_view(), name='contact'),
    path('support', views.Support.as_view(), name='support'),
    path('political-conf', views.PoliticalConf.as_view(), name='political_conf'),
    path('signin', views.SignIn.as_view(), name='signin'),
    path('login', views.Redistration.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('finans-news/', views.FinancNews.as_view(), name='finans_news'),
    path('finans-news/<int:news_page>', views.FinancNews.as_view(), name='finans_news_index')    
]