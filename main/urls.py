from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', loginer, name='login'),
    path('logout/', logouter, name='logout'),
    path('home/', home, name='home'),
    path('sing_up/', sing_up, name='sing_up')
]
