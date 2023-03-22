echo "Let's install django!"
source ../env_dj/bin/activate
pip install -r requirements.txt
cd ..
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
./gunicorn_starter.sh