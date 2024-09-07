# DjangoForge Base Project

The **Base Project** is the foundation of the DjangoForge ecosystem, providing core functionalities and common applications that are essential for the entire platform. This document will guide you through the different components of the Base Project, including their purpose, structure, and how they can be extended.

## Table of Contents

1. [Overview](#overview)
2. [Backoffice App](#backoffice-app)
    - [Purpose](#purpose)
    - [Structure](#structure)
    - [Key Features](#key-features)
3. [Base App](#base-app)
    - [Purpose](#purpose-1)
    - [Structure](#structure-1)
4. [Gold BI App](#gold-bi-app)
    - [Purpose](#purpose-2)
    - [Structure](#structure-2)
    - [Key Features](#key-features-1)
5. [Logging App](#logging-app)
    - [Purpose](#purpose-3)
    - [Structure](#structure-3)
    - [Key Features](#key-features-2)
6. [Website App](#website-app)
    - [Purpose](#purpose-4)
    - [Structure](#structure-4)
    - [Key Features](#key-features-3)
7. [Extending the Base Project](#extending-the-base-project)

## Overview

The Base Project contains several essential Django apps that provide core functionalities such as administration, business intelligence, logging, and website management. These apps are designed to be modular and scalable, allowing developers to build upon them and create complex business solutions tailored to various industries.

## project structure
```
src
├── backoffice
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── templates
│   │   └── backoffice
│   │       ├── backoffice_base.html
│   │       └── reports
│   │           ├── select_aggregation.html
│   │           └── select_report_type.html
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── base
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Dockerfile
├── gold_bi
│   ├── apps.py
│   ├── docs
│   │   ├── assets
│   │   │   └── images
│   │   │       └── logo.png
│   │   └── README.md
│   ├── __init__.py
│   ├── models.py
│   ├── signals.py
│   ├── tasks_scheduler.py
│   ├── templates
│   │   └── gold_bi
│   │       └── report
│   │           ├── monthly_snapshot.html
│   │           ├── quality_control.html
│   │           └── temporal_aggregation.html
│   └── tests.py
├── logging_app
│   ├── admin.py
│   ├── apps.py
│   ├── docs
│   │   ├── assets
│   │   │   └── logo.png
│   │   ├── _config.yml
│   │   └── README.md
│   ├── forms.py
│   ├── __init__.py
│   ├── middleware.py
│   ├── models
│   │   ├── aggregated.py
│   │   ├── base.py
│   │   └── __init__.py
│   ├── tasks
│   │   ├── aggregate_access_logs.py
│   │   ├── aggregate_error_logs.py
│   │   └── __init__.py
│   ├── templates
│   │   └── logging_app
│   │       ├── accordion.html
│   │       ├── AElist.html
│   │       ├── graphs.html
│   │       ├── log_list.html
│   │       └── request_log_detail.html
│   ├── tests.py
│   ├── urls.py
│   └── views
│       ├── aggregated.py
│       ├── base.py
│       └── __init__.py
├── manage.py
├── requirements.txt
└── website
    ├── admin.py
    ├── apps.py
    ├── docs
    │   └── README.md
    ├── forms.py
    ├── __init__.py
    ├── models.py
    ├── static
    │   ├── favicon
    │   │   ├── 16DjangoForge.ico
    │   │   └── 48DjangoForge.ico
    │   ├── icons
    │   │   ├── github.svg
    │   │   └── linkedin.svg
    │   └── pwa
    │       └── icons
    │           ├── icon-256x256.png
    │           └── Icon-512x512.png
    ├── templates
    │   ├── registration
    │   │   ├── login.html
    │   │   ├── logout.html
    │   │   └── password_reset.html
    │   └── website
    │       ├── base.html
    │       ├── footer.html
    │       ├── landing.html
    │       └── navbar.html
    ├── tests.py
    ├── urls.py
    └── views.py
```

## Backoffice App

### Purpose

The **Backoffice App** provides the tools and interfaces necessary for backend management and data visualization. It serves as the administrative hub where users can manage various aspects of the platform, such as user roles, content, and reports.

### Structure

- **`admin.py`**: Configures the admin interface for the Backoffice.
- **`apps.py`**: Registers the Backoffice app with Django.
- **`forms.py`**: Contains form classes used in the backend interface.
- **`models.py`**: Defines the database models for the backoffice features.
- **`templates/backoffice`**: Contains HTML templates for rendering the backoffice views.
    - **`backoffice_base.html`**: Base template for the backoffice UI.
    - **`reports/`**: Templates for generating and selecting reports.
        - **`select_aggregation.html`**: UI for selecting data aggregation options.
        - **`select_report_type.html`**: UI for choosing the report type.
- **`tests.py`**: Contains test cases for the Backoffice app.
- **`urls.py`**: Defines URL routing for the Backoffice views.
- **`utils.py`**: Utility functions used throughout the Backoffice app.
- **`views.py`**: Handles the logic for rendering the backoffice pages.

```
├── backoffice
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── templates
│   │   └── backoffice
│   │       ├── backoffice_base.html
│   │       └── reports
│   │           ├── select_aggregation.html
│   │           └── select_report_type.html
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
```

### Key Features

- **Admin Interface**: Customize and manage different aspects of the DjangoForge ecosystem from a centralized backend.
- **Report Generation**: Generate business reports with customizable aggregation and filtering options.

## Base App

### Purpose

The **Base App** contains the core settings and configurations that are shared across all other applications in DjangoForge. It serves as the foundation upon which the entire ecosystem is built.

### Structure

- **`asgi.py`**: Configures ASGI for asynchronous server connections.
- **`__init__.py`**: Initializes the app and its settings.
- **`settings.py`**: Core settings file that includes configuration for databases, installed apps, middleware, and more.
- **`urls.py`**: Main URL routing configuration for the project.
- **`wsgi.py`**: Configures WSGI for handling HTTP requests in a production environment.

```
├── base
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
```

### Key Features

- **Central Configuration**: Provides centralized settings and configuration options that are inherited by all other apps.
- **URL Routing**: Establishes the main routes and includes URLs from other applications.

## Gold BI App

### Purpose

The **Gold BI App** is responsible for business intelligence operations within DjangoForge. It manages ETL (Extract, Transform, Load) processes and provides scheduling capabilities using Django Q.

### Structure

- **`apps.py`**: Registers the Gold BI app.
- **`docs/`**: Contains documentation related to the Gold BI app.
    - **`assets/`**: Images and other assets used in documentation.
- **`models.py`**: Defines data models for storing business intelligence information.
- **`signals.py`**: Manages Django signals for tasks such as data processing triggers.
- **`tasks_scheduler.py`**: Handles task scheduling for ETL processes using Django Q.
- **`templates/gold_bi/report`**: HTML templates for generating BI reports.
    - **`monthly_snapshot.html`**: Template for monthly reports.
    - **`quality_control.html`**: Template for quality control reports.
    - **`temporal_aggregation.html`**: Template for reports based on temporal data aggregation.
- **`tests.py`**: Contains test cases for the Gold BI app.

```
├── gold_bi
│   ├── apps.py
│   ├── docs
│   │   ├── assets
│   │   │   └── images
│   │   │       └── logo.png
│   │   └── README.md
│   ├── __init__.py
│   ├── models.py
│   ├── signals.py
│   ├── tasks_scheduler.py
│   ├── templates
│   │   └── gold_bi
│   │       └── report
│   │           ├── monthly_snapshot.html
│   │           ├── quality_control.html
│   │           └── temporal_aggregation.html
│   └── tests.py
```

### Key Features

- **ETL Management**: Handles data extraction, transformation, and loading processes.
- **BI Reporting**: Provides tools and templates for generating detailed business intelligence reports.

## Logging App

### Purpose

The **Logging App** is designed to track and aggregate logs related to HTTP requests and errors. It is crucial for monitoring application health and troubleshooting issues.

### Structure

- **`admin.py`**: Configures the admin interface for managing logs.
- **`apps.py`**: Registers the Logging App with Django.
- **`forms.py`**: Contains form classes for filtering and displaying logs.
- **`middleware.py`**: Implements middleware for capturing request and error logs.
- **`models/`**: Defines models for storing and aggregating log data.
    - **`aggregated.py`**: Models for aggregated log data.
    - **`base.py`**: Base log models for HTTP requests and errors.
- **`tasks/`**: Contains tasks for aggregating log data.
    - **`aggregate_access_logs.py`**: Aggregates HTTP access logs.
    - **`aggregate_error_logs.py`**: Aggregates error logs.
- **`templates/logging_app/`**: HTML templates for displaying log data.
    - **`accordion.html`**: UI component for expandable log details.
    - **`AElist.html`**: List view for access and error logs.
    - **`graphs.html`**: Visual representation of log data.
    - **`log_list.html`**: General list view for logs.
    - **`request_log_detail.html`**: Detailed view for a single request log.
- **`tests.py`**: Contains test cases for the Logging App.
- **`urls.py`**: Defines URL routing for log views.
- **`views/`**: Handles logic for rendering log-related views.
    - **`aggregated.py`**: Views for aggregated logs.
    - **`base.py`**: Base views for log display.

```
├── logging_app
│   ├── admin.py
│   ├── apps.py
│   ├── docs
│   │   ├── assets
│   │   │   └── logo.png
│   │   ├── _config.yml
│   │   └── README.md
│   ├── forms.py
│   ├── __init__.py
│   ├── middleware.py
│   ├── models
│   │   ├── aggregated.py
│   │   ├── base.py
│   │   └── __init__.py
│   ├── tasks
│   │   ├── aggregate_access_logs.py
│   │   ├── aggregate_error_logs.py
│   │   └── __init__.py
│   ├── templates
│   │   └── logging_app
│   │       ├── accordion.html
│   │       ├── AElist.html
│   │       ├── graphs.html
│   │       ├── log_list.html
│   │       └── request_log_detail.html
│   ├── tests.py
│   ├── urls.py
│   └── views
│       ├── aggregated.py
│       ├── base.py
│       └── __init__.py
```

### Key Features

- **Request and Error Logging**: Tracks HTTP requests and errors, providing detailed logs for analysis.
- **Log Aggregation**: Aggregates log data to facilitate easier monitoring and reporting.

## Website App

### Purpose

The **Website App** manages the front-end of the DjangoForge site, acting as a simple CMS for rendering static or near-static HTML pages.

### Structure

- **`admin.py`**: Configures the admin interface for the Website App.
- **`apps.py`**: Registers the Website App with Django.
- **`forms.py`**: Contains form classes for user authentication and registration.
- **`models.py`**: Defines models related to website content and user management.
- **`static/`**: Contains static assets like images, icons, and CSS files.
    - **`favicon/`**: Favicon files for the site.
    - **`icons/`**: Social media and other icons.
    - **`pwa/`**: Icons for Progressive Web App support.
- **`templates/website`**: HTML templates for the site’s front-end.
    - **`base.html`**: Base template for the website.
    - **`footer.html`**: Footer section template.
    - **`landing.html`**: Landing page template.
    - **`navbar.html`**: Navigation bar template.
- **`tests.py`**: Contains test cases for the Website App.
- **`urls.py`**: Defines URL routing for the website.
- **`views.py`**: Handles logic for rendering front-end views.

```
└── website
    ├── admin.py
    ├── apps.py
    ├── docs
    │   └── README.md
    ├── forms.py
    ├── __init__.py
    ├── models.py
    ├── static
    │   ├── favicon
    │   │   ├── 16DjangoForge.ico
    │   │   └── 48DjangoForge.ico
    │   ├── icons
    │   │   ├── github.svg
    │   │   └── linkedin.svg
    │   └── pwa
    │       └── icons
    │           ├── icon-256x256.png
    │           └── Icon-512x512.png
    ├── templates
    │   ├── registration
    │   │   ├── login.html
    │   │   ├── logout.html
    │   │   └── password_reset.html
    │   └── website
    │       ├── base.html
    │       ├── footer.html
    │       ├── landing.html
    │       └── navbar.html
    ├── tests.py
    ├── urls.py
    └── views.py
```

### Key Features

- **Static Content Management**: Manages the content and layout of the website’s static pages.
- **User Authentication**: Provides templates and views for user login, logout, and password management.

## Extending the Base Project

The Base Project is designed to be extended and customized according to your specific business needs. You can add new applications, modify existing ones, or create custom modules that integrate seamlessly with the existing structure. Refer to the [Advanced Topics](docs/advanced.md) section for detailed guidance on how to extend and customize DjangoForge.

---

This concludes the overview of the DjangoForge Base Project. For more detailed instructions on how to use and extend these applications, please refer to the specific sections linked above.
