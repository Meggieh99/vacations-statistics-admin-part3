from django.urls import path, include
from vacations.api.views.user_view import RegisterView, LoginView
from vacations.api.views.like_view import LikeVacationView, UnlikeVacationView

urlpatterns: list = [
    
    path('register/', RegisterView.as_view(), name='api-user-register'),
    path('login/', LoginView.as_view(), name='api-user-login'),
    
]
