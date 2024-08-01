# Logging_app docs

## Introduction

The **logging_app** is a Django application designed to monitor access and errors within a Django project, document them, and provide a means to examine them, particularly in production environments. This app offers a comprehensive solution for tracking user interactions and system errors, facilitating effective troubleshooting and analysis.

## Purpose

In today's digital landscape, understanding user behavior and identifying system errors are crucial aspects of maintaining a successful web application. The **logging_app** serves the following purposes:

- **Access Monitoring**: Tracks and logs access to various pages and resources within the application, providing insights into user traffic patterns and popular features.
- **Error Logging**: Captures and documents errors that occur during application runtime, enabling developers to diagnose and rectify issues promptly.
- **Documentation**: Organizes access and error logs in a structured format, making it easier to review historical data and identify trends over time.
- **Production Monitoring**: Offers robust monitoring capabilities suitable for production environments, allowing administrators to monitor application health and performance continuously.

## Required Packages

The **logging_app** relies on several Python packages to function properly. Below is a list of essential packages that need to be installed in your Python environment:

- **Django (5.0)**: Django is the web framework on which the **logging_app** is built. It provides the foundation for handling HTTP requests, managing databases, and rendering templates.

- **psycopg2-binary (2.9.9)**: psycopg2-binary is a PostgreSQL adapter for Python. It enables Django to interact with PostgreSQL databases, which is often used as the backend database for Django projects.

- **django-environ (0.11.2)**: django-environ is a Django utility for handling environment variables. It simplifies the process of configuring Django settings using environment variables.

- **django-quill-editor (0.1.40)**: django-quill-editor is a Django app that provides integration with the Quill rich text editor. It allows users to input rich text content in forms within the Django admin interface.

- **pandas (2.1.4)**: pandas is a powerful data manipulation and analysis library for Python. It is used within the **logging_app** for handling data related to access and error logs.

- **numpy (1.26.2)**: numpy is a fundamental package for scientific computing with Python. It is used alongside pandas for efficient data manipulation and analysis tasks.

- **plotly (5.18.0)**: plotly is a Python graphing library that makes interactive, publication-quality graphs online. It is utilized within the **logging_app** to generate various graphs and charts for visualization purposes.

- **python-dateutil (2.8.2)**: python-dateutil is a module that provides powerful extensions to the standard datetime module in Python. It is used within the **logging_app** for handling date and time data.

- **fontawesomefree (6.4.2)**: fontawesomefree is a library that provides a collection of scalable vector icons. It is used for styling and enhancing the user interface of the **logging_app**.

Ensure that these packages are installed in your Python environment before running the **logging_app**. 


# Getting Started

To incorporate the **logging_app** into your Django project and leverage its monitoring capabilities, follow these steps:

1. **Installation**:
   - Copy the `logging_app` directory into your Django project's directory structure.

2. **Configuration**:
   - Add `'logging_app'` to the `INSTALLED_APPS` list in your project's `settings.py` file.

3. **URL Configuration**:
   - Include the `logging_app` URLs in your project's main URL patterns. Add the following line inside the URL patterns of your project's URLs file:
     ```python
     path('dashboard/logging/', include('logging_app.urls', namespace='logging')),
     ```
   - This line includes the URLs of the `logging` app under the namespace `'logging'` within the path `'dashboard/logging/'`.

4. **Database Migration**:
   - Run database migrations to create the necessary tables for the `logging_app` models:
     ```
     python manage.py makemigrations logging_app
     python manage.py migrate
     ```

5. **Middleware Setup**:
   - Ensure that the `LogMiddleware` is included in your project's middleware stack. Add `'logging_app.middleware.LogMiddleware'` to the `MIDDLEWARE` list in your project's `settings.py` file.

6. **Templates and Static Files**:
   - Ensure that the necessary templates and static files for the **logging_app** are properly configured and accessible within your project.

7. **Usage**:
   - Once configured, the **logging_app** will automatically start logging access and errors within your Django project. Visit the provided URLs to view the access and error logs, graphs, and detailed log information. To access it, the accordion should extend the accordion of the website app. the website app provide the base.html and dashboard.html that the templates in this app extends

