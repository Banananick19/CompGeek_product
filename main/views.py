from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.utils import timezone
from CompGeek.settings import PAGINATION_ARTICLES, PAGINATION_COMMENTS


from .forms import *
from .models import *
from .utilities import *


def index(request):
    articles = Article.objects.all()
    page = request.GET.get('page')
    context = get_pag(articles, PAGINATION_ARTICLES, page)
    context['title'] = 'CompGeek'
    return render(request, 'main/articles.html', context)


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'layout/form.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('home')
    success_message = 'Личные данные пользователя изменены'

    def get_context_data(self, **kwargs):
        kwargs['form_title'] = 'Изменение данных пользователя'
        return super().get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def article(request, tag):
    article = get_object_or_404(Article, tag=tag)

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
                    'form': form,
                    'title': article.label
                })
                return render(request, 'main/article.html', context)
    comments = Comment.objects.filter(article=article)
    page = request.GET.get('page')
    context = get_pag(comments, PAGINATION_COMMENTS, page)
    context.update({
        'article': article,
        'form': CommentForm(),
        'title': article.label
    })
    return render(request, 'main/article.html', context)

@login_required
def home(request):
    articles = Article.objects.filter(author=request.user)
    page = request.GET.get('page')
    context = get_pag(articles, PAGINATION_ARTICLES, page)
    context['title'] = request.user.username
    return render(request, 'main/home.html', context)


def loginer(request):
    if request.user.is_authenticated:
        messages.error(request, 'Вы уже вошли')
        return redirect('home')
    context = {
        'form_title': 'Вход'
    }

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
                context['form'] = LoginForm(request.POST)
                messages.error(request, 'Неверный логин или пароль')
                return render(request, 'layout/form.html', context)
        else:
            context['form'] = LoginForm(request.POST)
            messages.error(request, 'Поля заполнены неверно')
            return render(request, 'layout/form.html', context)

    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'layout/form.html', context)

def profile(request, username):
    user = get_object_or_404(User, username=username)
    articles = Article.objects.filter(author=user)
    page = request.GET.get('page')
    context = get_pag(articles, PAGINATION_ARTICLES, page)
    context['profile_user'] = user
    context['title'] = user.username
    return render(request, 'main/profile_user.html', context)

@login_required
def logouter(request):
    logout(request)
    messages.success(request, 'Вы вышли :<(')
    return redirect('login')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')

    context = {
        'form_title': 'Регистрация'
    }
    if request.method == 'POST':
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.clean()
            except:
                context['form'] = form
                messages.error(request, 'Неверно заполнены поля. Проверьте - совпадают ли пароли?')
                return render(request, 'layout/form.html', context)
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
            context['form'] = form
            messages.error(request, 'Неверно заполнены поля. Проверьте - совпадают ли пароли?')
            return render(request, 'layout/form.html', context)

    if request.method == 'GET':
        context['form'] = RegisterUserForm()
        return render(request, 'layout/form.html', context)


def articles_by(request):
    pattern = request.GET.get('pattern')
    articles = []
    if pattern:
        if articles != []:
            articles = articles.filter(
                Q(text__icontains=pattern) | Q(label__icontains=pattern) | Q(tag__icontains=pattern))
        else:
            articles = Article.objects.filter(
                Q(text__icontains=pattern) | Q(label__icontains=pattern) | Q(tag__icontains=pattern))

    if articles:
        page = request.GET.get('page')
        context = get_pag(articles, PAGINATION_ARTICLES, page)
        context['pattern'] = pattern
        context['title'] = pattern
        return render(request, 'main/articles.html', context)
    else:
        context = {
            'articles': [],
            'title': pattern
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
        context['category'] = category
        context['title'] = category.label
        return render(request, 'main/articles.html', context)
    else:
        context = {
            'articles': [],
            'title': category.label
        }
        return render(request, 'main/articles.html', context)

def articles_by_categories(request, category_tag, secondary_category_tag):
    try:
        category = PrimaryCategory.objects.get(tag=category_tag)
        secondary_category = SecondaryCategory.objects.get(tag=secondary_category_tag)
    except:
        response = render(request, 'main/404.html')
        response.status_code = 404
        return response
    articles = Article.objects.filter(primary_category=category, secondary_category=secondary_category)
    if articles:
        page = request.GET.get('page')
        context = get_pag(articles, PAGINATION_ARTICLES, page)
        context['category'] = category
        context['secondary_category'] = secondary_category
        context['title'] = category.label + '->' + secondary_category.label
        return render(request, 'main/articles.html', context)
    else:
        context = {
            'articles': [],
            'title': category.label + '->' + secondary_category.label
        }
        return render(request, 'main/articles.html', context)


@login_required
def write_article(request):

    context = {
        'form_title': 'Написать статью'
    }

    if request.method == 'POST':
        form = ArticleWriteForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Вы успешно создали статью')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            context['form'] = form
            messages.error(request, 'Поля заполенены неверно')
            return render(request, 'layout/form.html', context)
    if request.method == 'GET':
        form = ArticleWriteForm()
        context['form'] = form
        return render(request, 'layout/form.html', context)


#erros handelrs

def error_404(request, *args, **kwargs):
    context = {
        'title': '404',
        'error_message': 'Страница не найдена',
        'error_code': 404
    }
    return render(request, 'layout/error.html', context)

def error_403(request, *args, **kwargs):
    context = {
        'title': '403',
        'error_message': 'Недоступно.',
        'error_code': 403
    }
    return render(request, 'layout/error.html', context)

def error_500(request, *args, **kwargs):
    context = {
        'title': '500',
        'error_message': 'Ошибка сервера.',
        'error_code': 500
    }
    return render(request, 'layout/error.html', context)
