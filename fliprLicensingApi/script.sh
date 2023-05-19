#!/bin/sh
python manage.py makemigrations --no-input
python manage.py migrate --no-input --run-syncdb
# python manage.py collectstatic --no-input
python manage.py createsuperuser --no-input --email "rahulranjan25.rr@gmail.com" --name "Rahul R"
# gunicorn fliprLicensingApi.wsgi:application --bind 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000