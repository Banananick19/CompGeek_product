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
    path('articles', articles_by, name='articles'),
    path('writearticle/', write_article, name='write_article')
]
