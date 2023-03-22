echo "now NGINX.."
ipADDR=$(curl -s ifconfig.co)
sed -i "s/IP/$ipADDR/" conf.nginx
sed -i "s/USER/$user_name/" conf.nginx
sed -i "s/PROJECTDIR/$(basename $PWD)/" conf.nginx
sudo mv ./conf.nginx /etc/nginx/sites-available/conf.nginx
sudo ln -s /etc/nginx/sites-available/conf.nginx /etc/nginx/sites-enabled
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