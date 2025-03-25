# django-copy-paste
A collection of reusable Django code snippets

logger_conf.py
A simple, no-dependency logging config for Django.
No external libraries, no DB logging handlers — just plain old RotatingFileHandler and some clean separation:
info.log — general info (INFO and above)
errors.log — warnings and errors only
db.log — all SQL queries
Console output only when DEBUG = True
All logs go into a django_logs/ folder (auto-created)
