# DjangoForge: User Manual

## Introduction

DjangoForge is a project ready for deployment, based on Django. This manual provides detailed instructions on how to use the project and automate the deployment process using GitHub Actions.

## Project Setup

### 1. Create a Repository from Template

1. Click on the "Use this template" button on the GitHub repository page.
2. Create a new repository based on the template.

### 2. Clone the New Repository Locally

```bash
git clone --recursive https://github.com/your-username/your-new-repo.git
cd your-new-repo
```

## Project Development

1. Mount or develop new apps for the project: clone all necessary apps inside the project (the `src` directory) as submodules.
   ```bash
   git submodule add <URL to submodule> src/<name of app>
   ```
   Then `git add`, `git commit`, and push.

2. Update the setting file with all the Django apps we intend to use and add the new set of URLs the application uses in the `urls.py` file. In `settings.py` update the `INSTALLED_APPS` list with the apps we use.

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


# SET TO PRODUCTION

#### Automated Server Setup with Deployment Script

## Overview

This guide explains how to use the provided deployment script to set up a server for the DjangoForge project. The script automates various steps involved in server setup, application deployment, and database configuration.
Digital Ocean provides a feature called Droplets. Droplets are scalable compute platforms with add-on storage, where your applications can be deployed. In the script, there might be references to Digital Ocean-specific details like IP addresses, server configurations, etc. Before using the script we need to grant access to Digital Ocean to Github. To do so we need to access the remote server, so after creating the droplet we access it with root
NB the access from your computer to the server may be using a ssh key, that has nothing to do with the key we are creating with the following procedure:

## Public SSH Key:

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
NB use nano to copy the key in the file autorized_keys

Then select and copy the contents of the id_ed25519 file displayed in the terminal to your clipboard. Add the private SSH key to your GitHub repository as a "Secret." Go to "Settings" -> "Secrets" -> "New repository secret" and add the private SSH key with a meaningful name, DO_SSH_KEY.

The last and final step is to add the SSH ***public*** key to the GitHub account. navigate to the settings -> SSH and GCP keys -> New SSH key add your copied SSH key in key add the same key to the authorized_key file inside the .ssh folder in the server
Once you add the keys our server and GitHub sync is ready to test. You need to perform the deployment based on script written in yml file.

recap: 
the ***public*** key must be linked in github in the *profile settings* and in the *autorized_keys file* in the server
the ***private*** key must be a secret in github

## Secrets Required for Deployment

To successfully deploy the application using this GitHub Actions workflow, you need to set up the following secrets in your GitHub repository.

1. **DIGITALOCEAN_HOST**:
   - Description: IP address of the target server.
   - Where to find/create: Obtain from your hosting provider or system administrator.

1. **DIGITALOCEAN_USERNAME**:
   - Description: SSH username used to connect to the server.
   - Where to find/create: Your server's SSH username. we need to use root

1. **DIGITALOCEAN_SSH_KEY**:
   - Description: SSH private key for authentication.
   - Where to find/create: Generate an SSH key pair and add the private key as a secret.

1. **USER_NAME**:
   - Description: Username for the new user on the server.
   - Where to find/create: Specify a desired username for the new user.

1. **USER_PSSWRD**:
    - Description: Password for the newly created user on the server.
    - Where to find/create: Specify a secure password for the new user.

1. **POSTGRES_PASSWORD**:
   - Description: Password for the PostgreSQL database user.
   - Where to find/create: Specify a secure password for the database user.

1. **DJANGO_SECRET_KEY**:
   - Description: Django secret key for security.
   - Where to find/create: Generate a new secret key for your Django application.

1. **DJANGO_ALLOWED_HOSTS**:
   - Description: Comma-separated list of allowed hosts for the Django application.
   - Where to find/create: Specify the allowed hosts for your application. the host needed are the 
      human readable url eg: www.domain.com and domain.com. if there are no such url add a , as the secret content


Note: Ensure these secrets are set up in your GitHub repository settings under the "Settings" tab, and then navigate to "Secrets".





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

Capisco, possiamo tradurre la guida in inglese. Ecco la versione rivista della documentazione:

