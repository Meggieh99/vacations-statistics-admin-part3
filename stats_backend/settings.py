"""Django settings for statistics backend (Part III)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent

# Extend Python path to include Part B (vacations)
IN_DOCKER = os.environ.get("IN_DOCKER", "0") == "1"
if IN_DOCKER:
    sys.path.append("/app/vacations")
else:
    sys.path.append(r"C:\Project")

# General Django settings
SECRET_KEY: str = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG: bool = os.environ.get("DEBUG", "1") == "1"

# ALLOWED_HOSTS = [
#     "127.0.0.1",
#     "localhost",
#     "backend",  # allow container name inside Docker
# ]

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS: list[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",            # CORS support
    "stats_api",              #  local stats app
    "vacations",   
]

MIDDLEWARE: list[str] = [
    "corsheaders.middleware.CorsMiddleware",     #  should be first or second
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF: str = "stats_backend.urls"
WSGI_APPLICATION: str = "stats_backend.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Import shared DB config from Part B (if exists)
try:
    import db_config  # type: ignore
except Exception:
    db_config = None  # type: ignore

DB_NAME = os.environ.get("DB_NAME") or getattr(db_config, "DB_NAME", "vacation_db")
DB_USER = os.environ.get("DB_USER") or getattr(db_config, "DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD") or getattr(db_config, "DB_PASSWORD", "")
DB_HOST = os.environ.get("DB_HOST") or getattr(db_config, "DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT") or getattr(db_config, "DB_PORT", "5432")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}

# Locale and timezone
LANGUAGE_CODE: str = "en-us"
TIME_ZONE: str = "UTC"
USE_I18N: bool = True
USE_TZ: bool = True

# Static files
STATIC_URL: str = "static/"
STATIC_ROOT: Path = BASE_DIR / "staticfiles"

# Session & CSRF
SESSION_ENGINE: str = "django.contrib.sessions.backends.db"
SESSION_COOKIE_SAMESITE = "Lax"

CSRF_TRUSTED_ORIGINS: list[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# ✅ CORS settings
CORS_ALLOWED_ORIGINS: list[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
