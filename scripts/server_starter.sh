#!/bin/bash
echo """Hello! I'm a script that will allow you 
to install the Django project, let's start from the server.
Let's install what we need,
most importantly we are installing postgres and nginx"""
apt update
apt install virtualenv python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl

./database_starter.sh






