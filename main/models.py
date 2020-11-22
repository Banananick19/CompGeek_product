from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from CompGeek.settings import MEDIA_ROOT
import os


# Create your models here.



class User(AbstractUser):
    avatar = models.ImageField(blank=True, upload_to='img/avatars', verbose_name='аватар')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class PrimaryCategory(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True, verbose_name='название')
    tag = models.CharField(max_length=100, null=True, blank=True, verbose_name='тэг')

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категорий'



class SecondaryCategory(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True, verbose_name='Название')
    tag = models.CharField(max_length=100, null=True, blank=True, verbose_name='тэг')

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = 'Вторичныя категория'
        verbose_name_plural = 'Вторичные категорий'


class Article(models.Model):
    avatar = models.ImageField(blank=True, upload_to='img/article_avatars', verbose_name='аватар')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Автор')
    label = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='Название')
    tag = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='Тэг')
    text = models.TextField(verbose_name='Тест')
    preview_text = models.CharField(max_length=300, null=True, blank=True, unique=True, verbose_name='Превью текст')
    primary_category = models.ForeignKey('PrimaryCategory', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Категория')
    secondary_category = models.ForeignKey('SecondaryCategory', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Вторичная категория')


    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-date']

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True, verbose_name='статья')
    text = models.TextField(verbose_name='текст')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['date']

# singnals handlers

@receiver(models.signals.pre_delete, sender=User, weak=False)
def delete_related_resources(sender, instance, **kwargs):
    if instance.avatar.name:
        path = os.path.join(MEDIA_ROOT, instance.avatar.name)
        if os.path.exists(path):
            os.remove(path)


