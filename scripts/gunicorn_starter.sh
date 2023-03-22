echo "I'm going to move some files around:"
if [[ $user_name != "" ]]; then
  sed -i "s/USER/$user_name/" gunicorn.service
  sed -i "s/PROJECTDIR/$(basename $PWD)/" gunicorn.service
fi
sudo mv ./gunicorn.socket /etc/systemd/system/
sudo mv ./gunicorn.socket /etc/systemd/system/
echo "I'm starting gunicorn socket"
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
./nginx_starter.sh