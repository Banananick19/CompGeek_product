# Generated by Django 3.0.4 on 2020-10-06 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_article_views'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'Статья', 'verbose_name_plural': 'Статьи'},
        ),
        migrations.AlterModelOptions(
            name='primarycategory',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категорий'},
        ),
        migrations.AlterModelOptions(
            name='secondarycategory',
            options={'verbose_name': 'Вторичныя категория', 'verbose_name_plural': 'Вторичные категорий'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Поьзователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AddField(
            model_name='primarycategory',
            name='slug',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='secondarycategory',
            name='slug',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='article',
            name='label',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='article',
            name='primary_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.PrimaryCategory', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='article',
            name='secondary_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.SecondaryCategory', verbose_name='Вторичная категория'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tag',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Тэг'),
        ),
        migrations.AlterField(
            model_name='article',
            name='text',
            field=models.TextField(default='Тут пусто...', verbose_name='Тест'),
        ),
        migrations.AlterField(
            model_name='primarycategory',
            name='label',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='secondarycategory',
            name='label',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Название'),
        ),
    ]