---

# Project Deployment Guide

## Prerequisites:
- A GitHub account
- A DigitalOcean account

## Creating a Droplet on DigitalOcean:

1. Log in to your DigitalOcean account.
2. In the dashboard, select "Droplets" from the main menu.
3. Click on "Create Droplet".
4. Configure the Droplet options as desired (distribution, size, datacenter, etc.).
5. Choose "SSH Key" as the authentication method and select or create an SSH key pair.
6. Click on "Create Droplet" to start the creation process.

## Creating SSH Keys:

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
NB use nano to copy the key in the file autorized_keys

Then select and copy the contents of the id_ed25519 file displayed in the terminal to your clipboard. Add the private SSH key to your GitHub repository as a "Secret." Go to "Settings" -> "Secrets" -> "New repository secret" and add the private SSH key with a meaningful name, DO_SSH_KEY.

The last and final step is to add the SSH ***public*** key to the GitHub account. navigate to the settings -> SSH and GCP keys -> New SSH key add your copied SSH key in key add the same key to the authorized_key file inside the .ssh folder in the server
Once you add the keys our server and GitHub sync is ready to test. You need to perform the deployment based on script written in yml file.

recap: 
the ***public*** key must be linked in github in the *profile settings* and in the *autorized_keys file* in the server
the ***private*** key must be a secret in github









# Guide to Deploying a Project Using a Template

## Creating the Project Using the Template

1. **Create a Project Using the Template:**
   - Log in to GitHub and use the default template to create a new repository.
   - Make sure to select the appropriate template for the type of project you want to develop.

2. **Clone the Repository Locally:**
   - Use Git to clone the newly created repository to your local machine.
   - Run the command:
     ```
     git clone <repository_URL>
     ```
   to clone the repository.

3. **Modify the New Project:**
   - Open the cloned project in your preferred text editor.
   - Modify the source code, configuration files, and other project elements according to your needs.

## Configuration for Production

4. **Create the Droplet:**
   - Log in to your DigitalOcean account and create a new droplet.
   - Select the droplet specifications based on the project requirements.

5. **Update and Configure the Droplet:**
   - After creating the droplet, access it via SSH.
   - Update the droplet's operating system by running:
     ```
     sudo apt-get update && sudo apt-get upgrade -y
     ```
   - Install Docker and Docker Compose on the droplet.

6. **Generate the SSH Key Pair:**
   - Generate an SSH key pair by running the following command:
     ```
     ssh-keygen -t ed25519 -C "your_email@example.com"
     ```
   - Add the SSH private key to the `ssh-agent` and the `~/.ssh/authorized_keys` file by running the following commands:
     ```
     eval "$(ssh-agent -s)"
     ssh-add ~/.ssh/id_ed25519
     ```
   - To view the SSH public key, run:
     ```
     cat ~/.ssh/id_ed25519.pub
     ```
   - Copy the displayed SSH public key and add it to your GitHub Secrets and the `~/.ssh/authorized_keys` file on the droplet.

7. **Create the Token on DigitalOcean:**
   - Log in to your DigitalOcean account and generate a new access token for the API.
   - Copy the generated token securely.

8. **Create the Secrets on GitHub:**
   - Add the following secrets to the GitHub repository:
     - `DIGITALOCEAN_ACCESS_TOKEN`: The access token generated on DigitalOcean.
     - `DO_SSH_PRIVATE_KEY`: The SSH private key generated for the droplet.
     - `HOST`: The IP address or hostname of the droplet.
     - `POSTGRES_DB`: The name of the PostgreSQL database.
     - `POSTGRES_PASSWORD`: The password for the PostgreSQL database.
     - `POSTGRES_USER`: The user for the PostgreSQL database.
     - `USERNAME`: The username to access the droplet.

9. **Push Changes to the GitHub Repository:**
   - Stage, commit, and push the changes made to the repository to GitHub.

Once these steps are completed, your project will be ready to be deployed using the DigitalOcean droplet. Be sure to test the process and monitor the application after deployment to ensure everything is functioning correctly.






































