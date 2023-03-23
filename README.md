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

'myproject' is the name of folder containing the src, it can be anything but its better to stick to the same name;
'myprojectuser' is the name of the user that has been created
7.  `sudo -u postgres psql`
8.  `CREATE DATABASE myproject;`  # myproject is the name of the db
9.  `CREATE USER myprojectuser WITH PASSWORD 'password';` # myprojectuser is the name of a user inside the sql environment, use the 
10.  `ALTER ROLE myprojectuser SET client_encoding TO 'utf8';`
11.  `ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';`
12.  `ALTER ROLE myprojectuser SET timezone TO 'UTC';`
13.  `GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;`
14. `\q` # close the prompt

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
15. activate environment
    `sudo source env_dj/bin/activate`
16. install resources in pip from requirements
    `sudo pip install -r ./requirements.txt`
17. change directory to the /src directory
    `cd /src`
18. manage.py
    1. `sudo python manage.py makemigrations`   # create migrations
    2. `sudo python manage.py migrate`          # effectively migrate
    3. `sudo python manage.py createsuperuser`  # create the superuser
    4. `sudo python manage.py collectstatic`    # gather everythin inside a static folder
19. exit environment
    `deactivate`


### the setting file 
the setting file must be updated with all the django apps we intend to use and added in the urls.py file the new set of urls the application use. also we need to update the allowed hosts to include the ip address of the server and the domain name. so in setting:
1. update the INSTALLED_APPS list with the apps we use
2. update the ALLOWED_HOSTS to include the ip address of the server and the domain name
### the urls file
in urls.py:
1. include the app urls inside the file

# CALLING THE SCRIPT
now you can call the script inside the script folder
 `sudo ./set_pro_server.sh`
