echo "Let's install django!"
sudo . ../env_dj/bin/activate
sudo pip install -r requirements.txt
cd ..
cd src
sudo python manage.py makemigrations
sudo python manage.py migrate
echo "I have populated the database, now lets create the superuser"
echo "follow the instructions:"
sudo python manage.py createsuperuser
echo "now we gather the static files"
sudo python manage.py collectstatic
echo "I'm getting out of the environment"
sudo deactivate
cd ../scripts
./gunicorn_starter.sh