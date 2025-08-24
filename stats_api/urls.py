"""URL routes for Statistics API."""
from __future__ import annotations

from django.urls import path
from . import views

urlpatterns = [
    path("api/login/", views.login_view, name="stats_login"),
    path("api/logout/", views.logout_view, name="stats_logout"),
    path("api/vacations/stats/", views.vacations_stats, name="vacations_stats"),
    path("api/users/total/", views.total_users, name="total_users"),
    path("api/likes/total/", views.total_likes, name="total_likes"),
    path("api/likes/distribution/", views.likes_distribution, name="likes_distribution"),

     #NEW — hydrate auth on page load / refresh:
    path("api/session/", views.session_view, name="session"),

]

