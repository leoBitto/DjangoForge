from django.urls import path, include

from .views import *

app_name= 'backoffice'

urlpatterns = [
    path('', dashboard, name="backoffice"),
    path('select-report/', select_report_type, name='select_report_type'),
    path('report/<str:report_type>/', view_report, name='view_report'),

]
