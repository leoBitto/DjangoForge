from django.urls import path, include

from .views import *

app_name= 'backoffice'

urlpatterns = [
    path('', dashboard, name="backoffice"),
    path('select-report/', SelectReportTypeView.as_view(), name='select_report_type'),

]
