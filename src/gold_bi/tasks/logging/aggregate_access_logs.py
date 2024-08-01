import logging
from django.utils import timezone
from logging_app.models import AccessLog
from gold_bi.models import AggregatedAccessLog
from django.db.models import Count, F
from django.db import transaction
from django.db.models.functions import ExtractHour, ExtractWeekDay

logger = logging.getLogger('gold_bi')

def aggregate_access_logs():
    try:
        now = timezone.now()
        start_time = now - timezone.timedelta(days=1)
        end_time = now

        # Aggregazione dei dati
        access_aggregations = AccessLog.objects.using('default').filter(
            timestamp__gte=start_time, timestamp__lt=end_time
        ).annotate(
            hour=ExtractHour('timestamp'),
            day=ExtractWeekDay('timestamp')
        ).values('hour', 'day').annotate(
            count=Count('id')
        ).values('hour', 'day', 'count')

        # Aggiornamento dei risultati aggregati nel modello AggregatedAccessLog
        with transaction.atomic():
            for aggregation in access_aggregations:
                obj, created = AggregatedAccessLog.objects.using('gold').get_or_create(
                    hour=aggregation['hour'],
                    day=aggregation['day']
                )
                
                # Aggiorna il campo count in modo incrementale
                obj.count = F('count') + aggregation['count']
                obj.save()

        logger.info('Access logs aggregated successfully.')
    except Exception as e:
        logger.error('Error aggregating access logs: %s', e)
