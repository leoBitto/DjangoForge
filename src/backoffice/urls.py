from django.urls import path, include

from .views import *

app_name= 'backoffice'

urlpatterns = [
    path('', dashboard, name="backoffice"),
    path('select-report/', ReportTypeSelectionView.as_view(), name='select_report_type'),
    path('monthly-snapshot/<int:year>/<int:month>/', MonthlySnapshotView.as_view(), name='monthly_snapshot'),
    path('quality-control/<int:year>/<int:month>/', QualityControlView.as_view(), name='quality_control'),
    path('temporal-aggregation/<str:aggregation_type>/<str:start_date>/<str:end_date>/', TemporalAggregationView.as_view(), name='temporal_aggregation'),


]
