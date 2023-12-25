# DjangoForge

## Overview

DjangoForge is a ready-to-deploy Django project. This guide outlines the process of automated deployment using GitHub Actions for a template repository.

Follow these steps to prepare the project:

### 1. Create Repository from Template

1. Click on the "Use this template" button on the GitHub repository page.
2. Create a new repository based on the template.

### 2. Clone the New Repository Locally

```bash
git clone --recursive https://github.com/your-username/your-new-repo.git
cd your-new-repo
```

### DEVELOP THE PROJECT

1. Mount or develop new app for the project: clone all the apps you need inside the project (the `src` directory) as submodules.
    ```bash
    git submodule add <URL to submodule> src/<name of app>
    ```

    Then `git add`, `git commit`, and push.

2. Update the setting file with all the Django apps we intend to use and add the new set of URLs the application uses in the `urls.py` file. In `settings.py` update the `INSTALLED_APPS` list with the apps we use.


### `manifest.json`
The `manifest.json` file is essential for turning your project into a Progressive Web App (PWA). It contains information such as the app name, icons, and other configurations. You can find it in the `static` folder of the website app. change name, short name, app description and icon name.

**Customization Tips:**

- `"name"`: Update this with the name of your app.
- `"short_name"`: Provide a shorter version of your app name for limited space.
- `"start_url"`: Set the starting URL of your app.
- `"icons"`: Replace the default icons with your own. Ensure they have the correct sizes and file paths.

