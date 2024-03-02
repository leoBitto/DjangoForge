#!/bin/bash

# Questa funzione elimina le immagini precedenti e avvia i container
build_and_start_containers() {
    # Stop tutti i container, incluso i volumi e quelli orfani
    sudo docker-compose down -v --remove-orphans

    # Avvia i container Docker in background e ricrea le immagini se necessario
    sudo docker-compose -f docker-compose.yml up -d --build
    echo "Immagini create"

    # Applica le migrazioni del database all'interno del container "web"
    sudo docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
    echo "Migrazioni eseguite"

    # Raccoglie i file statici all'interno del container "web", cancellando quelli esistenti
    sudo docker-compose -f docker-compose.yml exec web python manage.py collectstatic --noinput --clear
    echo "File statici raccolti"

    # Crea un superuser con le credenziali dalle variabili d'ambiente
    sudo docker-compose -f docker-compose.yml exec web python manage.py createsuperuser 

    echo "Superuser creato"
    echo "Server in esecuzione"
}

# Questa funzione avvia solo i container Docker
start_containers() {
    # Stop tutti i container, incluso i volumi e quelli orfani
    sudo docker-compose down -v --remove-orphans

    # Avvia i container Docker in background 
    sudo docker-compose -f docker-compose.yml up -d 
    echo "Immagini create"

    # Applica le migrazioni del database all'interno del container "web"
    sudo docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
    echo "Migrazioni eseguite"

    # Raccoglie i file statici all'interno del container "web", cancellando quelli esistenti
    sudo docker-compose -f docker-compose.yml exec web python manage.py collectstatic --noinput --clear
    echo "File statici raccolti"

    echo "Server in esecuzione"
}

# Questa funzione ferma i container Docker
stop_containers() {
    # Ferma tutti i container precedenti
    sudo docker-compose down -v --remove-orphans

    echo "Server fermato"
}

# Controlla gli argomenti passati allo script
case "$1" in
    build)
        build_and_start_containers
        ;;
    start)
        start_containers
        ;;
    stop)
        stop_containers
        ;;
    *)
        echo "Utilizzo: $0 {build|start|stop}"
        exit 1
        ;;
esac
