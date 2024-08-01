from django.apps import AppConfig
import os
from django.conf import settings

class LoggingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logging_app'