With these steps completed, the **logging_app** will be integrated into your Django project, providing comprehensive monitoring and logging capabilities for your application.


## Models

### `Log`

This model represents a generic log of an action or event in the system.

#### Fields:
- `ip_address` (CharField): IP address from which the request was made.
- `timestamp` (DateTimeField): Date and time when the event occurred.
- `request_path` (CharField): Path of the request.
- `request_method` (CharField): HTTP method of the request.
- `response_code` (PositiveIntegerField): Response code of the request.

### `AccessLog`

Subclass of the `Log` model. Represents an access log.

### `ErrorLog`

Subclass of the `Log` model. Represents an error log.

#### Additional fields:
- `error_message` (TextField): Error message.
- `stack_trace` (TextField): Stack trace in case of error.


## Middleware 

### `LogMiddleware`

Middleware responsible for logging access and errors in the application.

#### Initialization:
- `__init__(self, get_response)`: Initializes the middleware with the `get_response` function to handle subsequent HTTP requests.

#### Methods:
- `__call__(self, request)`: Method called for each incoming HTTP request. Registers an access log for the server and captures any exceptions. Access logs are saved as `AccessLog` objects in the database. Additionally, this method checks if the user's IP address is present in the database to determine whether the user has given consent to log their IP address. If the IP address is not present, the user is redirected to a consent view to provide consent.
- `process_exception(self, request, exception)`: Method called only if an exception occurs during request processing. Captures the exception and logs the error. Error logs are saved as `ErrorLog` objects in the database.

#### Attributes:
- `LOGGING_PATH_PREFIX`: Tuple containing paths to be excluded from logging (e.g., '/logging/', '/static/').
- `LOGGING_PATH_POSTFIX`: Tuple containing file extensions to be excluded from logging (e.g., 'js', 'json', 'css').


## Views

### `GraphsView`

View responsible for rendering the dashboard page with various graphs and charts.

#### Methods:
- `get(self, request)`: Retrieves data for errors, access logs, and response codes. Renders the dashboard template with the necessary data for displaying graphs.

### `IPListView`

View responsible for rendering the IP list page.

#### Methods:
- `get(self, request)`: Retrieves access logs and renders the IP list template with the necessary data.

### `AEListView`

View responsible for rendering the access log and error log list page.

#### Methods:
- `get(self, request)`: Retrieves access logs and error logs and renders the access/error log list template with the necessary data.

### `AccessLogDetailView`

View responsible for rendering the details of a specific access log.

#### Methods:
- `get(self, request, log_id)`: Retrieves the specific access log identified by `log_id` and renders the log detail template with the log's data.

### `ErrorLogDetailView`

View responsible for rendering the details of a specific error log.

#### Methods:
- `get(self, request, log_id)`: Retrieves the specific error log identified by `log_id` and renders the log detail template with the log's data.

Ecco la documentazione aggiornata relativa alla nuova vista `ConsentView`:


### `ConsentView`

View responsible for rendering the consent form for data processing in compliance with European privacy laws.

#### Methods:
- `get(self, request)`: Renders the consent form template, presenting users with information about data processing consent required by European privacy laws. Users are provided with options to give or decline consent.
- `post(self, request)`: Handles form submission. If the user gives consent, the access is logged in the database, and the user is redirected to the home page. If the user declines consent, they are redirected to Google.


## URLs

### `logging_app` URLs

#### Configuration:
- Add the following line inside the URL patterns of the base project's URLs file:
  ```python
  path('dashboard/logging/', include('logging.urls', namespace='logging')),
  ```
  This line includes the URLs of the `logging` app under the namespace `'logging'` within the path `'dashboard/logging/'`.

#### Paths:
- `graphs/`: URL to access the graphs page.
- `Access-ErrorList/`: URL to access the access and error log list page.
- `IPList/`: URL to access the IP list page.
- `log/access/<int:log_id>/`: URL pattern to view the details of a specific access log.
- `log/error/<int:log_id>/`: URL pattern to view the details of a specific error log.

