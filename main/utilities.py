from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from functools import wraps
from django.db.models import F
from django.db import transaction
from .models import Article



def get_mean(expression, dictionary):
    for key in dictionary:
        if expression == key:
            return dictionary[key]

def counted(f):
    @wraps(f)
    def decorator(request, *args, **kwargs):
        with transaction.atomic():
            try:
                article = Article.objects.get(tag=kwargs['tag'])
                article.views = F('views') + 1
                article.save()
            except:
                pass
            return f(request, *args, **kwargs)
    return decorator

def transliterate(string):
    # Слоаврь с заменами
    slovar = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
              'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
              'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
              'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
              'ю': 'u', 'я': 'ja', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
              'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
              'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
              'Ц': 'C', 'Ч': 'CZ', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
              'Ю': 'U', 'Я': 'YA', ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
              '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
              ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
              '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
              'Є': 'e', '—': ''}

    # Циклически заменяем все буквы в строке
    for key in slovar:
        string = string.replace(key, slovar[key])
    return string

def get_pag(object_list, n, page):
    paginator = Paginator(object_list, n)
    try:
        object_list = paginator.page(page).object_list
        page = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1).object_list
        page = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(1).object_list
        page = paginator.page(1)
    context = {
        'object_list': object_list,
        'page': page
    }
    return context