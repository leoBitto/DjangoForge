# cliche_django
a repository to have a ready-to-deploy django app
fllow these steps to prepare the server:

## create the postgreSQL DB and User DONT FORGET THE SEMICOLON!

1.  CREATE DATABASE myproject;  # myproject is the name of the db
2.  CREATE USER myprojectuser WITH PASSWORD 'password'; # myprojectuser is the name of a user inside the sql environment
3.  ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
4.  ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
5.  ALTER ROLE myprojectuser SET timezone TO 'UTC';
6.  GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
7. \q # close the prompt

#### REMEMBER TO SET IN .env
1. DATABASE_NAME=myproject
2. DATABASE_USER=myprojectuser
3. DATABASE_PASS=password

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


######
1. enter server
2. pull from git inside folder with the project name
3. follow the script 