#!/bin/bash
echo """this script will allow to set gunicorn and nginx"""
read -p "what is the name of the user you have created? " user_name
echo "Let's start from gunicorn:"
sed -i "s/USER/$user_name/" ./gunicorn/gunicorn.service
sed -i "s/PROJECTDIR/$(basename ${PWD%/*})/" ./gunicorn/gunicorn.service

sudo cp ./gunicorn/gunicorn.socket /etc/systemd/system/
sudo cp ./gunicorn/gunicorn.service /etc/systemd/system/
echo "I'm starting gunicorn socket"
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl daemon-reload
sudo systemctl restart gunicorn

echo "now NGINX:"

ipADDR=$(curl -s ifconfig.co)
sed -i "s/IP/$ipADDR/" ./nginx/conf.nginx
sed -i "s/USER/$user_name/" ./nginx/conf.nginx
sed -i "s/PROJECTDIR/$(basename ${PWD%/*})/" ./nginx/conf.nginx
sudo cp ./nginx/conf.nginx /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/conf.nginx /etc/nginx/sites-enabled/
echo "i'm checking if everything is all right for NGINX"
sudo nginx -t
sudo systemctl restart nginx
echo " Let's fix the firewall"
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
echo "Now for the last checks, press q to exit in every check"
sudo systemctl status gunicorn.socket
sudo systemctl status gunicorn
sudo systemctl status nginx
