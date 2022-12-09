"""URL конфигурация проекта

В массиве `urlpatterns` прописаны маршруты на приложения в зависимости от запроса. 
Больше информации можно получить по ссылке:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/

Примеры:
    0. Ипортировать функцию маршрутизации
        from django.urls import path
        
    Использование функций
        1. Импортировать views из нужного приложения:
            from my_app import views
        2. Добавить маршрут в `urlpatterns`: 
            path('', views.home, name='home')
    
    Использование классов
        1. Импортировать класс из views нужного приложения:
            from other_app.views import Home
        2. Добавить маршрут в `urlpatterns`:  
            path('', Home.as_view(), name='home')

    Использование конфигурации URL из приложения
        1. Импортировать функции подключения конфигураций URL:
            from django.urls import include, path
        2. Добавить маршрут в `urlpatterns`:
            path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from . import settings

urlpatterns = [
    path('', include('client.urls')),
    path('server/', include('server.urls')),
    path('debug/', include('debug.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),
]
