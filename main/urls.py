from django.urls import path, include
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('login/', loginer, name='login'),
    path('logout/', logouter, name='logout'),
    path('home/', home, name='home'),
    path('sing_up/', sing_up, name='sing_up'),
    path('article/<str:tag>/', article, name='article'),
    path('home/change/', ChangeUserInfoView.as_view(), name='home_change'),
    path('profile/<str:username>/', profile, name='profile'),
    path('articles', articles_by, name='articles'),
    path('writearticle/', write_article, name='write_article'),
    path('articles/<str:category_tag>/', articles_by_category, name='articles_by_category'),
    path('articles/<str:category_tag>/<str:secondary_category_tag>', articles_by_categories, name='articles_by_categories'),
    path('articles_time/<str:time>', articles_by_views, name='articles_by_views'),
]
