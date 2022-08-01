from django.urls import path
from .views import UserCreate, UserLogin,Profile





urlpatterns = [
    path('create/', UserCreate.as_view()),
    path('login/', UserLogin.as_view()),
    path('profile/', Profile.as_view()),
]
