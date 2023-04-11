# cliche_django
a repository to have a ready-to-deploy django app
fllow these steps to prepare the server:

# HOW TO START
1. enter server
2. create user
    1. `adduser <choose a user name>`           #create the user
    2. `usermod -aG sudo <the user name chosen>`  #modify the provileges of the user
    3. `su <the user name chosen>`                # switch to the user
3. update the server
    1. `sudo apt update`              #update repo
    2. `sudo apt install virtualenv python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl` # install all the packages
4. clone from git 
    `git clone <url to repo>`
5. cd inside the new folder
6. create virtualenv called env_dj 
    `virtualenv env_dj`


# DATABASE
#### create the postgreSQL DB and User DONT FORGET THE SEMICOLON!

'myproject' is the name of the DB
'myprojectuser' is the name of the user that has been created
1.  `sudo -u postgres psql`
2.  `CREATE DATABASE myproject;`  
3.  `CREATE USER myprojectuser WITH PASSWORD 'password';`
4.  `ALTER ROLE myprojectuser SET client_encoding TO 'utf8';`
5.  `ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';`
6.  `ALTER ROLE myprojectuser SET timezone TO 'UTC';`
7.  `GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;`
8. `\q` # close the prompt

#### IN .env (DO NOT USE SPACES)
```
- DATABASE_NAME=myproject
- DATABASE_USER=myprojectuser
- DATABASE_PASS=password
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


### the setting file 
the setting file must be updated with all the django apps we intend to use and added in the urls.py file the new set of urls the application use. also we need to update the allowed hosts to include the ip address of the server and the domain name. so in setting:
0. clone all the apps inside the project
1. update the INSTALLED_APPS list with the apps we use
2. update the ALLOWED_HOSTS to include the ip address of the server and the domain name
### the urls file
in urls.py:
1. include the app urls inside the file

# CALLING THE SCRIPT
now you can call the script inside the script folder
 `sudo ./set_pro_server.sh`
