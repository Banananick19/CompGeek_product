from django.contrib import admin
from .models import *
from .forms import ArticleAdminWriteForm

# Register your models here.

for model in MODELS_FOR_ADMIN:
    if model == Article:
        continue
    admin.site.register(model)


@admin.register(Article)
class PersonAdmin(admin.ModelAdmin):
    form = ArticleAdminWriteForm
