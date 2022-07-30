from django.contrib import admin
from django.urls import path, include
from .views import UserCreate

urlpatterns = [
    path('create/', UserCreate.as_view()),

]
