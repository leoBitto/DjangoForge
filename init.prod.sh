#!/bin/bash

source ./env_dj/bin/activate
cd src
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

python manage.py collectstatic
gunicorn --bind 127.0.0.1:8000 base.wsgi



