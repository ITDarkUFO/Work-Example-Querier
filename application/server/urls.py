from django.urls import path

from server import views

urlpatterns = [
	path('api/page/', views.api_page),
    path('api/data/', views.api_data)
]
