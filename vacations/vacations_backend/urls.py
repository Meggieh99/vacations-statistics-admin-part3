from django.urls import path
from vacations.api.views.register_view import RegisterPageView
from vacations.api.views.login_view import LoginPageView, LoginFormHandlerView, LogoutView
from vacations.api.views.user_view import RegisterView, LoginView
from vacations.api.views.vacation_list_view import VacationListPageView
from vacations.api.views.vacation_api_view import (
    VacationListView,
    AddVacationView,
    EditVacationView,
    DeleteVacationView
)
from vacations.api.views.like_view import LikeVacationView, UnlikeVacationView
from vacations.api.views.vacation_detail_view import VacationDetailView
from vacations.api.views.admin_vacation_view import AdminVacationListView
from vacations.api.views.edit_vacation_view import EditVacationPageView
from vacations.api.views.add_vacation_page_view import AddVacationPageView

urlpatterns = [

    # HTML views
    path('', LoginPageView.as_view(), name='home'),
    path('register/form/', RegisterPageView.as_view(), name='register-form'),
    path('login/form/', LoginPageView.as_view(), name='login-form'),
    path('login/submit/', LoginFormHandlerView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('vacations/', VacationListPageView.as_view(), name='vacation-list'),
    path('manage/vacations/', AdminVacationListView.as_view(), name='admin-vacation-list'),
    path('manage/vacations/add/', AddVacationPageView.as_view(), name='vacation-add-form'),
    path('manage/vacations/<int:vacation_id>/edit/', EditVacationPageView.as_view(), name='edit-vacation-page'),
    path('vacations/<int:vacation_id>/details/', VacationDetailView.as_view(), name='vacation-detail'),

    # API views (user)
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='api-user-login'),

    # API views (vacation)
    path('api/vacations/', VacationListView.as_view(), name='api-vacation-list'),
    path('api/vacations/add/', AddVacationView.as_view(), name='vacation-add'),
    path('api/vacations/<int:vacation_id>/edit/', EditVacationView.as_view(), name='vacation-edit-api'),
    path('vacations/<int:vacation_id>/delete/', DeleteVacationView.as_view(), name='vacation-delete'),

    # API views (like)
  
   path('api/vacations/<int:vacation_id>/like/', LikeVacationView.as_view(), name='vacation-like'),
   path('api/vacations/<int:vacation_id>/unlike/', UnlikeVacationView.as_view(), name='vacation-unlike'),

]
