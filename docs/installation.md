# DjangoForge Installation Guide

[Back to index]({{ site.baseurl }})

Welcome to the installation guide for DjangoForge. This document will walk you through the process of setting up a development environment for DjangoForge. By the end of this guide, you'll have the project up and running on your local machine, ready for further development.

## Prerequisites

Before you start, ensure you have the following installed on your system:

- **Docker**: Make sure Docker is installed and running.
- **Docker Compose**: Docker Compose is needed to manage multi-container Docker applications.
- **Git**: Required to clone the repository and manage version control.
- **Bash**: This script is designed to be run in a Bash environment.

## Installation Steps

### 1. Fork the Repository

First, create a fork of the DjangoForge repository to your GitHub account. This allows you to make changes without affecting the original project.

### 2. Clone the Repository

Next, clone the repository from your fork to your local machine:

```bash
git clone https://github.com/leoBitto/djangoforge.git
cd djangoforge
```

### 3. Build and Start the Containers

Use the `manager.sh` script provided in the project to build and start the Docker containers. This script handles setting up the environment, including creating Docker images, applying database migrations, and more.

Run the following command from the root of the cloned repository:

```bash
source manager.sh build
```

This command will:

- **Remove existing containers and volumes**: Ensures a clean environment by stopping and removing any previous Docker containers and volumes.
- **Build Docker images**: Recreates the Docker images as defined in `docker-compose.dev.yml`.
- **Apply database migrations**: Runs database migrations to set up the required tables and schemas.
- **Collect static files**: Gathers static assets needed for the application.
- **Create a superuser**: Prompts you to create a superuser with credentials defined in the environment variables.
- **Start the Django Q cluster**: Ensures background tasks are properly managed.

### 4. Start the Development Server

If you need to restart the containers without rebuilding the images, you can use:

```bash
source manager.sh start
```

This command will start the Docker containers and apply any necessary migrations without rebuilding the images.

### 5. Stop the Containers

To stop the running containers without removing them, use:

```bash
source manager.sh stop
```

This will shut down the containers gracefully, allowing you to restart them later with the `start` command.

### 6. Destroy Containers and Volumes

If you want to completely remove all containers and associated volumes, use:

```bash
source manager.sh destroy
```

This is useful when you need to reset the environment or free up system resources.

## Troubleshooting

### Common Issues

- **Permission Denied**: If you encounter a "permission denied" error when running the script, ensure that your user has the necessary permissions to run Docker commands. You might need to prefix the command with `sudo`, or add your user to the `docker` group.
  
- **Database Errors**: If the database migrations fail, ensure that the database container is running and properly configured. Check the logs using `docker-compose logs` for more information.

- **Superuser Creation Failure**: If the superuser creation fails, ensure that the environment variables for the superuser credentials are correctly set.

## Next Steps

After completing the installation, you can start developing and extending DjangoForge. Be sure to review the [Base](docs/base.md) documentation to familiarize yourself with the codebase.

For contributing guidelines, refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

If you have any questions or run into issues, feel free to open an issue on GitHub or contact the DjangoForge support team.

---

Happy coding!


