import logging
from django_q.tasks import schedule, Schedule
from django.utils import timezone

logger = logging.getLogger('app')

def schedule_tasks():
    try:
        if not Schedule.objects.filter(func='logging_app.tasks.aggregate_access_logs.aggregate_access_logs').exists():
            schedule(
                'logging_app.tasks.aggregate_access_logs.aggregate_access_logs',
                schedule_type=Schedule.HOURLY,
                #minutes=30,
                repeats=-1,
                next_run=timezone.now() + timezone.timedelta(seconds=30),
                cluster='gold_bi'
            )
            logger.info("Scheduled aggregate_access_logs task")

        if not Schedule.objects.filter(func='logging_app.tasks.aggregate_error_logs.aggregate_error_logs').exists():
            schedule(
                'logging_app.tasks.aggregate_error_logs.aggregate_error_logs',
                schedule_type=Schedule.HOURLY,
                #minutes=30,
                repeats=-1,
                next_run=timezone.now() + timezone.timedelta(seconds=30),
                cluster='gold_bi'
            )
            logger.info("Scheduled aggregate_error_logs task")



    except Exception as e:
        logger.error("Error scheduling tasks: %s", e)
