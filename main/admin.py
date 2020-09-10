from django.contrib import admin
from .models import MODELS_FOR_ADMIN
# Register your models here.

for model in MODELS_FOR_ADMIN:
    admin.site.register(model)