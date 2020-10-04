from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    pass

    class Meta:
        verbose_name = 'Поьзователь'
        verbose_name_plural = 'Пользователи'


class PrimaryCategory(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True, verbose_name='')

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категорий'



class SecondaryCategory(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True, verbose_name='Название')

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = 'Вторичныя категория'
        verbose_name_plural = 'Вторичные категорий'


class Article(models.Model):
    author = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Автор')
    label = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='Название')
    tag = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='Тэг')
    text = models.TextField(default='Тут пусто...', verbose_name='Тест')
    primary_category = models.ForeignKey('PrimaryCategory', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Категория')
    secondary_category = models.ForeignKey('SecondaryCategory', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Вторичная категория')


    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

MODELS_FOR_ADMIN = [User, PrimaryCategory, SecondaryCategory, Article]
