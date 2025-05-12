# ============================
# 🔧 Django Logging Settings
# ============================
#
# 1. Logs split into files:
#    - errors.log: WARNING+ (verbose format)
#    - info.log: INFO+ (compact format)
#    - db.log: SQL queries
#
# 2. Log rotation:
#    - Max size: 15 MB
#    - 3 backups kept
#
# 3. Console output:
#    - DEBUG=True: full debug stream
#    - DEBUG=False: only Django INFO
#
# 4. Runtime separation:
#    - All logs in RUNTIME/logs/
#    - Ensures source/runtime separation
#
# ⚠ On Windows, RotatingFileHandler may cause race conditions
# when accessed concurrently. For production, consider
# using a synchronized alternative or switch to WatchedFileHandler on Linux.

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent
RUNTIME_DIR = PROJECT_ROOT / "runtime"
LOG_DIR = RUNTIME_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

MAX_LOG_SIZE = 15 * 1024 * 1024  # 15 MB
LOG_BACKUPS = 3

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(name)s %(pathname)s:%(lineno)d\n%(message)s'
        },
        'simple': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },

    'handlers': {
        'error_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'errors.log',
            'formatter': 'verbose',
            'maxBytes': MAX_LOG_SIZE,
            'backupCount': LOG_BACKUPS,
            'encoding': 'utf-8',
        },
        'info_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'info.log',
            'formatter': 'simple',
            'maxBytes': MAX_LOG_SIZE,
            'backupCount': LOG_BACKUPS,
            'encoding': 'utf-8',
        },
        'django_console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'debug_mode_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['require_debug_true'],
        },
    },

    'loggers': {
        'django': {
            'handlers': ['info_file', 'error_file', 'django_console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django_console'],
            'level': 'INFO',
            'propagate': False,
        },
    },

    'root': {
        'handlers': ['info_file', 'error_file', 'debug_mode_console'],
        'level': 'DEBUG',
    },
}
