# DjangoForge: A Django Ecosystem for SMEs

## Description

**DjangoForge** is a modular ecosystem based on Django, designed to provide customizable software solutions for small and medium-sized enterprises (SMEs). The project is organized into three main tiers:

- **Base Project**: Contains the essential functionalities required by all applications.
- **Tier 1**: Generic business applications like CRM and ERP, usable by a wide range of enterprises.
- **Tier 2**: Industry-specific applications, extending Tier 1 apps with tailored functionalities.

## Technologies Used

- **Framework**: Django
- **Database**: Postgres
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## Installation

### Prerequisites

- Docker and Docker Compose installed
- Python 3.x
- Git

### Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/leoBitto/djangoforge.git
    cd djangoforge
    ```

2. Build the Docker containers:
    ```bash
    source manager.sh build
    ```



## Contributing

Contributions are welcome! For more details, please see the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the GPLv3 License. For more details, see the [LICENSE](LICENSE) file.

## Contact

For questions or support, open an issue on GitHub.
