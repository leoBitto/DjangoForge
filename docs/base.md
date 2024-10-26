# DjangoForge Base Project

[Back to index]({{ site.baseurl }})

The **Base Project** is the foundation of the DjangoForge ecosystem, providing core functionalities and common applications that are essential for the entire platform. This document will guide you through the different components of the Base Project, including their purpose, structure, and how they can be extended.

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Backoffice App](#backoffice-app)
    - [Purpose](#purpose)
    - [Structure](#structure)
    - [Key Features](#key-features)
4. [Base App](#base-app)
    - [Purpose](#purpose-1)
    - [Structure](#structure-1)
    - [Key Configurations in `settings.py`](#key-configurations-in-settingspy)
5. [Gold BI App](#gold-bi-app)
    - [Purpose](#purpose-2)
    - [Structure](#structure-2)
    - [Key Features](#key-features-1)
    - [Development Protocol](#development-protocol)
    - [Q_CLUSTER Configuration](#q_cluster-configuration)
6. [Logging App](#logging-app)
    - [Purpose](#purpose-3)
    - [Structure](#structure-3)
    - [Key Features](#key-features-2)
    - [LOGGING Configuration](#logging-configuration)
    - [Integration with Gold BI](#integration-with-gold-bi)
7. [Website App](#website-app)
    - [Purpose](#purpose-4)
    - [Structure](#structure-4)
    - [Key Features](#key-features-3)
8. [Extending the Base Project](#extending-the-base-project)

## Overview

The Base Project contains several essential Django apps that provide core functionalities such as administration, business intelligence, logging, and website management.

## Project Structure

```bash
src
├── backoffice
├── base
├── gold_bi
├── logging_app
└── website
```


## Backoffice App

### Purpose

The **Backoffice App** provides the tools and interfaces necessary for backend management and data visualization. It serves as the administrative hub where users can manage various aspects of the platform, such as user roles, content, and reports.

### Structure

- **`admin.py`**: Configures the Django admin interface for the Backoffice.
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

### Key Features

- **Backoffice Interface**: Customize and manage different aspects of the DjangoForge ecosystem from a centralized backend.
- **Report presentation**: Generate business reports with customizable aggregation and filtering options.

## Base App

### Purpose

The **Base App** contains the core settings and configurations that are shared across all other applications in DjangoForge. It serves as the foundation upon which the entire ecosystem is built.

### Structure

- **`asgi.py`**: Configures ASGI for asynchronous server connections.
- **`__init__.py`**: Initializes the app and its settings.
- **`settings.py`**: Core settings file that includes configuration for databases, installed apps, middleware, and more.
- **`urls.py`**: Main URL routing configuration for the project.
- **`wsgi.py`**: Configures WSGI for handling HTTP requests in a production environment. this is used by Gunicorn.

```bash
├── base
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
```

### Key Configurations in `settings.py`

#### PWA Configuration

DjangoForge is designed to support Progressive Web Apps (PWAs), allowing your application to function like a native app on mobile devices. The following settings configure the PWA features:

- **`PWA_APP_NAME`**: The name of your PWA, displayed when the app is installed on a user's device.
- **`PWA_APP_DESCRIPTION`**: A brief description of your PWA's functionality.
- **`PWA_APP_THEME_COLOR`**: The color of the app's theme, which affects the browser's UI when the PWA is launched.
- **`PWA_APP_BACKGROUND_COLOR`**: The background color of the splash screen when the app is launched.
- **`PWA_APP_DISPLAY`**: Determines how the PWA is displayed, with `'standalone'` making it look like a native app without browser UI elements.
- **`PWA_APP_SCOPE`**: The URL scope that the PWA is allowed to control.
- **`PWA_APP_ORIENTATION`**: Specifies the orientation in which the app should be displayed.
- **`PWA_APP_START_URL`**: The URL that the PWA opens when launched.
- **`PWA_APP_STATUS_BAR_COLOR`**: Color of the status bar in the app.
- **`PWA_APP_ICONS`**: A list of icons used by the PWA in various resolutions.
- **`PWA_APP_SPLASH_SCREEN`**: Configuration for the splash screen images that are shown when the app is launched.

These settings enable your DjangoForge app to provide a consistent and native-like experience on mobile devices, improving user engagement.

#### WebPush Configuration

WebPush notifications allow you to send real-time notifications to users even when they are not actively using the app. The following settings configure WebPush with VAPID keys:

- **`VAPID_PUBLIC_KEY`**: The public key used for sending WebPush notifications. Stored securely using environment variables.
- **`VAPID_PRIVATE_KEY`**: The private key associated with the public key for secure communication.
- **`VAPID_ADMIN_EMAIL`**: The email address of the administrator, included in the VAPID authentication.

These settings are critical for enabling push notifications in DjangoForge, allowing you to keep users informed with timely updates.

## Gold BI App

### Purpose

The **Gold BI App** is responsible for providing basic models that should be extended, they provide the base for temporal aggregations. provide the forms used by other apps to choose the report temporal aggregations. More importantly it must be used to schedule the tasks provided by the tier 1 and tier 2 apps.

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

```bash
├── gold_bi
│   ├── apps.py
│   ├── docs
│   ├── models.py
│   ├── signals.py
│   ├── tasks_scheduler.py
│   ├── templates
│   └── tests.py
```

### Key Features

- **ETL Scheduling**: schedules the various tasks
- **BI Reporting**: Provides tools and templates for generating detailed business intelligence reports.

### Development Protocol

1. **Create the models inside the tier 1 and tier 2 apps**: they should be inside the aggregated file inside models folder.
2. **Create the views inside tier 1 and tier 2**: they should be inside the aggregated file inside the views folde, they provide the data extraction and creation of the report. every report type should handle all the relative temporal aggregation. every report type should have a view associated. 
3. **Create the templates for the report**: create the report template to create the dashboard.
4. **Create the tasks**: Create the task reading from the deault db, and wrte in the gold db.
5. **Schedule Tasks**: Create the task schedulation, one for every temporal aggregation

### Q_CLUSTER Configuration

The Gold BI App uses Django Q for managing task scheduling, which is crucial for handling ETL operations. The following settings configure Django Q:

- **`name`**: Specifies the name of the Q cluster, in this case, `'gold_bi'`.
- **`workers`**: The number of worker processes that will handle tasks.
- **`recycle`**: Determines how often workers are recycled to prevent memory leaks.
- **`timeout`**: Maximum time (in seconds) that a task can run before being terminated.
- **`django_redis`**: Specifies the Redis instance used for task queuing.
- **`retry`**: Time (in seconds) to wait before retrying a failed task.
- **`queue_limit`**: Maximum number of tasks that can be queued at once.
- **`bulk`**: Number of tasks to process in a single batch.
- **`orm`**: Specifies which ORM to use, typically `'default'` for Django’s default ORM.

This configuration ensures that the Gold BI App can efficiently manage task execution, handling everything from data processing to report generation.

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

```bash
├── logging_app
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── middleware.py
│   ├── models
│   ├── tasks
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views
```

### Key Features

- **Request and Error Logging**: Tracks HTTP requests and errors, providing detailed logs for analysis.
- **Log Presentation**: Show log data to facilitate easier monitoring and reporting.

### LOGGING Configuration

The `LOGGING` settings in `settings.py` control how log data is captured and stored. DjangoForge uses these settings to ensure that logs are properly categorized and easily accessible:

- **Formatters**:
    - **`verbose`**: Defines a detailed logging format, including timestamp, logger name, log level, file path, and function name.
- **Handlers**:
    - **`file_schedules`**: Logs schedule-related information to `schedules.log`.
    - **`file_tasks`**: Logs task-related information to `tasks.log`.
    - **`file_reports`**: Logs report-related information to `reports.log`.
- **Loggers**:
    - **`schedules`**: Uses the `file_schedules` handler to log information about scheduling tasks.
    - **`tasks`**: Uses the `file_tasks` handler to log task execution details.
    - **`reports`**: Uses the `file_reports` handler to log report generation events.

These configurations ensure that logs are systematically stored and can be easily monitored, providing a clear overview of the system's operations.

### Integration with Gold BI

the read logs tab is used to read the various log files:
- tasks
- reports
- schedules

## Website App

### Purpose

The **Website App** manages the front-end of the DjangoForge site.

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

```bash
└── website
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── static
    ├── templates
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

