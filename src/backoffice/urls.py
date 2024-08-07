from django.urls import path, include
from . import views

app_name= 'backoffice'

urlpatterns = [
    path('', views.dashboard, name="backoffice"),


]
