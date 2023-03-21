#!/bin/bash
read -p "replace term: " user_name

if [[ $user_name != "" ]]; then
  sed -i "s/USER/$user_name/" gunicorn.service
fi 