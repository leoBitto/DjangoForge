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

## SET TO PRODUCTION

# Automated Server Setup with Deployment Script

## Overview

This guide explains how to use the provided deployment script to set up a server for the DjangoForge project. The script automates various steps involved in server setup, application deployment, and database configuration. Digital Ocean provides a feature called Droplets. Droplets are scalable compute platforms with add-on storage, where your applications can be deployed. In the script, there might be references to Digital Ocean-specific details like IP addresses, server configurations, etc. The script could potentially use the Digital Ocean API or command-line tools to interact with your Droplet.

Public SSH Key:

When you create a new Droplet on Digital Ocean, make sure to add the public SSH key to your Digital Ocean account. This allows you to authenticate securely when GitHub Actions tries to connect to your Droplet.

Add the private SSH key to your GitHub repository as a "Secret." Go to "Settings" -> "Secrets" -> "New repository secret" and add the private SSH key with a meaningful name, DO_SSH_KEY.

1. Add GitHub Secrets:
Make sure you have the necessary secrets set up in your GitHub repository. These secrets include:
    
    1. **USER_NAME:**
       - **Description:** The username for the new user created on the server.
       - **Usage:** Used to create a new user during the server configuration script.
    
    2. **DJANGO_SECRET_KEY:**
       - **Description:** The Django secret key.
       - **Usage:** This key is essential for Django's security and should be kept confidential. It is used to generate cryptographic signatures and must remain private.
    
    3. **DJANGO_ALLOWED_HOSTS:**
       - **Description:** A comma-separated list of allowed hosts for Django.
       - **Usage:** Django uses this list to determine which HTTP requests are allowed. Hosts included in this list are considered secure.
    
    4. **DJANGO_DB_NAME:**
       - **Description:** The name of your PostgreSQL database.
       - **Usage:** Specifies the name of the database to which your Django project will connect to store data.
    
    5. **DJANGO_DB_USER:**
       - **Description:** The username for the PostgreSQL database user.
       - **Usage:** Indicates the username that Django will use to connect to the PostgreSQL database.
    
    6. **DJANGO_DB_PASS:**
       - **Description:** The password for the PostgreSQL database user.
       - **Usage:** The password associated with the database user specified in **DJANGO_DB_USER**.
    
    7. **DO_SERVER_IP:**
       - **Description:** The IP address of your Digital Ocean server.
       - **Usage:** Used to connect to the server via SSH during the deployment process.
    
    8. **DO_SSH_USERNAME:**
       - **Description:** The username used for SSH connection to the Digital Ocean server.
       - **Usage:** The username used to authenticate the SSH connection to your server.
    
    9. **DO_SSH_KEY:**
       - **Description:** The private SSH key used for connection to the Digital Ocean server.
       - **Usage:** This private key is required to authenticate and establish an SSH connection to the Digital Ocean server. Ensure not to share this key and keep it confidential.

2. Create the GitHub Actions Workflow:
Create a new file (e.g., .github/workflows/deploy.yml) and paste the provided script into that file. Adjust the file paths and configurations as needed. This GitHub Actions workflow automates the deployment process of a Django application to a Digital Ocean server. The following steps are executed:
    
    1. Checkout Repository:
    Perform a checkout of the repository to retrieve project files.
    2. Configure SSH and Deploy:
    Set up SSH information to connect to the Digital Ocean server.
    Connect to the server via SSH and execute the deployment script.
    3. Update and Upgrade Server:
    Update the server's operating system and installed packages.
    4. Create New User:
    Create a new user on the server with necessary privileges.
    5. Activate Virtual Environment and Install Python Dependencies:
    Create and activate a Python virtual environment.
    Install project dependencies for Django.
    6. Create .env File:
    Generate the .env file containing secret variables required by Django.
    7. Create PostgreSQL Database and User:
    Create the PostgreSQL database and associated user.
    8. Run Django Management Commands:
    Execute Django commands for migrations, superuser creation, and static file collection.
    9. Configure Gunicorn:
    Perform necessary configurations for Gunicorn, a WSGI application server for Django.
    Start and enable the Gunicorn service.
    10. Configure Nginx:
    Apply configurations for Nginx, a web server.
    Conduct a configuration test and restart Nginx.
    11. Fix Firewall:
    Open and close specific firewall ports.
    12. Final Checks:
    Perform final checks by viewing the status of deployed services.

This script streamlines the deployment process, automating several manual steps, and can be triggered automatically on every push to the main branch of the GitHub repository.

3. Push to Main Branch:
Commit and push this new workflow file to your main branch. This will trigger the GitHub Actions workflow.

4. Monitor Workflow Execution:
Go to the "Actions" tab on your GitHub repository to monitor the progress of the workflow. If everything is configured correctly, the workflow will execute the steps defined in the script.

5. Check Server and Application:
After the workflow has completed successfully, check your Digital Ocean server to ensure that the Django application is deployed and running. You can use the final checks section in the script as a starting point for verification.

Note:
The workflow is configured to run on every push to the main branch. You can adjust the trigger conditions in the on section if needed.
Ensure that your server and GitHub repository configurations are compatible with this script (e.g., PostgreSQL setup, file paths, etc.).





