# cliche_django
a repository to have a ready-to-deploy django app
fllow these steps to prepare the server:

# HOW TO START
1. enter server
2. create user
    1. adduser $user_name
    2. usermod -aG sudo $user_name
    3. su $user_name
3. clone from git 
4. execute the server_starter.sh script


#### create the postgreSQL DB and User DONT FORGET THE SEMICOLON!

myproject is the name of folder containing the src, it can be anything but its better to stick to the same name;
myprojectuser is the name of the user that has been created

1.  CREATE DATABASE myproject;  # myproject is the name of the db
2.  CREATE USER myprojectuser WITH PASSWORD 'password'; # myprojectuser is the name of a user inside the sql environment
3.  ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
4.  ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
5.  ALTER ROLE myprojectuser SET timezone TO 'UTC';
6.  GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
7. \q # close the prompt

#### IN .env (DO NOT USE SPACES)

1. DATABASE_NAME=myproject
2. DATABASE_USER=myprojectuser
3. DATABASE_PASS=password

4. also create a new secret key
5. set DEBUG=FALSE

## the django project
the django project is inside the /src folder, in here reside all the code necessary to make the django project work. inside the folder /base there are the basic setting and the .env file.
inside the /src folder, along with the /base folder there will be all the django app
### the setting file 
the setting file must be updated with all the django apps we intend to use and added in the urls.py file the new set of urls the application use. also we need to update the allowed hosts to include the ip address of the server and the domain name. so in setting:
1. update the INSTALLED_APPS list with the apps we use
2. update the ALLOWED_HOSTS to include the ip address of the server and the domain name
### the urls file
in urls.py:
1. include the app urls inside the file