For more details, refer to the [Web App Manifest documentation](https://developer.mozilla.org/en-US/docs/Web/Manifest).

### `service-worker.js`
The `service-worker.js` file handles Service Worker functionalities, such as resource caching. Customize it based on your project's needs. You can find it in the `static` folder inside the website app. you need to customize the caching of the icon.

**Customization Tips:**

- `CACHE_NAME`: This is the name of the cache. You can keep it as is or customize it.
- `urlsToCache`: Add URLs of resources you want to cache for offline access.
- `self.addEventListener('fetch', function(event) {...}`: This section determines how the Service Worker responds to network requests. Customize it if needed.

For more details, refer to the [Service Worker API documentation](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API).


# DJANGO

The Django project is inside the `/src` folder. Here resides all the code necessary to make the Django project work. Inside the `/base` folder, there are the basic settings and the `.env` file. Inside the `/src` folder, along with the `/base` folder, there will be all the Django apps.

```
cliche_django/    # Cartella principale del progetto 
├── env_dj/        # Ambiente virtuale 
│   ├── ... 
├── scripts/       # Script 
│   ├── ... 
├── log/           # log 
│   ├── ... 
├── static/        # static, its fille when collectstatic is used 
│   ├── ... 
└── src/           # Sorgenti principali dell'applicazione 
    ├── base/      # Applicazione principale del progetto 
    │   ├── ... 
    ├── website/   # Sottomodulo Git 'website' 
    │   ├── ... 
    └── manage.py  # File di gestione del progetto Django 
```

# using website module
the website module allow you to load images, gather them in galleries, add
contacts and opening hours. to use the module you need to:
1. modify landing page
2. modify navbar and footer with the links of all the pages you want to be accessible
3. modify the view called base, it will call the page landing.html
    add the info in the context you use in the landing. it will be the first page
    seen by the user.
4. modify the favicon, and title in the template base.html

## the dashboard
the website application have a dashboard part that allow you to make the CRUD operations
on graphical objects such as images and galleries... 
the dashboard can be the place where all such operations for the other apps should be done.
it can be expanded by creating a dashboard directory inside the templates directory of the new app

```
app folder
│   ├── ... 
├── templates/        
│   ├── dashboard
└── ...  
``` 

this allow you to keep the dashboard components inside of the new app separated from the rest.
inside this directory there should be a file called dashboard.html that expand using include
the dashboard.html inside website app.

this file should be expanded using expand with templates that show the objects needed

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

1. **DO_SERVER_IP:**
   - Description: IP address of the target server.
   - Where to find/create: Obtain from your hosting provider or system administrator.

2. **DO_SSH_USERNAME:**
   - Description: SSH username used to connect to the server.
   - Where to find/create: Your server's SSH username. we need to use root

3. **DO_SSH_KEY:**
   - Description: SSH private key for authentication.
   - Where to find/create: Generate an SSH key pair and add the private key as a secret.

4. **USER_NAME:**
   - Description: Username for the new user on the server.
   - Where to find/create: Specify a desired username for the new user.

5. **USER_PSSWRD:**
    - Description: Password for the newly created user on the server.
    - Where to find/create: Specify a secure password for the new user.

6. **DJANGO_DB_NAME:**
   - Description: Name of the PostgreSQL database.
   - Where to find/create: Choose a name for your Django application database.

7. **DJANGO_DB_USER:**
   - Description: Username for the PostgreSQL database user.
   - Where to find/create: Specify a username for the database user.

8. **DJANGO_DB_PASS:**
   - Description: Password for the PostgreSQL database user.
   - Where to find/create: Specify a secure password for the database user.

9. **DJANGO_SECRET_KEY:**
   - Description: Django secret key for security.
   - Where to find/create: Generate a new secret key for your Django application.

10. **DJANGO_ALLOWED_HOSTS:**
   - Description: Comma-separated list of allowed hosts for the Django application.
   - Where to find/create: Specify the allowed hosts for your application. the host needed are the 
      human readable url eg: www.domain.com and domain.com. if there are no such url add a , as the secret content


Note: Ensure these secrets are set up in your GitHub repository settings under the "Settings" tab, and then navigate to "Secrets".



### Deployment Workflow

This script streamlines the deployment process, automating several manual steps, and can be triggered automatically on every push to the main branch of the GitHub repository.
Go to the "Actions" tab on your GitHub repository to monitor the progress of the workflow. If everything is configured correctly, the workflow will execute the steps defined in the script.
After the workflow has completed successfully, check your Digital Ocean server to ensure that the Django application is deployed and running. You can use the final checks section in the script as a starting point for verification.


#### Checkout Repository:

This step uses the GitHub `actions/checkout` action to clone the repository into the GitHub Actions runner. The `submodules: recursive` flag indicates to clone submodules if present.

#### Define REPO_NAME:

Utilizes the `$GITHUB_REPOSITORY` variable to extract the repository name and saves it in the `REPO_NAME` variable within GitHub Actions Environment Variables (`$GITHUB_ENV`).

#### Configure Server:

Uses the `appleboy/ssh-action` action to connect to the server configured in secret variables (`DO_SERVER_IP`, `DO_SSH_USERNAME`, `DO_SSH_KEY`).
- Creates a new user on the server (`USER_NAME`).
- Creates a PostgreSQL database and user, also setting permissions.

#### Clone Repository:

Clones the GitHub repository (primarily to obtain the source code) inside the server using the GitHub username and repository name.

#### Activate Virtual Environment and install dependencies:

Creates a Python virtual environment (`env_dj`), activates the virtual environment, and installs project dependencies specified in the `requirements.txt` file.

#### Create .env file:

Creates the `.env` file within the project path with the necessary Django secret key, debug settings, allowed hosts, and database credentials.

#### Run Django Commands:

Executes Django commands such as `makemigrations`, `migrate`, `createsuperuser` (without user input prompt), and `collectstatic`.

#### Configure Gunicorn:

Configures Gunicorn with the username and repository name. Copies the Gunicorn configuration files (`gunicorn.socket` and `gunicorn.service`) into the systemd directory and starts the Gunicorn service.

#### Configure Nginx:

Configures Nginx with the server's IP address, username, and repository name. Copies the Nginx configuration file (`conf.nginx`) into the correct directory and checks the Nginx configuration before restarting the service.

#### Fix Firewall:

Fixes firewall rules by removing the rule for port 8000 and allowing full access to Nginx.

#### Final Checks:

Restarts Gunicorn and Nginx and displays the status of the services to check if they are active and functioning.




