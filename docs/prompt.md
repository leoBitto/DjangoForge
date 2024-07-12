ho in mente un ambizioso progetto, quello di creare un applicativo da proporre ad aziende medio piccole per gestire il proprio business. 
in questo momento sto creando un template che verrà personalizzato in base all azienda cliente. il progetto è strutturato nel seguente modo:
````
.
├── config
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── docs
│   ├── CODE_OF_CONDUCT.md
│   ├── README.md
│   ├── _config.yml
│   └── assets
│       └── img
│           ├── DjangoForge.png
│           ├── DjangoForge_sfondo.png
│           └── djangoforgeico.svg
├── manager.sh
├── nginx
│   ├── nginx.conf
│   └── nginx.dev.conf
└── src
    ├── Dockerfile
    ├── base
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── __init__.cpython-310.pyc
    │   │   └── settings.cpython-310.pyc
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── gold_bi
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    ├── logging_app
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── __init__.cpython-310.pyc
    │   │   ├── admin.cpython-310.pyc
    │   │   ├── apps.cpython-310.pyc
    │   │   └── models.cpython-310.pyc
    │   ├── admin.py
    │   ├── apps.py
    │   ├── docs
    │   │   ├── README.md
    │   │   ├── _config.yml
    │   │   └── assets
    │   │       ├── Immagine 2024-03-19 124951.png
    │   │       └── img
    │   │           └── Immagine 2024-03-19 124951.png
    │   ├── forms.py
    │   ├── middleware.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── templates
    │   │   └── logging_app
    │   │       ├── AElist.html
    │   │       ├── IPlist.html
    │   │       ├── accordion.html
    │   │       ├── consent.html
    │   │       ├── graphs.html
    │   │       └── log_detail.html
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── manage.py
    ├── requirements.txt
    └── website
        ├── __init__.py
        ├── __pycache__
        │   ├── __init__.cpython-310.pyc
        │   ├── admin.cpython-310.pyc
        │   ├── apps.cpython-310.pyc
        │   └── models.cpython-310.pyc
        ├── admin.py
        ├── apps.py
        ├── docs
        │   └── README.md
        ├── forms.py
        ├── migrations
        │   ├── 0001_initial.py
        │   ├── 0002_remove_gallery_image_header.py
        │   ├── 0003_remove_gallery_image_img.py
        │   ├── 0004_gallery_image_img.py
        │   ├── 0005_remove_gallery_image_img.py
        │   ├── 0006_gallery_image_img.py
        │   ├── 0007_carousel_image_delete_gallery_image.py
        │   ├── 0008_rename_carousel_gallery.py
        │   ├── 0009_rename_carousel_image_gallery.py
        │   ├── 0010_alter_gallery_options_alter_image_description_and_more.py
        │   └── __init__.py
        ├── models.py
        ├── static
        │   ├── favicon
        │   │   ├── 16DjangoForge.ico
        │   │   ├── 48DjangoForge.ico
        │   │   └── bee.ico
        │   ├── icons
        │   │   ├── github.svg
        │   │   └── linkedin.svg
        │   └── pwa
        │       └── icons
        │           ├── Icon-512x512.png
        │           └── icon-256x256.png
        ├── templates
        │   ├── registration
        │   │   ├── login.html
        │   │   ├── logout.html
        │   │   └── password_reset.html
        │   └── website
        │       ├── base.html
        │       ├── dashboard
        │       │   ├── contact_page.html
        │       │   ├── create_group.html
        │       │   ├── dashboard.html
        │       │   ├── gallery_page.html
        │       │   ├── group_list.html
        │       │   ├── image_page.html
        │       │   ├── opening_hours_page.html
        │       │   └── push_info.html
        │       ├── footer.html
        │       ├── landing.html
        │       └── navbar.html
        ├── tests.py
        ├── urls.py
        └── views.py
````      

