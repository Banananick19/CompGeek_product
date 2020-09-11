from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


from .forms import *


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'main/home.html', {})

def loginer(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                messages.success(request, 'Успешный вход')
                login(request, user)
                return redirect('home')
            else:
                context = {
                    'form': LoginForm(request.POST)
                }
                messages.error(request, 'Неверный логин или пароль')
                return render(request, 'main/login.html', context)
        else:
            context = {
                'form': LoginForm(request.POST)
            }
            messages.error(request, 'Поля заполнены неверно')
            return render(request, 'main/login.html', context)

    if request.method == 'GET':
        context = {
            'form': LoginForm()
        }
        return render(request, 'main/login.html', context)


def logouter(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Вы вышли :<(')
        return redirect('login')
    else:
        messages.error(request, 'Как вы собирались выходить? Вы даже не вошли -_-')
        return redirect('login')

def sing_up(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            try:
                form.clean()
            except:
                context = {
                    'form': form
                }
                messages.error(request, 'Неверно заполнены поля. Проверьте - совпадают ли пароли?')
                return render(request, 'main/sing_up.html', context)
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                messages.success(request, 'Успешный вход')
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Попробуйте войти')
                return redirect('login')
        else:
            context = {
                'form': form
            }
            messages.error(request, 'Неверно заполнены поля. Проверьте - совпадают ли пароли?')
            return render(request, 'main/sing_up.html', context)

    if request.method == 'GET':
        context = {
            'form': RegisterUserForm()
        }
        return render(request, 'main/sing_up.html', context)
