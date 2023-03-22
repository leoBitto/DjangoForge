echo "now NGINX.."
ipADDR=$(curl -s ifconfig.co)
sed -i "s/IP/$ipADDR/" ../nginx/conf.nginx
sed -i "s/USER/$user_name/" ../nginx/conf.nginx
sed -i "s/PROJECTDIR/$(basename $PWD)/" ../nginx/conf.nginx
sudo mv ../nginx/conf.nginx /etc/nginx/sites-available/
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