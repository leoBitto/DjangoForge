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

        #CRM
        if not Schedule.objects.filter(func='crm.tasks.aggregate_crm.aggregate_crm_monthly').exists():
            schedule(
                'crm.tasks.aggregate_crm.aggregate_crm_monthly',
                schedule_type=Schedule.CRON,
                cron='59 23 L * *', 
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled monthly crm aggregation task")

        
        # INVENTORY GLOBAL
        if not Schedule.objects.filter(func='inventory.tasks.aggregate_inventory.aggregate_inventory_annually').exists():
            schedule(
                'inventory.tasks.aggregate_inventory.aggregate_inventory_annually',
                schedule_type=Schedule.CRON,
                cron='59 23 31 12 *',  
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled inventory annual aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_inventory.aggregate_inventory_quarterly').exists():
            schedule(
                'inventory.tasks.aggregate_inventory.aggregate_inventory_quarterly',
                schedule_type=Schedule.CRON,
                cron='59 23 L 3,6,9,12 *',  
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled inventory quarter aggregation task")


        # INVENTORY PRODUCT
        if not Schedule.objects.filter(func='inventory.tasks.aggregate_product.aggregate_product_annually').exists():
            schedule(
                'inventory.tasks.aggregate_product.aggregate_product_annually',
                schedule_type=Schedule.CRON,
                cron='59 23 31 12 *',
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled annual product aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_product.aggregate_product_quarterly').exists():
            schedule(
                'inventory.tasks.aggregate_product.aggregate_product_quarterly',
                schedule_type=Schedule.CRON,
                cron='59 23 L 3,6,9,12 *',
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled quarter product aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_product.aggregate_product_monthly').exists():
            schedule(
                'inventory.tasks.aggregate_product.aggregate_product_monthly',
                schedule_type=Schedule.CRON,
                cron='59 23 L * *',
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled monthly product aggregation task")

        # INVENTORY QUALITY
        if not Schedule.objects.filter(func='inventory.tasks.aggregate_quality.aggregate_quality_annually').exists():
            schedule(
                'inventory.tasks.aggregate_quality.aggregate_quality_annually',
                schedule_type=Schedule.CRON,
                cron='59 23 31 12 *',  # L'ultimo giorno dell'anno alle 23:59
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled annual quality aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_quality.aggregate_quality_quarterly').exists():
            schedule(
                'inventory.tasks.aggregate_quality.aggregate_quality_quarterly',
                schedule_type=Schedule.CRON,
                cron='59 23 L 3,6,9,12 *', 
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled quarterly quality aggregation task")

        # INVENTORY ORDERS
        if not Schedule.objects.filter(func='inventory.tasks.aggregate_orders.aggregate_orders_annually').exists():
            schedule(
                'inventory.tasks.aggregate_orders.aggregate_orders_annually',
                schedule_type=Schedule.CRON,
                cron='59 23 31 12 *',  # L'ultimo giorno dell'anno alle 23:59
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled annual orders aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_orders.aggregate_orders_quarterly').exists():
            schedule(
                'inventory.tasks.aggregate_orders.aggregate_orders_quarterly',
                schedule_type=Schedule.CRON,
                cron='59 23 L 3,6,9,12 *',  # L'ultimo giorno di marzo, giugno, settembre, e dicembre alle 23:59
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled quarterly orders aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_orders.aggregate_orders_monthly').exists():
            schedule(
                'inventory.tasks.aggregate_orders.aggregate_orders_monthly',
                schedule_type=Schedule.CRON,
                cron='59 23 L * *', 
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled monthly orders aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_orders.aggregate_orders_weekly').exists():
            schedule(
                'inventory.tasks.aggregate_orders.aggregate_orders_weekly',
                schedule_type=Schedule.CRON,
                cron='59 23 * * 0',  # L'ultimo giorno di marzo, giugno, settembre, e dicembre alle 23:59
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled weekly orders aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_orders.aggregate_orders_daily').exists():
            schedule(
                'inventory.tasks.aggregate_orders.aggregate_orders_daily',
                schedule_type=Schedule.CRON,
                cron='59 23 * * *', 
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled daily orders aggregation task")
  

        # INVENTORY SALES
        if not Schedule.objects.filter(func='inventory.tasks.aggregate_sales.aggregate_sales_annually').exists():
            schedule(
                'inventory.tasks.aggregate_sales.aggregate_sales_annually',
                schedule_type=Schedule.CRON,
                cron='59 23 31 12 *',  # L'ultimo giorno dell'anno alle 23:59
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled annual sales aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_sales.aggregate_sales_quarterly').exists():
            schedule(
                'inventory.tasks.aggregate_sales.aggregate_sales_quarterly',
                schedule_type=Schedule.CRON,
                cron='59 23 L 3,6,9,12 *',  # L'ultimo giorno di marzo, giugno, settembre, e dicembre alle 23:59
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled quarterly sales aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_sales.aggregate_sales_monthly').exists():
            schedule(
                'inventory.tasks.aggregate_sales.aggregate_sales_monthly',
                schedule_type=Schedule.CRON,
                cron='59 23 L * *',
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled monthly sales aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_sales.aggregate_sales_weekly').exists():
            schedule(
                'inventory.tasks.aggregate_sales.aggregate_sales_weekly',
                schedule_type=Schedule.CRON,
                cron='59 23 * * 0', 
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled weekly sales aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_sales.aggregate_sales_daily').exists():
            schedule(
                'inventory.tasks.aggregate_sales.aggregate_sales_daily',
                schedule_type=Schedule.CRON,
                cron='59 23 * * *',  # L'ultimo giorno di marzo, giugno, settembre, e dicembre alle 23:59
                repeats=-1,
                cluster='gold_bi'
            )
            logger.info("Scheduled daily sales aggregation task")


        




    except Exception as e:
        logger.error("Error scheduling tasks: %s", e, exc_info=True)
