from django.contrib import admin
from .models import *
from .forms import ArticleAdminWriteForm, CommentAdminForm

def comment_author_username(obj):
    return obj.author.username

# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ['date']
    list_filter = ('author__is_staff',)
    list_display = ('label', 'tag', 'preview_text', 'date')
    search_fields = ('author__username', 'text', 'date', 'label', 'tag', 'preview_text',)
    form = ArticleAdminWriteForm

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (comment_author_username, 'date',)
    search_fields = ('author__username', 'text', 'date')
    readonly_fields = ['date']
    form = CommentAdminForm

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff',)

@admin.register(PrimaryCategory)
class PrimaryCategoryAdmin(admin.ModelAdmin):
    list_display = ('label', 'tag')
    search_fields = ('label', 'tag')


@admin.register(SecondaryCategory)
class SecondaryCategoryAdmin(admin.ModelAdmin):
    list_display = ('label', 'tag')
    search_fields = ('label', 'tag')

