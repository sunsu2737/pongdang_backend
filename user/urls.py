from django.urls import path
from .views import UserCreate, UserLogin





urlpatterns = [
    path('create/', UserCreate.as_view()),
    path('login/', UserLogin.as_view()),
    
]
