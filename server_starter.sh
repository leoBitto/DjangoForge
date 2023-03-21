#!/bin/bash
echo """Hello! I'm a script that will allow you 
to install the Django project, let's start from the server."""
echo """you are now logged as root, let's create a new user:"""
read -p "what is the name of the new user? " user_name

adduser $user_name
usermod -aG sudo $user_name

echo "The user has been create and have sudo privileges"
echo "I'm switching to it now.."
su $user_name
echo "switched!"
echo "now let's install what we need,"
echo "most importantly we are installing postgres and nginx"
sudo apt update
sudo apt install python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl
echo "Done!"
echo "now that we have taken care of the server part we can create the database"
echo "from here, i will leave you to the postgres database shell"
echo "refer to the readme and follow the instructions"
sudo -u postgres psql

echo "Welcome back! I hope the installation went well!"
echo "Don't forget to store the information you just used inside the .env file"
echo "you'll find the .env file inside the /base folder."
echo "Let's install django!"
source ./env_dj/bin/activate
cd src
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
echo "I have populated the database, now lets create the superuser"
echo "follow the instructions:"
python manage.py createsuperuser
echo "now we gather the static files"
python manage.py collectstatic
echo "I'm getting out of the environment"
deactivate
echo "I'm going to move some files around:"
if [[ $user_name != "" ]]; then
  sed -i "s/USER/$user_name/" gunicorn.service
fi