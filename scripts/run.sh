#!/bin/sh
set -e 

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn -b :80 --chdir /app app.wsgi:application