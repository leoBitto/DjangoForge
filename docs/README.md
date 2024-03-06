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

