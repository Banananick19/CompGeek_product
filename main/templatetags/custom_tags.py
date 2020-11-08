from datetime import datetime
import hashlib
import urllib.parse
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# return only the URL of the gravatar
# TEMPLATE USE:  {{ email|gravatar_url:150 }}
@register.filter
def gravatar_url(email, size=40):
    default = "http://banana19.pythonanywhere.com/static/img/site/logo.png"
    return "https://www.gravatar.com/avatar/{}?{}".format(hashlib.md5(email.lower().encode('utf-8')).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))

# return an image tag with the gravatar
# TEMPLATE USE:  {{ email|gravatar:150 }}
@register.filter
def gravatar(email, size=40):
    url = gravatar_url(email, size)
    return mark_safe('<img src="%s" height="%d" width="%d">' % (url, size, size))

