# DjangoForge: User Manual

## Introduction

DjangoForge is a project ready for deployment, based on Django. This manual provides detailed instructions on how to use the automatic procedure of deployment using GitHub Actions.

## Project Setup

### Create a Repository from Template

1. Click on the "Use this template" button on the GitHub repository page.


2. Create a new repository based on the template.

### Clone the New Repository Locally

```bash
git clone --recursive https://github.com/your-username/your-new-repo.git your-new-repo
cd your-new-repo
```

## Project Development

1. Mount or develop new apps for the project: clone all necessary apps inside the project (the `src` directory) as submodules.
   ```bash
   git submodule add <URL to submodule> src/<name of app>
   ```
   
1. Update the setting file with all the Django apps we intend to use and add the new set of URLs the application uses in the `urls.py` file. In `settings.py` update the `INSTALLED_APPS` list with the apps we use.

1. Then `git add`, `git commit`, and `git push`. 

### use the manager.sh
manager.sh is a shell script that can work in a linux machine. it is used to simplify the process of starting the project locally for development
run : `source manager.sh build` to build and start containers
run : `source manager.sh start` to start containers
run : `source manager.sh stop`  to stop containers
run : `source manager.sh destroy` to eliminate containers

the build command is the most used in development:
1. eliminates the containers along with their images; 
1. build them again; 
1. create the migrations for django;
1. run collectstatic;
1. prompt for superuser creation.

after running the command you can find the app running at http://localhost


## Project Deployment 

### Prerequisites:
- A GitHub account
- A DigitalOcean account ( or another server provider )

### Creating a Droplet on DigitalOcean:

1. Log in to your DigitalOcean account.
2. In the dashboard, select "Droplets" from the main menu.
3. Click on "Create Droplet".
4. Configure the Droplet options as desired (distribution, size, datacenter, etc.).
5. Choose "SSH Key" as the authentication method and select or create an SSH key pair.
6. Click on "Create Droplet" to start the creation process.

> [!NOTE]  
> the service Digital Ocean is a suggestion. the project is not bound to be on a droplet.
> this document and the following wiki will refer to digital ocean services since 
> this is the service used by the author at the time of writing this document

> [!TIP] 
> before using the docker implementation it's better to use the full power of Django for debugging purpose
> so start the development server of Django during the first stages of development

#### Creating SSH Keys:

