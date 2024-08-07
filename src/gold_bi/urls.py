from django.urls import path
from .views import *
# include the following line inside the urls of base
# path('dashboard/logging/', include('logging_app.urls', namespace='logging')),

app_name = 'goldBI'

urlpatterns = [
    path('logging_graphs/', AEGraphsView.as_view(), name='logging_graphs'),
    path('Access-ErrorList/', AEListView.as_view(), name='AElist'),
    path('log/access/<int:log_id>/', AccessLogDetailView.as_view(), name='access_log_detail'),  # URL per visualizzare i dettagli di un log
    path('log/error/<int:log_id>/', ErrorLogDetailView.as_view(), name='error_log_detail'),  # URL per visualizzare i dettagli di un log

    path('select-report/', ReportTypeSelectionView.as_view(), name='select_report_type'),
    path('monthly-snapshot/<int:year>/<int:month>/', MonthlySnapshotView.as_view(), name='monthly_snapshot'),
    path('quality-control/<int:year>/<int:month>/', QualityControlView.as_view(), name='quality_control'),
    path('temporal-aggregation/<str:aggregation_type>/<str:start_date>/<str:end_date>/', TemporalAggregationView.as_view(), name='temporal_aggregation'),

    
]