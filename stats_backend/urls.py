"""Project URL configuration for the statistics backend."""
from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path("", include("stats_api.urls")),
]
