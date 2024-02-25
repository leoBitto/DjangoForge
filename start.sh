#!/bin/bash


# Stop all containers, including volumes and orphaned ones
sudo docker-compose down -v --remove-orphans

# Start the docker containers in the background and rebuild if necessary
sudo docker-compose -f docker-compose.yml up -d --build
echo "Images created"

# Apply database migrations within the "web" container
sudo docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
echo "Migrations done"

# Collect static files within the "web" container, clearing existing ones
sudo docker-compose -f docker-compose.yml exec web python manage.py collectstatic --noinput --clear
echo "Statics collected"

# Create a superuser with credentials from environment variables
sudo docker-compose -f docker-compose.yml exec web python manage.py createsuperuser 

echo "Superuser created"
echo "Server is running"
