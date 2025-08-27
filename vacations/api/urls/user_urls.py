from django.urls import path
from vacations.api.views.register_view import RegisterPageView
from vacations.api.views.login_view import LoginPageView, LoginFormHandlerView, LogoutView
from vacations.api.views.user_view import RegisterView, LoginView

urlpatterns: list = [
    # API endpoints
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='api-user-login'),

    # HTML form pages
    path('register/form/', RegisterPageView.as_view(), name='register-form'),
    path('login/form/', LoginPageView.as_view(), name='login-form'),
    path('login/submit/', LoginFormHandlerView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    

    # Default route
    path('', LoginPageView.as_view(), name='home'),
]
