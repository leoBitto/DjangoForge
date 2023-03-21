#!/bin/bash
source ./env_dj/bin/activate
cd src
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
