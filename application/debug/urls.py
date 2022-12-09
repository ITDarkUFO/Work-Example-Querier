from django.urls import path
from debug import views

urlpatterns = [
    path('', views.page_debug),
    path('api/page', views.api_page),
    path('api/data', views.api_data),
]
