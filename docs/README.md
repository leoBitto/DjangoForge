# DjangoForge: User Manual

[![pages-build-deployment](https://github.com/leoBitto/DjangoForge/actions/workflows/pages/pages-build-deployment/badge.svg?branch=main)](https://github.com/leoBitto/DjangoForge/actions/workflows/pages/pages-build-deployment)

## Introduction
Welcome to the DjangoForge User Manual!
DjangoForge is a project ready for deployment, based on Django. This manual provides detailed instructions on how to use the automatic procedure of deployment using GitHub Actions.

## Project Setup

### Create a Repository from Template

1. Click on the "Use this template" button on the GitHub repository page.
1. Create a new repository based on the template.

### Clone the New Repository Locally

```bash
git clone --recursive https://github.com/your-username/your-new-repo.git your-new-repo
cd your-new-repo
git remote add template https://github.com/leoBitto/DjangoForge.git
git remote add origin https://github.com/your-username/your-new-repo.git
```

to get updates from DjangoForge you must:

```bash

git fetch --all
git merge template/main --allow-unrelated-histories
```

## Project Development

1. Mount or develop new apps for the project: clone all necessary apps inside the project (the `src` directory) as submodules.
   ```bash
   git submodule add <URL to submodule> src/<name of app>
   ```
   
1. Update the setting file with all the Django apps we intend to use and add the new set of URLs the application uses in the `urls.py` file. In `settings.py` update the `INSTALLED_APPS` list with the apps we use.

1. Then `git add`, `git commit`, and `git push`. 

### use the manager.sh

`manager.sh` is a shell script that simplifies the process of starting the project locally for development.

- `source manager.sh build`: To build and start containers.
- `source manager.sh start`: To start containers.
- `source manager.sh stop`: To stop containers.
- `source manager.sh destroy`: To eliminate containers.

The most used command during development is `build`, which:
1. Eliminates the containers along with their images.
2. Builds them again.
3. Creates migrations for Django.
4. Runs `collectstatic`.
5. Prompts for superuser creation.

After running the command, you can find the app running at http://localhost.

_________________________________________________________________________________
## Project Deployment 

### Prerequisites:
- A GitHub account
- A DigitalOcean account ( or another IaaS provider )

> [!TIP] 
> before using the docker implementation it's better to use the full power of
> Django for debugging purpose
> so start the development server of Django during the first stages of development

>[!WARNING]
> you should change the name of the IMAGE_NAME in the CI-CD.yml and in server_setup.yml
> file so you can control the name you'll see in the packages tab on Github

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


#### Creating SSH Keys:

When you create a new Droplet on Digital Ocean, make sure to add the ***public SSH key*** to your Github account. This allows you to authenticate securely when GitHub Actions tries to connect to your Droplet. To do so, you need to enter the server as root, create a ssh key pairs:

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

Then select and copy the contents of the id_ed25519 file displayed in the terminal to your clipboard. Add the private SSH key to your GitHub repository as a "Secret":
1.  Go to "Settings" -> "Secrets" -> "New repository secret" 
1. add the private SSH key with a meaningful name, [eg. DO_SSH_KEY].

The last and final step is to add the SSH ***public*** key to the GitHub account:
1. navigate to the settings -> SSH and GCP keys -> New SSH key 
1. add your copied SSH key in key 
1. add the same key to the authorized_key file inside the .ssh folder in the server
Once you add the keys our server and GitHub sync is ready to test. 

recap: 
the ***public*** key must be linked in github in the *profile settings* ***and*** in the *autorized_keys file* in the server
the ***private*** key must be a secret in github

### create the other secrets on Github
the actions read from the secrets of github, they use the following information:

1. **DEBUG**             -> False (DJANGO)
1. **DOMAIN**            -> names of the domain (NGINX) if you don't have a domain yet use the ip adress of the droplet, if you have more than one domain eg. www.yourdomain.com and domain.com, separate them with a space
1. **EMAIL**             -> add a valid email for SSL (CERTBOT)
1. **GHCR_TOKEN**        -> [token of github](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
1. **HOST**              -> droplet IP address  
1. **POSTGRES_DB**       -> the name of the db (POSTGRES)
1. **POSTGRES_PASSWORD** -> the password of the db (POSTGRES)
1. **POSTGRES_USER**     -> the name of the db user (POSTGRES)
1. **PRIVATE_KEY**       -> private key from server
1. **SECRET_KEY**        -> yousecretkey (DJANGO)
1. **USERNAME**          -> root

>[!WARNING]
> you should change the name of the IMAGE_NAME in the build-and-push.yml 
> file so you can control the name you'll see in the packages tab on Github
> its not used the name of the repo because it NEED TO BE lowercase


>[!WARNING]
> you should change the name of the repo and your username in the docker 
> compose dev (docker-compose.dev.yml) so that you will point to your image
> the docker compose dev is used to create the image that is pushed to the ghcr

###  change the IMAGE_NAME
after the creation of the secret you have to change the image name in the workflow.
image name is an environment variable of the workflow that will be used as the name
to create the directory inside the server and as the name of the image inside the 
repository container.

## start the actions
After the creation of the secrets you can manually start the workflow in server_setup.yml
it will set up the server at the ip address you provided in the secrets. 
it will require the domain names separated by a comma if more than one. they will be used by certbot


then you can create a super user 
_______________________________________________________________________________

_______________________________________________________________________________

### Scopo e Filosofia Generale del Progetto

**1. Scopo del Progetto**
Il progetto è concepito per informatizzare e centralizzare le informazioni generate dalle piccole e medie imprese (PMI), con l'obiettivo di creare un sistema di Business Intelligence (BI). Il focus è sulla *self-service BI*, che consente agli imprenditori di accedere facilmente ai dati rilevanti della propria attività, permettendo loro di prendere decisioni più informate e di diventare maggiormente data-driven. Questo approccio rende la BI accessibile anche a coloro che non hanno competenze tecniche avanzate, democratizzando l'accesso alle informazioni strategiche.

**2. Utenti Target**
Il progetto è destinato principalmente a piccole e medie imprese, guidate da imprenditori interessati a sfruttare i dati per migliorare la gestione delle loro attività. Gli utenti ideali sono aziende che operano in settori come la distribuzione, la ristorazione, l'artigianato e altri contesti in cui il numero di dipendenti è limitato e le risorse tecniche sono spesso scarse.

**3. Filosofia del Progetto**
Il progetto si basa sulla convinzione che la Business Intelligence non debba essere esclusiva delle grandi aziende, ma che tutti possano beneficiare di queste informazioni strategiche. L'obiettivo è creare un software semplice, scalabile e standardizzato, che possa essere offerto a basso costo, rendendolo accessibile a un vasto pubblico di PMI. La semplicità nell'implementazione e nell'uso, unita alla scalabilità, è il cuore della filosofia del progetto.

**4. Casi d'Uso Principali**
Il progetto è pensato per supportare casi d'uso come:
   - Una piccola azienda di distribuzione con un solo dipendente.
   - Un ristorante con un numero limitato di dipendenti.
   - Un artigiano che desidera monitorare meglio i suoi processi e le sue vendite.

**5. Contesto d'Uso**
Il progetto è destinato a essere utilizzato in contesti aziendali ben consolidati, dove le imprese cercano di ottimizzare le loro operazioni attraverso l'uso di dati e analisi avanzate, ma senza dover ricorrere a soluzioni costose e complesse solitamente riservate alle grandi organizzazioni.



### **Componenti Principali del Sistema**

1. **Logging App**
   - **Scopo**: Questa applicazione è responsabile della registrazione e aggregazione dei log delle richieste HTTP e degli errori del sistema.
   - **Struttura**:
     - **Modelli**: I modelli per i log sono definiti in `base.py` e `aggregated.py`, situati nella directory `models/`.
     - **Attività (Tasks)**: Le attività di aggregazione dei log vengono gestite da script come `aggregate_access_logs.py` e `aggregate_error_logs.py` all'interno della cartella `tasks/`.
     - **Visualizzazioni (Views)**: Le visualizzazioni relative ai log sono definite in `views/base.py` e `views/aggregated.py`.

2. **Website App**
   - **Scopo**: Funziona come un semplice Content Management System (CMS) per gestire il frontend del sito. Offre funzionalità di base come pagine statiche e gestione delle autenticazioni.

3. **Backoffice App**
   - **Scopo**: Questa app fornisce strumenti per la gestione del backend e la visualizzazione dei dati, rivolta principalmente agli amministratori del sistema.

4. **Gold BI**
   - **Scopo**: Gestisce i processi ETL (Extract, Transform, Load) e le attività di schedulazione tramite Django Q. Questa app può estendersi alle schedulazioni di task di altre applicazioni, centralizzando la gestione delle operazioni pianificate.

### **Interazione tra le Componenti**

- **Comunicazione Inter-app**: 
   - Le diverse app comunicano tra loro sfruttando le funzionalità native di Django. Poiché ogni app è anche un modulo Python, le classi e le funzioni possono essere richiamate da un modulo all'altro. Ad esempio, un'app può importare modelli o task da un'altra app e utilizzarli secondo necessità.
   - Django gestisce anche il routing delle richieste tra le app e coordina l'interazione attraverso le sue funzionalità integrate, come i signal e le view.


### **Ambiente di Sviluppo e Produzione**

#### **1. Ambiente di Sviluppo**

**Configurazione Docker:**
- **Dockerfile**: Utilizzato per costruire l'immagine dell'applicazione. Include la creazione di un'immagine Python, l'installazione delle dipendenze, e la configurazione dell'ambiente di lavoro.
  - **Fase di Build**:
    - Installa le dipendenze di sistema e Python.
    - Crea una cache di pacchetti Python per un'installazione più veloce.
  - **Fase Finale**:
    - Configura un'immagine finale con le dipendenze e il codice sorgente.
    - Imposta il proprietario e il gruppo dei file, e avvia il server Gunicorn.

**File Docker Compose per Sviluppo (`docker-compose.dev.yml`):**
- **Servizi**:
  - **web**: Contiene l'app Django e viene avviato con Gunicorn. Monta volumi per i file statici e media. Dipende dai servizi `db` e `db_gold`.
  - **djangoq**: Esegue il cluster di Django Q per le operazioni di background. Utilizza lo stesso Dockerfile della `web`.
  - **db** e **db_gold**: Servizi PostgreSQL per i database principali e Gold BI, rispettivamente.
  - **nginx**: Servizio Nginx per servire i file statici e media, e fare da reverse proxy.
- **Volumi**: Utilizzati per i dati dei database e i file statici/media.
- **Network**: Configurato per il bridging tra i servizi, con indirizzi IP fissi.

**Script di Gestione (`manager.sh`):**
- **Funzioni**:
  - `build_and_start_containers`: Costruisce le immagini e avvia i container, applica le migrazioni e raccoglie i file statici.
  - `start_containers`: Avvia i container senza ricostruirli.
  - `stop_containers`: Ferma i container.
  - `destroy_containers`: Elimina tutti i container e i volumi.

#### **2. Ambiente di Produzione**

**File Docker Compose per Produzione (`docker-compose.prod.yml`):**
- **Servizi**:
  - **web**: Utilizza un'immagine pre-costruita (`djangoforge:latest`). Configurato per l'esecuzione in produzione con Gunicorn.
  - **djangoq**: Utilizza la stessa immagine del servizio `web` e gestisce le operazioni di background.
  - **db** e **db_gold**: Servizi PostgreSQL, configurati come in sviluppo ma senza montaggio di volumi specifici.
- **Volumi**:
  - **static_volume** e **media_volume**: Montati per l'archiviazione dei file statici e media.
  - **postgres_data** e **postgres_data_gold**: Utilizzati per la persistenza dei dati dei database.
- **Network**: Configurato per il bridging tra i servizi, con indirizzi IP fissi.

**Note sul Deployment**:
- **Immagini**: In produzione, le immagini Docker sono pre-costruite e recuperate da un registry.
- **Port Mapping**: Esposizione delle porte per l'accesso ai servizi.












