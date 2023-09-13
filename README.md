# cliche_django
a repository to have a ready-to-deploy django project.
follow these steps to prepare the project and :

# HOW TO START
## MOUNTING THE PROJECT
before doing all the previous steps we need to mount the project in the development
machine, then create the new repo where the project will be launched.

1. clone the cliche_django project from github changing the name of the folder that
   will contain the project
    `git clone https://github.com/leoBitto/cliche_django.git <name of the new project>`

2. create a new empty repo in github that will contain the entire project

3. change the remote version of the repo we just created in the the dev machine
   ( the cloned cliche ) to the repo we created on github
    `git remote set-url <URL of the new repo on github>`

4. finally mount the project: clone all the apps you need inside the project 
   (the src directory) as submodules
    `git submodule add <URL to submodule>`
    4.1. clone the website submodule inside the project
   `git submodule add https://github.com/leoBitto/website.git src/website`


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






