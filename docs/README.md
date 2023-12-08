# DjangoForge

#### A ready-to-deploy Django project.

Follow these steps to prepare the project:

## HOW TO START

### MOUNTING THE PROJECT

Before performing production steps, we need to mount the project on the **development** machine and create a new repo where the project will be launched.

1. Clone the `cliche_django` project from GitHub, changing the name of the folder that will contain the project. The recursive flag allows downloading the submodules.
    ```bash
    git clone --recursive https://github.com/leoBitto/DjangoForge.git <name of the new project>
    ```

2. Create a new empty repo on GitHub that will contain the entire project.

3. Change the remote version of the repo we just created on the dev machine (the cloned `cliche`) to the repo we created on GitHub.
    ```bash
    git remote set-url origin <URL of the new repo on GitHub>
    ```

4. Finally, mount the project: clone all the apps you need inside the project (the `src` directory) as submodules.
    ```bash
    git submodule add <URL to submodule> src/<name of app>
    ```

    Then `git add`, `git commit`, and push.

5. Update the setting file with all the Django apps we intend to use and add the new set of URLs the application uses in the `urls.py` file. In `settings.py`:

    1. Update the `INSTALLED_APPS` list with the apps we use.

   In `urls.py`:
    1. Include the app URLs inside the file.


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


## SET TO PRODUCTION

1. Enter the server.

2. Update the server.
    ```bash
    apt update    # Update repo
    apt upgrade   # Upgrade repo; a reboot may be necessary
    apt install virtualenv python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl  # Install all the packages
    ```

3. Create a user.
    ```bash
    adduser <choose a user name>               # Create the user
    usermod -aG sudo <the user name chosen>    # Modify the privileges of the user
    su <the user name chosen>                   # Switch to the user
    ```

4. Change the directory to the home of the new user.

5. Clone from git.
    ```bash
    git clone --recursive <URL to repo> <name of the directory you want to put the cloned repo>
    ```

6. CD inside the new folder.

7. Create a virtual environment called `env_dj`.
    ```bash
    virtualenv env_dj
    ```

### DATABASE

#### Create the PostgreSQL DB and User (DON'T FORGET THE SEMICOLON!)

'myproject' is the name of the DB.
'myprojectuser' is the name of the user that has been created.

1.  ```bash
    sudo -u postgres psql
    ```

2.  ```bash
    CREATE DATABASE myproject;
    ```

3.  ```bash
    CREATE USER myprojectuser WITH PASSWORD 'password';  # Password must be between quotes
    ```

4.  ```bash
    ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
    ```

5.  ```bash
    ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
    ```

6.  ```bash
    ALTER ROLE myprojectuser SET timezone TO 'UTC';
    ```

7.  ```bash
    GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
    ```

8.  ```bash
    \q   # Close the prompt
    ```

#### IN .env (DO NOT USE SPACES), put `.env` inside `/src`

```env
SECRET_KEY=thisisaverysecretkeyforthisdjangoforge
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
# aggiungi un indirizzo ip e un nome di dominio con la virgola e senza spazi
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASS=
```

# DJANGO

The Django project is inside the `/src` folder. Here resides all the code necessary to make the Django project work. Inside the `/base` folder, there are the basic settings and the `.env` file. Inside the `/src` folder, along with the `/base` folder, there will be all the Django apps.

From the main folder:

1. Activate the environment.
    ```bash
    source env_dj/bin/activate
    ```

2. Install resources in pip from requirements.
    ```bash
    pip install -r requirements.txt
    ```

3. Change directory to the `/src` directory.
    ```bash
    cd /src
    ```

4. `manage.py`:
    1. ```bash
       python manage.py makemigrations   # Create migrations
       ```
    2. ```bash
       python manage.py migrate          # Effectively migrate
       ```
    3. ```bash
       python manage.py createsuperuser  # Create the superuser
       ```
    4. ```bash
       python manage.py collectstatic    # Gather everything inside a static folder
       ```

5. Exit the environment.
    ```bash
    deactivate
    ```

### SETTING PERMISSION

`/home/` and all the contained folders MUST be owned by the nginx user `www-data`.

# CALLING THE SCRIPT

Now you can call the script inside the script folder:

```bash
sudo ./set_pro_server.sh
```

NB you may need to call the scripts inside the apps to make everything work

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
inside this directory there should be a file called dashboard.html that expand using '{% include %}'
the dashboard.html inside website app.

this file should be expanded using '{% expand %}' with templates that show the objects needed






