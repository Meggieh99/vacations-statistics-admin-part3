"""Django settings for statistics backend (Part III)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent

# point Python to Part B so 'vacations' app can be imported
PART_B_ROOT: str = r"C:\Project"
if PART_B_ROOT not in sys.path:
    sys.path.append(PART_B_ROOT)

SECRET_KEY: str = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG: bool = os.environ.get("DEBUG", "1") == "1"
ALLOWED_HOSTS: list[str] = ["127.0.0.1", "localhost"]

INSTALLED_APPS: list[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "vacations",
    "stats_api",
]

MIDDLEWARE: list[str] = [
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

# DB from Part B
try:
    import db_config  # type: ignore
except Exception:
    db_config = None  # type: ignore

DB_NAME = getattr(db_config, "DB_NAME", "vacation_db")
DB_USER = getattr(db_config, "DB_USER", "postgres")
DB_PASSWORD = getattr(db_config, "DB_PASSWORD", "")
DB_HOST = getattr(db_config, "DB_HOST", "localhost")
DB_PORT = getattr(db_config, "DB_PORT", "5432")

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

LANGUAGE_CODE: str = "en-us"
TIME_ZONE: str = "UTC"
USE_I18N: bool = True
USE_TZ: bool = True

STATIC_URL: str = "static/"
STATIC_ROOT: Path = BASE_DIR / "staticfiles"

SESSION_ENGINE: str = "django.contrib.sessions.backends.db"

# Allow React dev server to POST/GET (same host; cookies allowed)
CSRF_TRUSTED_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
SESSION_COOKIE_SAMESITE = "Lax"
