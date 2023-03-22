#!/bin/bash
echo "I'm going to move some files around:"

sed -i "s/USER/$user_name/" ../gunicorn/gunicorn.service
sed -i "s/PROJECTDIR/$(basename $PWD)/" ../gunicorn/gunicorn.service

sudo cp ../gunicorn/gunicorn.socket /etc/systemd/system/
sudo cp ../gunicorn/gunicorn.service /etc/systemd/system/
echo "I'm starting gunicorn socket"
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
./nginx_starter.sh