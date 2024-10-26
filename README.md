# Arnia: Personal Finance Management

## Description

**Arnia** is a modular ecosystem built on Django, designed to help you manage personal finances with the thoroughness of a small business setup. Organized for complete control and an overview of your finances, **Arnia** enables you to track income, expenses, accounts, and recurring payments efficiently.

### Key Features

- **Financial Dashboard**: Get a clear overview of total balances, recent income, and expenditures at a glance.
- **Account and Transaction Management**: Organize your accounts (e.g., checking accounts, credit cards) and categorize both income and expenses.
- **Recurring Expenses and Notifications**: Set up recurring payments and receive reminders to stay up-to-date.
- **Financial Analytics**: Summaries and reports for a comprehensive view of your finances.

## Technologies Used

- **Framework**: Django
- **Database**: PostgreSQL
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
    git clone https://github.com/leoBitto/arnia.git
    cd arnia
    ```

2. Build the Docker containers:
    ```bash
    source manager.sh build
    ```

3. Start the application:
    ```bash
    docker-compose up
    ```

## License

This project is licensed under the GPLv3 License. For more details, see the [LICENSE](LICENSE) file.

## Contact

For questions or support, please open an issue on GitHub.

