"""Project URL configuration for the statistics backend."""
from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path("", include("stats_api.urls")),
    path("api/", include("vacations.api.urls.api_urls")),
    path("vacations/", include("vacations.api.urls.vacation_urls")),
    path("users/", include("vacations.api.urls.user_urls")),
    path("likes/", include("vacations.api.urls.like_urls")),
    
]