**DJANGO**:
- il progetto django è contenuto in una cartella chiamata src e ha una cartella che si chiama base in cui ci sono i file settings, asgi, wsgi e gli url di base del progetto. 
- all'interno di src ci sono due cartelle che contengono tre distinte app:
-- la prima è website e si occupa della parte grafica del progetto che si potrebbe tradurre in termini di software business nella parte grafica di front office e back office; continene il template base.html, footer.html, header.html e landing.html. tutti i file di tutte le app estendono base.html che è composto da header e footer più altri componenti dati dalle altre app. queste pagine html compongono il front office
nei template c'è una cartella che si chiama dashboard. all'interno di questa cartella invece ci sono i template che compongono il back office, estendnendo sempre base.html qui vengono include delle pagine speciali che permettono le operazioni crud sui modelli, e altre operazioni "speciali" come l'attivazione di azioni.
-- la seconda è logging app. la logging app per adesso va bene, devi solo sapere che esiste. questa app non ha un corrispettivo front office ma solo back office e non permette operazioni crud ma fa solamente visualizzare le operazioni che nginx registra in entrata.
-- la terza si chiama gold_bi e in pratica gestisce dei flussi ETL che permettono di popolare un database chiamato GOLD che contiene dati rifiniti adatti all'analisi. mette a disposizione delle viste che generano delle informazioni da inserire nella parte backoffice della dashboard di controllo dell'applicativo

questa è , per adesso, la base minimale della parte django.

**NGINX**
nginx accetta le connessioni che vengono poi date a gunicorn che le gira a django. nginx viene usato sia in sviluppo, tramite un container docker, che in produzione, direttamente sul server. nginx passa le info all'app logging app.

**DOCKER & docker-compose**

docker viene usato per creare l'app di django. docker compose invece viene suato per orchestrare le varie componenti. esistono due versioni del docker compose:
- la versione sviluppo, crea l'effettiva immagine di django e quella di nginx e di un db postgres. crea il network e dei volumi per i file statici e i media. è il file che viene usato per creare l'effettiva immagine
services:
  web:
    build:
      context: ./src
      dockerfile: Dockerfile
    image: webapp_django
    command: gunicorn base.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 90
    volumes:
      - static_volume:/home/app/web/static
      - media_volume:/home/app/web/media
    expose:
      - 8000
    env_file:
      - ./config/.env
    depends_on:
      - db
      - db_gold
    networks:
      - app_network

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - ./config/.env
    networks:
      - app_network

  db_gold:
    image: postgres:15
    volumes:
      - postgres_data_gold:/var/lib/postgresql/data/
    env_file:
      - ./config/.env
    networks:
      - app_network

  nginx:
    image: nginx:latest
    volumes:
      - static_volume:/home/app/web/static
      - media_volume:/home/app/web/media
      - ./nginx/nginx.dev.conf:/etc/nginx/nginx.conf:ro
    ports:
      - 80:80
    restart: always
    depends_on:
      - web
    networks:
      - app_network


volumes:
  postgres_data:
  postgres_data_gold:
  static_volume:
  media_volume:

networks:
  app_network:
    driver: bridge

- la versione di produzione invece scarica tutte le immagini dai rispettivi register. tranne quello di nginx che come accennato prima in produzione viene fatto girare direttamente sul server. qui la configurazine del network e dei volumi è più avanzata.
services:
  web:
    image: djangoforge:latest # Utilizza l'immagine pre-build presente nel registry
    container_name: web
    command: gunicorn base.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 90
    volumes:
      - static_volume:/home/app/web/static
      - media_volume:/home/app/web/media
    env_file:
      - ./config/.env
    depends_on:
      - db
    ports:
      - 8000:8000
    networks:
      app_network:
        ipv4_address: 192.168.100.2

  db:
    image: postgres:15
    container_name: postgres_db
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - ./config/.env
    networks:
      app_network:
        ipv4_address: 192.168.100.3
  
  db_gold:
    image: postgres:15
    container_name: postgres_db_gold
    volumes:
      - postgres_data_gold:/var/lib/postgresql/data/
    env_file:
      - ./config/.env
    networks:
      app_network:
        ipv4_address: 192.168.100.4

volumes:
  static_volume:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/web/static
  media_volume:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/web/media
  postgres_data:
  postgres_data_gold:


networks:
  app_network:
    driver: bridge
    ipam:
      config:
        - subnet: 192.168.100.0/24



**GITHUB**

github viene usato come strumento di repository per la condivisione del codice tra le macchine in cui viene sviluppato il software, per hostare la docuemntazione e viene usato il ghcr per contenere l'immagine dell'app. ci sono dei flussi CD/CI che vengono usati per automatizzare la creazione dell'immagine e il caricamento su ghcr, e il deploy sul server. il server per adesso è un droplet di digital ocean. per la creazione dell'immagine viene usato docker compose dev mentre nel deploy sul server viene fatto un scp del file docker compose prod e viene fatto partire installando dal ghcr e dal dockerhub le immagini necessarie. 
