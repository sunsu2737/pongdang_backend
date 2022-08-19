from django.urls import path
from .views import UserCreate, UserLogin,Profile,UploadProfile, FeedUpload, FeedGet





urlpatterns = [
    path('create/', UserCreate.as_view()),
    path('login/', UserLogin.as_view()),
    path('profile/', Profile.as_view()),
    path('profileImage/', UploadProfile.as_view()),
    path('feedImage/', FeedUpload.as_view()),
    path('feed/', FeedGet.as_view()),
]
