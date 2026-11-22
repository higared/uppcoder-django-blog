"""
Django settings for the blog starter.

Designed for Uppcoder Spark (free plan):
- Database comes from the environment: POSTGRES_* (Uppcoder) or
  DATABASE_URL, otherwise falls back to local SQLite so it always starts.
- HTTPS-proxy settings are already set, otherwise the admin login
  fails with "403 Origin checking failed" behind Uppcoder's proxy.
- No secret / password sits in the code. Set DJANGO_SECRET_KEY
  in the environment before you share the app.
"""
import os
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).lower() in ("1", "true", "yes", "on")


SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "django-insecure-dev-only-change-me-in-production"
)

DEBUG = env_bool("DJANGO_DEBUG", True)

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if h.strip()
]
# Uppcoder gives the app its own HTTPS address; allow it by default
# when the platform tells us the address. Add your own domain here
# if you later bind one.
if os.environ.get("UPPCODER_SELF_URL"):
    _self = urlparse(os.environ["UPPCODER_SELF_URL"])
    if _self.hostname and _self.hostname not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_self.hostname)

# Behind Uppcoder's HTTPS proxy Django receives plain HTTP.
# Without this, Django thinks the request was not HTTPS and the
# admin login fails with "403 Origin checking failed".
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

_csrf = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
if os.environ.get("UPPCODER_SELF_URL") and not _csrf:
    _csrf = os.environ["UPPCODER_SELF_URL"]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf.split(",") if o.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "blog" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"

# --- Database: PostgreSQL on Uppcoder, SQLite locally -----------------
if os.environ.get("POSTGRES_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "postgres"),
            "USER": os.environ.get("POSTGRES_USER", "postgres"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
elif os.environ.get("DATABASE_URL"):
    _u = urlparse(os.environ["DATABASE_URL"])
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": _u.path.lstrip("/"),
            "USER": _u.username or "",
            "PASSWORD": _u.password or "",
            "HOST": _u.hostname or "localhost",
            "PORT": str(_u.port or "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# NOTE: No WhiteNoise here on purpose. Uppcoder's pixi env
# (django + gunicorn + psycopg only) does not install whitenoise,
# and importing it crashes startup with ModuleNotFoundError -> 502.
# Django's default staticfiles storage is enough for this starter.

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
