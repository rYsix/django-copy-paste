import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# =============================
# Source Directory Configuration
# =============================

SOURCE_DIR = Path(__file__).resolve().parent.parent   # /source
PROJECT_ROOT = SOURCE_DIR.parent                      # /

load_dotenv(PROJECT_ROOT / ".env")

RUNTIME_DIR = Path(os.getenv("RUNTIME_DIR", PROJECT_ROOT / "runtime"))
LOG_DIR = Path(os.getenv("LOG_DIR", RUNTIME_DIR / "logs"))
os.makedirs(LOG_DIR, exist_ok=True)

# =============================
# Core Settings
# =============================

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# =============================
# Security Settings
# =============================

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# =============================
# Installed Applications
# =============================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# =============================
# Middleware Stack
# =============================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =============================
# URL & WSGI Configuration
# =============================

ROOT_URLCONF = "source_project.urls"
WSGI_APPLICATION = "source_project.wsgi.application"
APPEND_SLASH = True

# =============================
# Templates
# =============================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [SOURCE_DIR / "templates"],
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

# =============================
# Database Configuration
# =============================

DATABASE_MODE = os.getenv("DATABASE_MODE", "sqlite")

if DATABASE_MODE == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": RUNTIME_DIR / "db.sqlite3",
        }
    }
elif DATABASE_MODE == "psql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DATABASE_NAME"),
            "USER": os.getenv("DATABASE_USER"),
            "PASSWORD": os.getenv("DATABASE_PASSWORD"),
            "HOST": os.getenv("DATABASE_HOST", "localhost"),
            "PORT": os.getenv("DATABASE_PORT", "5432"),
        }
    }
else:
    raise ValueError("Invalid DATABASE_MODE: must be 'sqlite' or 'psql'")

# =============================
# Caching
# =============================

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache_table",
        "TIMEOUT": None,
        "OPTIONS": {"MAX_ENTRIES": 10000},
    }
}

# =============================
# Logging
# =============================
# console пишет в stdout → виден в терминале, systemd (journalctl) или docker logs

MAX_LOG_SIZE = 15 * 1024 * 1024
LOG_BACKUPS = 3

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(name)s %(pathname)s:%(lineno)d\n%(message)s",
        },
        "simple": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "error_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "errors.log",
            "formatter": "verbose",
            "maxBytes": MAX_LOG_SIZE,
            "backupCount": LOG_BACKUPS,
            "encoding": "utf-8",
        },
        "info_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "info.log",
            "formatter": "simple",
            "maxBytes": MAX_LOG_SIZE,
            "backupCount": LOG_BACKUPS,
            "encoding": "utf-8",
        },
        "django_console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "debug_mode_console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "filters": ["require_debug_true"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["info_file", "error_file", "django_console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["django_console"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["info_file", "error_file", "debug_mode_console"],
        "level": "DEBUG",
    },
}

# =============================
# Password Validation
# =============================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =============================
# Localization
# =============================

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# =============================
# Email Settings
# =============================

EMAIL_MODE = os.getenv("EMAIL_MODE", "console")

if EMAIL_MODE == "console":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
elif EMAIL_MODE == "smtp":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "true").lower() == "true"
    EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "false").lower() == "true"
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
else:
    raise ValueError("Invalid EMAIL_MODE: must be 'console' or 'smtp'")

# =============================
# Static & Media Files
# =============================

STATIC_URL = "/static/"
STATICFILES_DIRS = [SOURCE_DIR / "static"]
STATIC_ROOT = os.getenv("STATIC_ROOT", RUNTIME_DIR / "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.getenv("MEDIA_ROOT", RUNTIME_DIR / "media")

# =============================
# Miscellaneous
# =============================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =============================
# Startup Summary
# =============================

print(
    "\n[settings] Project loaded with the following configuration:\n"
    f" ├─ DEBUG:            {DEBUG}\n"
    f" ├─ DATABASE_MODE:    {DATABASE_MODE}\n"
    f" ├─ DATABASE_ENGINE:  {DATABASES['default']['ENGINE']}\n"
    f" ├─ EMAIL_MODE:       {EMAIL_MODE}\n"
    f" ├─ STATIC_ROOT:      {STATIC_ROOT}\n"
    f" ├─ MEDIA_ROOT:       {MEDIA_ROOT}\n"
    f" ├─ RUNTIME_DIR:      {RUNTIME_DIR}\n"
    f" ├─ LOG_DIR:          {LOG_DIR}\n"
    f" └─ ALLOWED_HOSTS:    {ALLOWED_HOSTS}\n"
)
