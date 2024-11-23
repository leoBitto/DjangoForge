# Deployment

[Back to index]({{ site.baseurl }})

## Prerequisites:
- A GitHub account
- An IaaS provider account (e.g., DigitalOcean, AWS, Azure, etc.)

> [!TIP]  
> Before using the Docker implementation, it’s recommended to utilize Django's development server for debugging purposes during the initial stages of development.

> [!WARNING]  
> Ensure you update the image name inside the docker-compose.prod.yml with the lowercase name of the repository

## Setting Up the Server

### Creating a Virtual Machine or Droplet:
1. Log in to your IaaS provider's account.
2. Navigate to the "Create VM" or "Create Droplet" section.
3. Configure your instance settings (OS distribution, size, region, etc.).
4. Choose **SSH Key** as the authentication method and either create or select an existing SSH key pair.
5. Finalize and create the virtual machine.

> [!NOTE]  
> This guide uses generic terms. The steps may differ slightly depending on the IaaS provider you choose.

### Creating SSH Keys:
To establish a secure connection between your server and GitHub Actions, you need to create and configure SSH keys:

1. **Generate an SSH key pair**:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   - Press **Enter** to accept the default file location.
   - Leave the passphrase empty by pressing **Enter** again.

2. **Add the SSH key to the SSH agent**:
   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```

3. **Retrieve the public key**:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   - Copy the displayed key for use in the next steps.

### Configuring SSH Keys in GitHub:
1. **Add the private key to GitHub as a repository secret**:
   - Navigate to **Settings** → **Secrets and Variables** → **Actions** → **New repository secret**.
   - Name it, e.g., `PRIVATE_KEY`, and paste the **private key** contents.

2. **Add the public key to your GitHub account**:
   - Go to **Profile Settings** → **SSH and GPG keys** → **New SSH key**.
   - Paste the **public key** copied earlier.

### Configuring the Server:
1. **Add the public key to the server**:
   - Connect to the server as root:
     ```bash
     ssh root@your_server_ip
     ```
   - Add the public key to the `~/.ssh/authorized_keys` file:
     ```bash
     echo "your_public_key" >> ~/.ssh/authorized_keys
     ```

> [!TIP]  
> Use `nano ~/.ssh/authorized_keys` to edit and verify the key is correctly added.

### Recap:
- **Public key**:
  - Added to GitHub under **Profile Settings** → **SSH keys**.
  - Added to the server’s `authorized_keys` file.
- **Private key**:
  - Saved as a repository secret in GitHub Actions.

---

Per creare il **Personal Access Token (PAT)** per il secret `GHCR_TOKEN` e configurare correttamente tutti gli altri valori, puoi seguire le istruzioni dettagliate che possiamo includere nella documentazione. 

Ecco come procedere e come documentarlo:

---

### **Configuring Required GitHub Secrets**

To deploy the project, you need to set up the necessary secrets in your GitHub repository. Below are step-by-step instructions for obtaining each value:

#### **1. Create a Personal Access Token (PAT) for `GHCR_TOKEN`**
The **GitHub Container Registry** requires a PAT to authenticate and push Docker images. Follow these steps:

1. Go to [GitHub Personal Access Tokens](https://github.com/settings/tokens).
2. Click **"Generate new token"** and select the following permissions:
   - **`write:packages`** (required for pushing Docker images to GHCR).
   - **`read:packages`** (to pull images, if needed).
   - **`delete:packages`** (optional, for cleaning up images).
3. Give the token a descriptive name (e.g., `GHCR Token`) and click **"Generate token"**.
4. Copy the token immediately (it won't be visible again) and add it to your repository:
   - Go to **"Settings" → "Secrets and variables" → "Actions" → "New repository secret"**.
   - Create a secret named `GHCR_TOKEN` and paste the token value.

---

#### **2. Obtaining the `DEBUG` Value**
- Use `True` for development or `False` for production environments. For deployment, set this to `False`.

---

#### **3. Setting the `SECRET_KEY`**
- Generate a strong, random secret key using a Python command:
  ```bash
  python -c 'import secrets; print(secrets.token_urlsafe(50))'
  ```
- Add the generated key as the value of the `SECRET_KEY` secret.

---

#### **4. Defining `DJANGO_ALLOWED_HOSTS`**
- Use a comma-separated list of hosts:
  - For local testing: `"localhost, 127.0.0.1"`.
  - For production: Your domain name (e.g., `"yourdomain.com"`).

---

#### **5. Configuring Database Secrets**
- Replace these placeholders with actual values from your database configuration:
  - **POSTGRES_DB**: The name of the primary database (e.g., `main_db`).
  - **POSTGRES_USER**: The database username (e.g., `db_user`).
  - **POSTGRES_PASSWORD**: The database password.
  - **SQL_HOST**: Hostname of the database (e.g., `db`).
  - **SQL_PORT**: Usually `5432` for PostgreSQL.

#### **6. Configuring Secondary Database Secrets (Gold Postgres)**
- These follow the same structure as the primary database:
  - **GOLD_POSTGRES_DB**: Name of the secondary database.
  - **GOLD_POSTGRES_USER**: Username for the secondary database.
  - **GOLD_POSTGRES_PASSWORD**: Password for the secondary database.
  - **GOLD_SQL_HOST**: Hostname for the secondary database (e.g., `db_gold`).
  - **GOLD_SQL_PORT**: Usually `5432`.

---

#### **7. Setting `EMAIL`**
- Add the email address used by the application, such as `admin@yourdomain.com`.

---

#### **8. Setting `DOMAIN`**
- Add your domain name (e.g., `yourdomain.com`).

---

### **Recap of Configured Secrets**

Once you have all the necessary values, add them as GitHub secrets under **"Settings" → "Secrets and variables" → "Actions" → "New repository secret"**.

| Secret Name             | Description                                   | How to Obtain                                   |
|-------------------------|-----------------------------------------------|------------------------------------------------|
| `DEBUG`                 | Debug mode for Django                        | Use `False` for production                    |
| `SECRET_KEY`            | Secret key for Django                        | Generate with Python                          |
| `DJANGO_ALLOWED_HOSTS`  | Allowed hosts for Django                     | Add domain(s)                                 |
| `SQL_ENGINE`            | SQL engine for Django                        | Use `django.db.backends.postgresql`           |
| `POSTGRES_DB`           | Main database name                           | Use your database config                      |
| `POSTGRES_USER`         | Main database user                           | Use your database config                      |
| `POSTGRES_PASSWORD`     | Main database password                       | Use your database config                      |
| `SQL_HOST`              | Main database host                           | Usually `db`                                  |
| `SQL_PORT`              | Main database port                           | Usually `5432`                                |
| `GOLD_POSTGRES_DB`      | Secondary database name                      | Use your secondary database config            |
| `GOLD_POSTGRES_USER`    | Secondary database user                      | Use your secondary database config            |
| `GOLD_POSTGRES_PASSWORD`| Secondary database password                  | Use your secondary database config            |
| `GOLD_SQL_HOST`         | Secondary database host                      | Usually `db_gold`                             |
| `GOLD_SQL_PORT`         | Secondary database port                      | Usually `5432`                                |
| `EMAIL`                 | Application email                            | Add your email address                        |
| `DOMAIN`                | Application domain                           | Add your domain                               |
| `GHCR_TOKEN`            | Token for GitHub Container Registry (GHCR)   | Generate from GitHub Settings                 |

---

Questa sezione guida chiunque nel progetto a configurare i secrets in modo chiaro e organizzato. 
---

## CI/CD Workflow Execution:
Ensure that the CI/CD pipeline executes all 4 stages in sequence, one after the other, to maintain proper deployment order:

1. **Setup Server** (e.g., installing Docker, Nginx).
2. **Build and Push Docker Image** to your container registry.
3. **Deploy and Run Containers** on the server.
4. **Create Django Superuser** (run only initially).

This structured approach ensures reliable deployment and maintains consistency across environments.














