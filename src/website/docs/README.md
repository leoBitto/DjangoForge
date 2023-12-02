
# Website

The **website** app is a Django application designed to manage basic web pages within a website.

## Quick Start

1. Add "website" to your `INSTALLED_APPS` in your Django project's settings:

   ```python
   INSTALLED_APPS = [
       ...
       'website',
   ]

    ```



2. Include the website URLconf in your project urls.py like this::
you may want to add some url path inside the ''

    > path('', include(('website.urls', 'website'), namespace="website")),

3. Run ``python manage.py migrate website`` to create the website models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create the models (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000 to see the website


-----------

# website docs                       
if you want to use the article links outside the app you need to use the namespace.
it is always a good idea when having many apps inside a Django project to use the namespace.
for example:

    > <a href="{% url 'website:URL'  %}"</a>


...

## User Registration

To enable user registration and authentication, follow these steps:

1. Add `'django.contrib.auth'` and `'django.contrib.auth.urls'` to your `INSTALLED_APPS` in your Django project's settings:

   ```python
   INSTALLED_APPS = [
       ...
       'django.contrib.auth',
       ...
   ]

2. Include the authentication URLconf in your **project**'s urls.py:


    >path('accounts/', include('django.contrib.auth.urls')),


Now, your website should have user registration and authentication functionality. For more advanced features, refer to the Django Authentication documentation.