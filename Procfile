web: env PYTHONUNBUFFERED=true python manage.py runserver
worker: env PYTHONUNBUFFERED=true celery worker -A mailme -l DEBUG -E -B
compass: compass watch
