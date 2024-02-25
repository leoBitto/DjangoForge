#!/bin/bash

#stop every previous container
sudo docker-compose down -v --remove-orphans

echo "server stopped"
