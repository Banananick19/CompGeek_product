from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    pass


class PrimaryCategory(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.label)


class SecondaryCategory(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.label)


class Article(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField(default='Тут пусто...')
    primary_category = models.ForeignKey('PrimaryCategory', on_delete=models.PROTECT, null=True, blank=True)
    secondary_category = models.ForeignKey('SecondaryCategory', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return str(self.label)


MODELS_FOR_ADMIN = [User, PrimaryCategory, SecondaryCategory, Article]
