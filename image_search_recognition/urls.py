# image_search_recognition/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('image/', views.image_recognition, name='image_recognition'),
]