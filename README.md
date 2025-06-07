# Django Copy-Paste

**IMHO** — удобный и логичный скелет Django-проекта, в котором сразу:

* Чёткое разделение **исходного кода** (`source/`) и **runtime-файлов** (`runtime/`)
* Отдельная директория для **приложений** (`apps/`), что масштабируемо и понятно
* Конфигурация через **.env**, с гибкой поддержкой SQLite и PostgreSQL
* Готовое к работе **логирование**, включая ротацию, вывод в консоль и создание папок
* Без лишнего — ничего лишнего не навязано, но есть возможность расширить

## 📁 Структура проекта

```
django-copy-paste/
├── source/                       # Весь исходный код
│   ├── source_project/           # Основной Django проект
│   │   ├── settings.py           # Настройки проекта
│   │   ├── urls.py               # URL конфигурация
│   │   └── wsgi.py               # WSGI приложение
│   ├── apps/                     # Django приложения
│   ├── templates/                # HTML шаблоны
│   ├── static/                   # Статические файлы (CSS, JS, изображения)
│   └── manage.py                 # Django команды
├── runtime/                      # Runtime файлы (создаются автоматически)
│   ├── logs/                     # Логи приложения
│   ├── media/                    # Файлы пользователей
│   ├── staticfiles/              # Собранные статические файлы
│   └── db.sqlite3                # SQLite база (по умолчанию)
├── .env                          # Переменные окружения (игнорируется git)
├── .env.example                  # Шаблон окружения
├── .gitignore                    # Правила игнорирования git
├── LICENSE                       # MIT лицензия
└── README.md                     # Этот файл
```

## ⚙️ Конфигурация

### Переменные окружения

Гибкая конфигурация проекта через `.env` файл:

```bash
# Основные настройки
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Конфигурация базы данных
DATABASE_MODE=sqlite  # или 'psql' для PostgreSQL
DATABASE_NAME=имя_базы
DATABASE_USER=пользователь_базы
DATABASE_PASSWORD=пароль_базы
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Конфигурация email
EMAIL_MODE=console  # или 'smtp' для продакшена
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=ваш_email@gmail.com
EMAIL_HOST_PASSWORD=ваш_пароль

# Пути к файлам (опционально)
RUNTIME_DIR=/путь/к/runtime
LOG_DIR=/путь/к/логам
STATIC_ROOT=/путь/к/статике
MEDIA_ROOT=/путь/к/медиа
```

### Режимы базы данных

* **SQLite** (по умолчанию): Идеально для разработки
* **PostgreSQL**: Готово к продакшену

### Режимы email

* **Console**: Все письма отображаются в консоли (разработка)
* **SMTP**: Настоящая отправка писем (продакшен)

## 📝 Конфигурация логирования

### Файлы логов

* `runtime/logs/info.log` — обычные события
* `runtime/logs/errors.log` — ошибки и предупреждения

### Особенности:

* Ротация: 15MB + 3 резервных файла
* UTF-8 поддержка
* Вывод в консоль при DEBUG=True
* Автосоздание директорий для логов

### Уровни логов:

* DEBUG / INFO / WARNING / ERROR / CRITICAL

## 🔒 Безопасность по умолчанию

* Content-Type sniffing защита
* Включённый XSS фильтр
* `X-Frame-Options: DENY`
* Безопасные cookies
* CSRF защита
* Поддержка `X-Forwarded-*` заголовков

## 📦 Зависимости по умолчанию

```txt
Django>=4.2,<5.0
python-dotenv>=1.0.0
psycopg2-binary>=2.9.0  # если PostgreSQL
```

## 🧩 Расширение проекта (по желанию)

```bash
# poetry + pre-commit + форматирование
poetry add django python-dotenv
poetry add --group dev ruff black isort pre-commit pytest pytest-django

# Инструменты для dev
poetry add --group dev django-extensions django-debug-toolbar

# Docker
mkdir docker
# Далее: Dockerfile, docker-compose.yml и т.д.
```
