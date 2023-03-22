#!/bin/bash
echo "Let's install django!"
activate () {
    cd ..
    . $PWD/env_dj/bin/activate
    sudo pip install -r ../requirements.txt
    cd src
    python manage.py makemigrations
    python manage.py migrate
    echo "I have populated the database, now lets create the superuser"
    echo "follow the instructions:"
    python manage.py createsuperuser
    echo "now we gather the static files"
    python manage.py collectstatic
    echo "I'm getting out of the environment"
    deactivate
}
activate

cd ../scripts
./gunicorn_starter.sh