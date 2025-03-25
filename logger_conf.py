# Настройки логирования Django:
# 1. Разделение логов:
#    - errors.log (WARNING и выше) - полный формат с трейсами
#    - info.log (INFO и выше) - краткий формат
#    - db.log (SQL запросы) - специальный формат
#
# 2. Ротация логов:
#    - Макс. размер файла: 15MB
#    - Хранится 3 резервных копии
#    - Автосоздание папки django_logs
#
# 3. Консольный вывод:
#    - В DEBUG режиме: все сообщения (DEBUG+)
#    - В production: только INFO сообщения Django
#    - SQL логи НЕ выводятся в консоль
#
# 4. Особенности:
#    - Сохраняет существующие логгеры
#    - Корневой логгер обрабатывает все неотловленные сообщения
#    - UTF-8 кодировка всех лог-файлов

# Настройки логов
LOG_DIR = os.path.join(BASE_DIR, 'django_logs')
os.makedirs(LOG_DIR, exist_ok=True)

# 15 MB на файл, 3 бэкапа - 4 итог
MAX_LOG_SIZE = 15 * 1024 * 1024  
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
        'django_simple': {
            'format': '[%(levelname)s] %(message)s'
        },
        'sql_formatter': {
            'format': '%(asctime)s [SQL] %(message)s'
        },
    },

    'handlers': {
        # Файл ошибок (только WARNING и выше)
        'error_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'errors.log'),
            'formatter': 'verbose',
            'maxBytes': MAX_LOG_SIZE,
            'backupCount': LOG_BACKUPS,
            'encoding': 'utf-8',
        },
        # Основной файловый лог (INFO и выше)
        'info_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'info.log'),
            'formatter': 'simple',
            'maxBytes': MAX_LOG_SIZE,
            'backupCount': LOG_BACKUPS,
            'encoding': 'utf-8',
        },
        # Файл для SQL запросов
        'db_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'db.log'),
            'formatter': 'sql_formatter',
            'maxBytes': MAX_LOG_SIZE,
            'backupCount': LOG_BACKUPS,
            'encoding': 'utf-8',
        },
        # Консоль для Django (только INFO)
        'django_console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django_simple',
        },
        # Консоль для debug (только в DEBUG режиме)
        'debug_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['require_debug_true'],
        },
    },

    'loggers': {
        # Логгер Django по умолчанию
        'django': {
            'handlers': ['info_file', 'error_file', 'django_console'],
            'level': 'INFO',
            'propagate': False,
        },
        # Ошибки запросов
        'django.request': {
            'handlers': ['info_file', 'error_file', 'django_console'],
            'level': 'INFO',
            'propagate': False,
        },
        # SQL запросы (пишем только в файл)
        'django.db.backends': {
            'handlers': ['db_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Логи сервера разработки
        'django.server': {
            'handlers': ['django_console'],
            'level': 'INFO',
            'propagate': False,
        },
    },

    'root': {
        'handlers': ['info_file', 'error_file', 'debug_console'],
        'level': 'DEBUG',
    },
}
