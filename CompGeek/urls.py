from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
from django.conf.urls.static import static
from main.views import error_404, error_500, error_403


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

handler404 = error_404
handler403 = error_403
handler500 = error_500


if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>/', never_cache(serve)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)