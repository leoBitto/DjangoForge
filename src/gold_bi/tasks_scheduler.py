import logging
from django_q.tasks import schedule, Schedule
from django.utils import timezone

logger = logging.getLogger('app')

def schedule_tasks():
    try:
        now = timezone.now()

        def get_next_run_for_schedule(schedule_type):
            if schedule_type == Schedule.DAILY:
                return (now + timezone.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            elif schedule_type == Schedule.WEEKLY:
                days_until_next_sunday = 6 - now.weekday()
                return (now + timezone.timedelta(days=days_until_next_sunday)).replace(hour=0, minute=0, second=0, microsecond=0)
            elif schedule_type == Schedule.MONTHLY:
                next_month_start = now.replace(day=1) + timezone.timedelta(days=32)
                return next_month_start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            elif schedule_type == Schedule.CRON and "1,4,7,10" in cron:
                # Quarterly: Next quarter start (1st of April, July, October, or January)
                month = (now.month - 1) // 3 * 3 + 4
                if month > 12:
                    month = 1
                    year = now.year + 1
                else:
                    year = now.year
                return now.replace(year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
            elif schedule_type == Schedule.YEARLY:
                next_year_start = now.replace(year=now.year + 1, month=1, day=1)
                return next_year_start.replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                raise ValueError("Unsupported schedule type")

        def schedule_task(func_path, schedule_type, cron=None, cluster='gold_bi'):
            next_run = get_next_run_for_schedule(schedule_type)
            if not Schedule.objects.filter(func=func_path).exists():
                schedule(
                    func_path,
                    schedule_type=schedule_type,
                    next_run=next_run,
                    cron=cron,
                    repeats=-1,
                    cluster=cluster
                )
                logger.info(f"Scheduled {func_path} task for {next_run}")

        # Schedulazione delle aggregazioni di log
        schedule_task('logging_app.tasks.aggregate_access_logs.aggregate_access_logs', 
                      Schedule.HOURLY)

        schedule_task('logging_app.tasks.aggregate_error_logs.aggregate_error_logs', 
                      Schedule.HOURLY)

        # Aggregazioni Vendite
        schedule_task('inventory.tasks.aggregate_sales_daily.aggregate_sales_daily', 
                      Schedule.DAILY)

        schedule_task('inventory.tasks.aggregate_sales_weekly.aggregate_sales_weekly', 
                      Schedule.WEEKLY)

        schedule_task('inventory.tasks.aggregate_sales_monthly.aggregate_sales_monthly', 
                      Schedule.MONTHLY)

        schedule_task('inventory.tasks.aggregate_sales_quarterly.aggregate_sales_quarterly', 
                      Schedule.CRON, 
                      cron='0 0 1 1,4,7,10 *')

        schedule_task('inventory.tasks.aggregate_sales_annually.aggregate_sales_annually', 
                      Schedule.YEARLY)

        # Aggregazioni Ordini
        schedule_task('inventory.tasks.aggregate_orders_daily.aggregate_orders_daily', 
                      Schedule.DAILY)

        schedule_task('inventory.tasks.aggregate_orders_weekly.aggregate_orders_weekly', 
                      Schedule.WEEKLY)

        schedule_task('inventory.tasks.aggregate_orders_monthly.aggregate_orders_monthly', 
                      Schedule.MONTHLY)

        schedule_task('inventory.tasks.aggregate_orders_quarterly.aggregate_orders_quarterly', 
                      Schedule.CRON, 
                      cron='0 0 1 1,4,7,10 *')

        schedule_task('inventory.tasks.aggregate_orders_annually.aggregate_orders_annually', 
                      Schedule.YEARLY)

        # Aggregazioni Inventario
        schedule_task('inventory.tasks.aggregate_inventory_quarter.aggregate_inventory_quarter', 
                      Schedule.CRON, 
                      cron='0 0 1 1,4,7,10 *')

        schedule_task('inventory.tasks.aggregate_inventory_annual.aggregate_inventory_annual', 
                      Schedule.YEARLY)

        # Aggregazioni Qualità Dati
        schedule_task('inventory.tasks.aggregate_quality_quarterly.aggregate_quality_quarterly', 
                      Schedule.CRON, 
                      cron='0 0 1 1,4,7,10 *')

        schedule_task('inventory.tasks.aggregate_quality_annually.aggregate_quality_annually', 
                      Schedule.YEARLY)

        # Aggregazioni Prodotti
        schedule_task('inventory.tasks.aggregate_product_monthly.aggregate_product_monthly', 
                      Schedule.MONTHLY)

        schedule_task('inventory.tasks.aggregate_product_quarterly.aggregate_product_quarterly', 
                      Schedule.CRON, 
                      cron='0 0 1 1,4,7,10 *')

        schedule_task('inventory.tasks.aggregate_product_annually.aggregate_product_annually', 
                      Schedule.YEARLY)

    except Exception as e:
        logger.error("Error scheduling tasks: %s", e, exc_info=True)
