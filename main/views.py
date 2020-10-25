from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.utils import timezone
from CompGeek.settings import PAGINATION_ARTICLES, PAGINATION_COMMENTS

from datetime import timedelta

from .forms import *
from .models import *
from .utilities import get_pag, counted


def index(request):
    articles = Article.objects.all()
    page = request.GET.get('page')
    context = get_pag(articles, PAGINATION_ARTICLES, page)
    return render(request, 'main/articles.html', context)


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('home')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

@counted
def article(request, tag):
    try:
        article = Article.objects.get(tag=tag)
    except:
        messages.error(request, 'Мы не нашли эту статью')
        response = render(request, 'main/404.html')
        response.status_code = 404
        return response
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.article = article
                comment.save()
            else:
                comments = Comment.objects.filter(article=article)
                page = request.GET.get('page')
                context = get_pag(comments, 10, page)
                context.update({
                    'article': article,
                    'form': form
                })
                return render(request, 'main/article.html', context)
    comments = Comment.objects.filter(article=article)
    page = request.GET.get('page')
    context = get_pag(comments, PAGINATION_COMMENTS, page)
    context.update({
        'article': article,
        'form': CommentForm()
    })
    return render(request, 'main/article.html', context)


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    articles = Article.objects.filter(author=request.user)
    page = request.GET.get('page')
    context = get_pag(articles, PAGINATION_ARTICLES, page)
    return render(request, 'main/home.html', context)


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

def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        response = render(request, 'main/404.html')
        response.status_code = 404
        return response
    articles = Article.objects.filter(author=user)
    page = request.GET.get('page')
    context = get_pag(articles, PAGINATION_ARTICLES, page)
    context['profile_user'] = user
    return render(request, 'main/profile_user.html', context)

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


def articles_by(request):
    parent_rubric = request.GET.get('parent_category')
    sub_rubric = request.GET.get('sub_caregory')
    pattern = request.GET.get('pattern')
    articles = []

    if parent_rubric:
        articles = Article.objects.filter(primary_category=parent_rubric)
    if sub_rubric:
        if articles != []:
            articles = articles.filter(secondary_category=sub_rubric)
        else:
            articles = Article.objects.filter(secondary_category=sub_rubric)
    if pattern:
        if articles != []:
            articles = articles.filter(
                Q(text__icontains=pattern) | Q(label__icontains=pattern) | Q(tag__icontains=pattern))
        else:
            articles = Article.objects.filter(
                Q(text__icontains=pattern) | Q(label__icontains=pattern) | Q(tag__icontains=pattern))

    if articles:
        articles = articles.values('tag', 'label')
        page = request.GET.get('page')
        context = get_pag(articles, PAGINATION_ARTICLES, page)
        return render(request, 'main/articles.html', context)
    else:
        context = {
            'articles': []
        }
        return render(request, 'main/articles.html', context)

def articles_by_category(request, category_tag):
    try:
        category = PrimaryCategory.objects.get(tag=category_tag)
    except:
        response = render(request, 'main/404.html')
        response.status_code = 404
        return response
    articles = Article.objects.filter(primary_category=category)
    if articles:
        page = request.GET.get('page')
        context = get_pag(articles, PAGINATION_ARTICLES, page)
        return render(request, 'main/articles.html', context)
    else:
        context = {
            'articles': []
        }
        return render(request, 'main/articles.html', context)

def articles_by_categories(request, category_tag, secondary_category_tag):
    try:
        category = PrimaryCategory.objects.get(slug=category_tag)
        secondary_category = SecondaryCategory.objects.get(slug=secondary_category_tag)
    except:
        response = render(request, 'main/404.html')
        response.status_code = 404
        return response
    articles = Article.objects.filter(primary_category=category, secondary_category=secondary_category)
    if articles:
        page = request.GET.get('page')
        context = get_pag(articles, PAGINATION_ARTICLES, page)
        return render(request, 'main/articles.html', context)
    else:
        context = {
            'articles': []
        }
        return render(request, 'main/articles.html', context)

def articles_by_views(request, time):
    if not time in ['week', 'month', 'ever']:
        response = render(request, 'main/404.html')
        response.status_code = 404
        return response
    articles = False
    if time == 'week':
        articles = Article.objects.filter(date__gte=timezone.now() - timedelta(days=7))
    elif time == 'month':
        articles = Article.objects.filter(date__gte=timezone.now() - timedelta(days=30))
    elif time == 'ever':
        articles = Article.objects.all()

    if articles:
        articles.order_by('-views')
        page = request.GET.get('page')
        context = get_pag(articles, PAGINATION_ARTICLES, page)
        return render(request, 'main/articles.html', context)
    else:
        context = {
            'object_list': articles
        }
        return render(request, 'main/articles.html', context)

def write_article(request):
    if not request.user.is_authenticated:
        messages.error('Вы не зашли в аккаунт')
        return redirect('login')
    if request.method == 'POST':
        form = ArticleWriteForm(request.POST)
        form.author = request.user
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно создали статью')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            context = {
                'form': form
            }
            messages.error(request, 'Поля заполенены неверно')
            return render(request, 'main/writearticle.html', context)
    if request.method == 'GET':
        form = ArticleWriteForm()
        context = {
            'form': form
        }
        return render(request, 'main/writearticle.html', context)


#erros handelrs

def error_404(request, exception):
   return render(request, 'main/404.html', {})