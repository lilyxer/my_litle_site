from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from women.views import page_not_found, index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
    path('users/', include('users.urls', namespace='users'))    # users:login/logout - изоляция приложения, чтобы не путать другие login/logout
]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))    # подключаем дебаг панель
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))



handler404 = page_not_found         # if DEBUG = FALSE handler400/403/404/500