When you create a new Droplet on Digital Ocean, make sure to add the public SSH key to your Github account. This allows you to authenticate securely when GitHub Actions tries to connect to your Droplet. To do so, you need to enter the server as root, create a ssh key pairs:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```
When you’re prompted to “Enter a file in which to save the key,” press Enter. This accepts the default file location.
Just give Enter for the passphrase. Once the SSH key is generated we need to add the key with SSH-agent and start the SSH-agent in the background

```bash
eval "$(ssh-agent -s)"
```
Add your SSH private key to the ssh-agent. If you created your key with a different name, or if you are adding an existing key that has a different name, replace id_ed25519 in the command with the name of your private key file.

```bash
ssh-add ~/.ssh/id_ed25519
```
Before logout from the server we need to copy the SSH key to add in GitHub.

```bash
cat ~/.ssh/id_ed25519.pub
```
> [!TIP] 
> use nano to copy the key in the file autorized_keys

Then select and copy the contents of the id_ed25519 file displayed in the terminal to your clipboard. Add the private SSH key to your GitHub repository as a "Secret." Go to "Settings" -> "Secrets" -> "New repository secret" and add the private SSH key with a meaningful name, DO_SSH_KEY.

The last and final step is to add the SSH ***public*** key to the GitHub account. navigate to the settings -> SSH and GCP keys -> New SSH key add your copied SSH key in key add the same key to the authorized_key file inside the .ssh folder in the server
Once you add the keys our server and GitHub sync is ready to test. 

recap: 
the ***public*** key must be linked in github in the *profile settings* ***and*** in the *autorized_keys file* in the server
the ***private*** key must be a secret in github

### create the secrets on Github
the actions read from the secrets of github, they contain the following information:

1. DEBUG             -> False (DJANGO)
1. SECRET_KEY        -> yousecretkey (DJANGO)
1. POSTGRES_DB       -> the name of the db (POSTGRES)
1. POSTGRES_USER     -> the name of the db user (POSTGRES)
1. POSTGRES_PASSWORD -> the password of the db (POSTGRES)
1. DOMAIN            -> names of the domain (NGINX)

other info used by the droplet and the container registry:

1. DO_SSH_PRIVATE_KEY-> private key from server
1. GHCR_TOKEN        -> token of github
1. HOST              -> droplet address IP 
1. USERNAME          -> root


____________________________________________________________________________________________________________________________________________________


# stuff for the wiki
- folder structure of the project
- what to touch (urls.py,settings.py)
- website
- logging app
- docker
- docker compose
- nginx
- github actions & secrets
- in production
- in development

the deploy consist in various steps. it is automated with github actions that require secrets to work.
the actions are two:
1. build and push
1. deploy

the first action allow to create and image from the repository and upload it on the ghcr connected to the repo
the second will need a digital ocean droplet to connect with, it will upload the docker-compose file 
and create and run the images.

the project is compose of three images: nginx, db and web. 
- nginx is the container of nginx, it serves as a reverse proxy to direct connection to the web container
- web is container that run gunicorn/django is the actual app
- db is the container for postgres

only web is a personalized image. db and nginx are images that come from the dockerhub

the steps taken by the two actions are as follows:
### build and push
1. create two environment variables: REGISTRY and IMAGE_NAME 
   REGISTRY point to the name of the registry: ghcr.io
   IMAGE_NAME point the name of the image it is used primarly to tag the image
1. checkout the repo
1. create the conf file ( more info in the next section )
1. build the web image
1. log in to the container registry
1. tag image
1. push image to the container registry

at this point you should be able to see the image in the section packages of you main GitHub page. it has the name equal to the 
environment variable IMAGE_NAME 

### deploy 
1. checkout the repo
1. enter server and update & upgrade, install docker and docker compose
1. enter server and create conf file
1. enter server and scp docker-compose file and nginx conf
1. enter server and stop old container, start new containers

## CONFIG
the configuration file are basically two:
- one is a generic config file for both django and postgres
- the other is a nginx.conf file to set up nginx and SSL
















## Dockerfile: Step-by-Step Guide

**Important Commands**
To start:
`sudo docker-compose -f docker-compose.yml up -d --build`
`sudo docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput`
`sudo docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear`
To stop:
`sudo docker-compose down -v`

1. **Introduction:**
   This Dockerfile defines a multi-stage build process for a production Django application. It creates an optimized and deployment-ready Docker image.

2. **Builder Stage:**
   - **Base Image:** `python:3.11.4-slim-buster` provides a minimal Python environment.
   - **Working Directory:** `/usr/src/app` is set as the working directory.
   - **Environment Variables:**
     - `PYTHONDONTWRITEBYTECODE=1`: Disables bytecode generation for better performance.
     - `PYTHONUNBUFFERED=1`: Enables unbuffered output for real-time logging.
   - **System Dependencies:** `gcc` is installed for potential compiled dependencies.
   - **Pip Installation:** `pip` is updated and used to install Python dependencies.
   - **Copying Source Code:** The entire project is copied to the builder's working directory.
   - **Wheel Creation:** `pip wheel` is used to create wheel files from dependencies in the build stage, improving efficiency in the final stage.

3. **Final Stage:**
   - **Base Image:** The `python:3.11.4-slim-buster` image is used again.
   - **App User:** A dedicated user `app` is created to run the application.
   - **Application Directory:** Directories are created for the `app` user, static files, media files, and the working directory is set.
   - **Copying Artifacts from Builder:**
     - Pre-built wheel files are copied from the build stage using `COPY --from=builder`.
     - `requirements.txt` is copied for reference.
   - **Installing Dependencies:** `pip install` is used to install dependencies using the pre-built wheel files and `requirements.txt`.
   - **Copying Project:** The entire project source code is copied to the application directory.
   - **Permissions:** Ownership of all files and directories is changed to `app:app`.
   - **Run User:** The user is set to `app` to run the application.
   - **Command:** `gunicorn` is run with specific options.

4. **Notes:**
   - This Dockerfile uses a multi-stage approach to improve efficiency and reduce the size of the final image.
   - The `app` user is used for security purposes and to separate application privileges.
   - The `gunicorn` command is configured with specific options for worker management and timeout.

5. **Usage:**
   To use this Dockerfile:
   1. Build the image: `docker build -t my-django-app .`
   2. Run the container: `docker run -p 8000:8000 my-django-app` (replace `8000` with the desired port number)

6. **Further Resources:**
   - Docker documentation: https://docs.docker.com/
   - Django documentation: https://docs.djangoproject.com/
   - Gunicorn documentation: https://gunicorn.org/

7. **Conclusion:**
   This Dockerfile provides a robust and efficient way to build and deploy a Django application.

## Automated Deployment with Script

### Overview

This script streamlines the deployment process, automating several manual steps, and can be triggered automatically on every push to the main branch of the GitHub repository.

### Deployment Workflow

1. **Checkout Repository:**
   Clones the repository GitHub into the GitHub Actions runner.

2. **Define REPO_NAME:**
   Extracts the repository name and saves it in the `REPO_NAME` variable within GitHub Actions Environment Variables (`$GITHUB_ENV`).

3. **Configure Server:**
  

 Connects to the server configured in secret variables and performs setup tasks.

4. **Clone Repository:**
   Clones the GitHub repository inside the server using the GitHub username and repository name.

5. **Activate Virtual Environment and install dependencies:**
   Creates a Python virtual environment, activates it, and installs project dependencies.

6. **Create .env file:**
   Creates the `.env` file with necessary configurations.

7. **Run Django Commands:**
   Executes Django commands for setup and configuration.

8. **Configure Gunicorn:**
   Configures Gunicorn for serving the Django application.

9. **Configure Nginx:**
   Configures Nginx as a reverse proxy.

10. **Fix Firewall:**
    Adjusts firewall rules to allow traffic.

11. **Final Checks:**
    Restarts services and performs checks to ensure successful deployment.

---

## Module `website`

The `website` module allows you to load images, gather them in galleries, add contacts, and opening hours. To use the module:

1. Modify the landing page.
2. Modify the navbar and footer with the links of all the pages you want to be accessible.
3. Modify the view called "base", it will call the page `landing.html`. Add the info in the context you use in the landing. It will be the first page seen by the user.
4. Modify the favicon and title in the template `base.html`.

### Dashboard

The `website` application has a dashboard part that allows you to perform CRUD operations on graphical objects such as images and galleries...
The dashboard can be the place where all such operations for the other apps should be done.
It can be expanded by creating a dashboard directory inside the templates directory of the new app.

```
app folder
│   ├── ... 
├── templates/        
│   ├── dashboard
└── ...  
```

This allows you to keep the dashboard components inside of the new app separated from the rest.
Inside this directory, there should be a file called `dashboard.html` that expands using include `dashboard.html` inside the website app.

This file should be expanded using the expand statement with templates that show the objects needed.
