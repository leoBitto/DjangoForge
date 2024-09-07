import logging
from django_q.tasks import schedule, Schedule

logger = logging.getLogger('schedules')

def schedule_tasks():
    """
    Questo file utilizza la sintassi CRON per schedulare le task.

    La sintassi CRON è composta da 5 campi separati da spazi:
    ┌───────────── min (0 - 59)
    │ ┌───────────── ora (0 - 23)
    │ │ ┌───────────── giorno del mese (1 - 31)
    │ │ │ ┌───────────── mese (1 - 12)
    │ │ │ │ ┌───────────── giorno della settimana (0 - 6) (Domenica = 0)
    │ │ │ │ │
    │ │ │ │ │
    * * * * * comando da eseguire

    Esempi di sintassi CRON utilizzati:
    - `59 23 * * *` : Ogni giorno alle 23:59.
    - `0 * * * *` : Ogni ora all'inizio dell'ora (es: 14:00, 15:00).
    - `59 23 * * 0` : Ogni domenica alle 23:59.
    - `59 23 L * *`,  : Ultimo giorno del mese alle 23:59.
    - `59 23 L 3,6,9,12 *` : L'ultimo giorno di marzo, giugno, settembre, e dicembre alle 23:59.
    - `59 23 31 12 *` : L'ultimo giorno dell'anno (31 dicembre) alle 23:59.
    """

    try:
        # Aggregazione Access
        if not Schedule.objects.filter(func='logging_app.tasks.aggregate_access_logs.aggregate_access_logs').exists():
            schedule(
                'logging_app.tasks.aggregate_access_logs.aggregate_access_logs',
                schedule_type=Schedule.CRON,
                cron='0 * * * *',  # Ogni ora all'inizio dell'ora
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled hourly aggregate_access_logs task")

        if not Schedule.objects.filter(func='logging_app.tasks.aggregate_error_logs.aggregate_error_logs').exists():
            schedule(
                'logging_app.tasks.aggregate_error_logs.aggregate_error_logs',
                schedule_type=Schedule.CRON,
                cron='0 * * * *',  # Ogni ora all'inizio dell'ora
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled hourly aggregate_error_logs task")

 



    except Exception as e:
        logger.error("Error scheduling tasks: %s", e, exc_info=True)
