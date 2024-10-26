# Contributing to DjangoForge

Thank you for your interest in contributing to DjangoForge! Please follow these guidelines to ensure that your contribution can be integrated into the project.

## How to Contribute

1. **Fork the Repository**: Create a copy of the repository in your GitHub account.
2. **Create a Branch**: Work on a dedicated branch for your changes.
    ```bash
    git checkout -b your-branch-name
    ```
3. **Write Code and Tests**: Make sure your code is well-documented and includes tests for new features or bug fixes.
4. **Run Tests**: Before submitting a pull request, ensure all tests pass.
    ```bash
    docker-compose exec web python manage.py test
    ```
5. **Pull Request**: Open a pull request describing the changes made and their purpose. Follow the pull request template provided by the repository.

## Coding Style

- Use Django best practices.
- Follow PEP 8 conventions for Python.
- Ensure the code is DRY (Don't Repeat Yourself) and well-documented.

## Review Process

Pull requests will be reviewed by the project team. Please be patient; we will do our best to provide feedback as quickly as possible.

## Reporting Issues

If you find a bug, please open an issue on GitHub with a detailed description of the problem and how to reproduce it.

Thank you for your contribution!
