from django.urls import path
from client import views

urlpatterns = [
    path('', views.page_home),
    path('home/', views.page_home, name='home'),
    path('login/', views.page_login, name='login'),
    path('logout/', views.page_logout, name='logout'),
    path('docs/', views.page_docs, name='docs')
]
