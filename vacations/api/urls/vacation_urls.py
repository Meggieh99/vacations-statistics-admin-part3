from django.urls import path
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
    # Vacation HTML pages
    path('', VacationListPageView.as_view(), name='vacation-list'),
    path('manage/vacations/', AdminVacationListView.as_view(), name='admin-vacation-list'),
    path('manage/vacations/add/', AddVacationPageView.as_view(), name='vacation-add-form'),
    path('manage/vacations/<int:vacation_id>/edit/', EditVacationPageView.as_view(), name='edit-vacation-page'),
    

    # Vacation API endpoints -(fetch/json)
    path('vacations/', VacationListView.as_view(), name='api-vacation-list'),
    path('api/vacations/add/', AddVacationPageView.as_view(), name='vacation-add'),
    path('api/vacations/<int:vacation_id>/edit/', EditVacationView.as_view(), name='vacation-edit-api'),


    path('vacations/<int:vacation_id>/delete/', DeleteVacationView.as_view(), name='vacation-delete'),
    path('vacations/<int:vacation_id>/details/', VacationDetailView.as_view(), name='vacation-detail'),

    # Like / Unlike endpoints (API)
    path('vacations/<int:vacation_id>/like/', LikeVacationView.as_view(), name='vacation-like'),
    path('vacations/<int:vacation_id>/unlike/', UnlikeVacationView.as_view(), name='vacation-unlike'),
]
