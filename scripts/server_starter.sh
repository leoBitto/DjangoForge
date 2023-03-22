#!/bin/bash
echo """Hello! I'm a script that will allow you 
to install the Django project, let's start from the server."""
echo "Let's install what we need,"
echo "most importantly we are installing postgres and nginx"
apt update
apt install python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl
echo """you are now logged as root, let's create a new user:"""
read -p "what is the name of the new user? " user_name
adduser $user_name
usermod -aG sudo $user_name

echo "The user has been create and have sudo privileges"
echo "I'm switching to it now.."
su $user_name
echo "switched!, now proceed calling the database_started script"
./database_started.sh






