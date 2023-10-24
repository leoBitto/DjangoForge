# cliche_django
a repository to have a ready-to-deploy django project.
follow these steps to prepare the project :

### `manifest.json`
The `manifest.json` file is essential for turning your project into a Progressive Web App (PWA). It contains information such as the app name, icons, and other configurations. You can find it in the `static` folder.

**Customization Tips:**

- `"name"`: Update this with the name of your app.
- `"short_name"`: Provide a shorter version of your app name for limited space.
- `"start_url"`: Set the starting URL of your app.
- `"icons"`: Replace the default icons with your own. Ensure they have the correct sizes and file paths.

For more details, refer to the [Web App Manifest documentation](https://developer.mozilla.org/en-US/docs/Web/Manifest).

### `service-worker.js`
The `service-worker.js` file handles Service Worker functionalities, such as resource caching. Customize it based on your project's needs. You can find it in the `static` folder.

**Customization Tips:**

- `CACHE_NAME`: This is the name of the cache. You can keep it as is or customize it.
- `urlsToCache`: Add URLs of resources you want to cache for offline access.
- `self.addEventListener('fetch', function(event) {...}`: This section determines how the Service Worker responds to network requests. Customize it if needed.

For more details, refer to the [Service Worker API documentation](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API).


# HOW TO START
## MOUNTING THE PROJECT
before doing all the production steps we need to mount the project in the development
machine, then create the new repo where the project will be launched.

1. clone the cliche_django project from github changing the name of the folder that will contain the project the recursive flag allow to download the submodules
    `git clone --recursive https://github.com/leoBitto/cliche_django.git <name of the new project>`

2. create a new empty repo in github that will contain the entire project

3. change the remote version of the repo we just created in the the dev machine
   ( the cloned cliche ) to the repo we created on github
    `git remote set-url origin <URL of the new repo on github>`

4. finally mount the project: clone all the apps you need inside the project 
   (the src directory) as submodules
    `git submodule add <URL to submodule>`
    


5. the setting file must be updated with all the django apps we intend to use
   and added the new set of urls the application use in the urls.py file. 
   In settings.py:

    1. update the INSTALLED_APPS list with the apps we use
    2. update the ALLOWED_HOSTS to include the ip address of the server and the domain name

   In urls.py:
    1. include the app urls inside the file


## SET TO PRODUCTION
1. enter server
2. update the server
    1. `apt update`              #update repo
    2. `apt upgrade`              #upgrade repo a reboot may be necessary

    2. `apt install virtualenv python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl` # install all the packages
3. create user
    1. `adduser <choose a user name>`           #create the user
    2. `usermod -aG sudo <the user name chosen>`  #modify the provileges of the user
    3. `su <the user name chosen>`                # switch to the user
4. change the directory to the home of the new user
5. clone from git 
    `git clone --recursive <url to repo> <name of the directory you want to put the cloned repo>`
6. cd inside the new folder
7. create virtualenv called env_dj 
    `virtualenv env_dj`


# DATABASE
#### create the postgreSQL DB and User DONT FORGET THE SEMICOLON!

'myproject' is the name of the DB
'myprojectuser' is the name of the user that has been created
1.  `sudo -u postgres psql`
2.  `CREATE DATABASE myproject;`  
3.  `CREATE USER myprojectuser WITH PASSWORD 'password';` # password must be between quotes
4.  `ALTER ROLE myprojectuser SET client_encoding TO 'utf8';`
5.  `ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';`
6.  `ALTER ROLE myprojectuser SET timezone TO 'UTC';`
7.  `GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;`
8. `\q` # close the prompt

#### IN .env (DO NOT USE SPACES)
```
- DATABASE_NAME=myproject
- DATABASE_USER=myprojectuser
- DATABASE_PASS='password'  # password must be between quotes
- SECRET_KEY=also create a new secret key
- DEBUG=FALSE
```

# DJANGO
the django project is inside the /src folder, in here reside all the code necessary to make the django project work. inside the folder /base there are the basic setting and the .env file.
inside the /src folder, along with the /base folder there will be all the django app

from the main folder
1. activate environment
    `source env_dj/bin/activate`
2. install resources in pip from requirements
    `pip install -r requirements.txt`
3. change directory to the /src directory
    `cd /src`

4. manage.py
    1. `python manage.py makemigrations`   # create migrations
    2. `python manage.py migrate`          # effectively migrate
    3. `python manage.py createsuperuser`  # create the superuser
    4. `python manage.py collectstatic`    # gather everythin inside a static folder
5. exit environment
    `deactivate`


 Also we need to update the allowed hosts to include the ip address of the server and the domain name.

### SETTING PERMISSION 
/home/ and all the contained folders MUST be owned by the nginx user www-data


# CALLING THE SCRIPT
now you can call the script inside the script folder
 `sudo ./set_pro_server.sh`

NB you may need to call the scripts inside the apps to make everything work


cliche_django/    # Cartella principale del progetto
├── env_dj/        # Ambiente virtuale
│   ├── ...
├── scripts/       # Script
│   ├── ...
└── src/           # Sorgenti principali dell'applicazione
    ├── base/      # Applicazione principale del progetto
    │   ├── ...
    ├── website/   # Sottomodulo Git 'website'
    │   ├── ...
    └── manage.py  # File di gestione del progetto Django


# using website module
the website module allow you to load images, gather them in galleries, add
contacts and opening hours. to use the module you need to:
1. modify landing page
2. modify navbar and footer with the links of all the pages you want to be accessible
3. modify the view called base, it will call the page landing.html
    add the info in the context you use in the landing. it will be the first page
    seen by the user.
4. modify the favicon in the template base.html
