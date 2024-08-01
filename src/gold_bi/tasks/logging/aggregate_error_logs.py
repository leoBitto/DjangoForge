import logging
from django.utils import timezone
from logging_app.models import ErrorLog
from gold_bi.models import AggregatedErrorLog
from django.db.models import Count, F
from django.db import transaction
from django.db.models.functions import ExtractHour, ExtractWeekDay

logger = logging.getLogger('gold_bi')

def aggregate_error_logs():
    try:
        now = timezone.now()
        start_time = now - timezone.timedelta(days=1)
        end_time = now

        # Aggregazione dei dati
        error_aggregations = ErrorLog.objects.using('default').filter(
            timestamp__gte=start_time, timestamp__lt=end_time
        ).annotate(
            hour=ExtractHour('timestamp'),
            day=ExtractWeekDay('timestamp')
        ).values('hour', 'day').annotate(
            count=Count('id')
        ).values('hour', 'day', 'count')

        # Aggiornamento dei risultati aggregati nel modello AggregatedErrorLog
        with transaction.atomic():
            for aggregation in error_aggregations:
                obj, created = AggregatedErrorLog.objects.using('gold').get_or_create(
                    hour=aggregation['hour'],
                    day=aggregation['day']
                )
                
                # Aggiorna il campo count in modo incrementale
                obj.count = F('count') + aggregation['count']
                obj.save()

        logger.info('Error logs aggregated successfully.')
    except Exception as e:
        logger.error('Error aggregating error logs: %s', e)
