"""
Django settings for smartquiz_config project.
"""




from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-%(1=7=0^c02s4_=7z_^hu%_6_v4rdtm-8!xpf8x4=03o^p4$rp"

DEBUG = True
ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'accounts.User'

# ================= APPS =================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "accounts",
    "teachers",
    "students",
    "quizzes",
    "analytics",
]

# ================= MIDDLEWARE =================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "smartquiz_config.urls"

# ================= TEMPLATES =================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "smartquiz_config.wsgi.application"

# ================= DATABASE =================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "db.sqlite3"),
    }
}

# ================= PASSWORD VALIDATION =================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ================= INTERNATIONAL =================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ================= STATIC FILES =================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# ================= MEDIA FILES =================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================================
# ✅ EMAIL CONFIGURATION (GMAIL - FINAL WORKING)
# ============================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'yadavamisha547@gmail.com'   # 👉 replace with your Gmail
EMAIL_HOST_PASSWORD = 'htavzlxsmwplbcui'  # 👉 16-char App Password (NO spaces)

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# Password reset expiry
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour

# ================= LOGGING (OPTIONAL) =================
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {'class': 'logging.StreamHandler'},
        },
        'loggers': {
            'django.core.mail': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }