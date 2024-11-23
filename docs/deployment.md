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

### Configurazione dei Secrets su GitHub

1. **Accedi ai secrets del repository:**
   - Vai su **Settings** → **Secrets and variables** → **Actions**.

2. **Aggiungi i seguenti secrets:**
   | Nome del Secret           | Descrizione                                           |
   |---------------------------|-------------------------------------------------------|
   | `HOST`                    | IP del server DigitalOcean                            |
   | `USERNAME`                | Nome utente per l'accesso SSH (es. `root`)            |
   | `PRIVATE_KEY`             | Contenuto della chiave privata SSH (`id_ed25519`)     |
   | `SECRET_KEY`              | Secret key Django (se non generata dinamicamente)     |
   | `DJANGO_ALLOWED_HOSTS`    | Host consentiti (es. `yourdomain.com 127.0.0.1`)      |
   | `POSTGRES_USER`           | Nome utente del database PostgreSQL                   |
   | `POSTGRES_PASSWORD`       | Password del database PostgreSQL                      |
   | `GOLD_POSTGRES_USER`      | Nome utente del database PostgreSQL secondario       |
   | `GOLD_POSTGRES_PASSWORD`  | Password del database PostgreSQL secondario           |
   | `DOMAIN`                  | Dominio per CSRF settings (se richiesto)              |


---

## CI/CD Workflow Execution:
Ensure that the CI/CD pipeline executes all 4 stages in sequence, one after the other, to maintain proper deployment order:

1. **Setup Server** (e.g., installing Docker, Nginx).
2. **Build and Push Docker Image** to your container registry.
3. **Deploy and Run Containers** on the server.
4. **Create Django Superuser** (run only initially).

This structured approach ensures reliable deployment and maintains consistency across environments.














