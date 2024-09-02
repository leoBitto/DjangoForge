import logging
from django_q.tasks import schedule, Schedule
from django.utils import timezone
import datetime as dt

logger = logging.getLogger('app')

def schedule_tasks():
    try:
        now = timezone.now()
        if now.month == 12:
            next_month_start = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            next_month_start = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)


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
                #next_run=timezone.now() + timezone.timedelta(seconds=50),
                cluster='gold_bi'
            )
            logger.info("Scheduled aggregate_error_logs task")

        # inventory Aggregation
        if not Schedule.objects.filter(func='inventory.tasks.aggregate_inventory.aggregate_inventory_quarter').exists():
            schedule(
                'inventory.tasks.aggregate_inventory.aggregate_inventory_quarter',
                schedule_type=Schedule.DAILY,
                repeats=-1,
                #next_run=now.replace(hour=0, minute=0, second=0, microsecond=0),
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled quarter inventory aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_inventory.aggregate_inventory_annual').exists():
            schedule(
                'inventory.tasks.aggregate_inventory.aggregate_inventory_annual',
                schedule_type=Schedule.WEEKLY,
                repeats=-1,
                #next_run= (now + timezone.timedelta(days=(6 - now.weekday()))).replace(hour=22, minute=0, second=0, microsecond=0),  # Next Sunday
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled weekly inventory aggregation task")

        # order Aggregation
        if not Schedule.objects.filter(func='inventory.tasks.aggregate_orders.aggregate_orders_daily').exists():
            schedule(
                'inventory.tasks.aggregate_orders.aggregate_orders_daily',
                schedule_type=Schedule.MONTHLY,
                repeats=-1,
                #next_run= next_month_start,  # First of next month
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled monthly inventory aggregation task")
       
        if not Schedule.objects.filter(func='inventory.tasks.aggregate_orders.aggregate_orders_weekly').exists():
            schedule(
                'inventory.tasks.aggregate_orders.aggregate_orders_weekly',
                schedule_type=Schedule.CRON,
                cron='0 0 1 1,4,7,10 *',  # Example: First day of Jan, Apr, Jul, and Oct
                repeats=-1,
                #next_run=now.replace(month=(now.month - 1) // 3 * 3 + 4, day=1, hour=0, minute=0, second=0, microsecond=0),  # First of next quarter
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled quarterly inventory aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_orders.aggregate_orders_monthly').exists():
            schedule(
                'inventory.tasks.aggregate_orders.aggregate_orders_monthly',
                schedule_type=Schedule.YEARLY,
                repeats=-1,
                #next_run=now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0) + timezone.timedelta(days=365),  # First of next year
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled yearly inventory aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_orders.aggregate_orders_quarterly').exists():
            schedule(
                'inventory.tasks.aggregate_orders.aggregate_orders_quarterly',
                schedule_type=Schedule.CRON,
                cron='0 0 1 1,7 *',
                repeats=-1,
                #next_run=now.replace(day=1, month=(now.month + 6) % 12, hour=0, minute=0, second=0, microsecond=0),  # First of next 6 months
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled quality aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_orders.aggregate_orders_annually').exists():
            schedule(
                'inventory.tasks.aggregate_orders.aggregate_orders_annually',
                schedule_type=Schedule.CRON,
                cron='0 0 1 1,7 *',
                repeats=-1,
                #next_run=now.replace(day=1, month=(now.month + 6) % 12, hour=0, minute=0, second=0, microsecond=0),  # First of next 6 months
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled quality aggregation task")

        # sales Aggregation
        if not Schedule.objects.filter(func='inventory.tasks.aggregate_sales.aggregate_sales_daily').exists():
            schedule(
                'inventory.tasks.aggregate_sales.aggregate_sales_daily',
                schedule_type=Schedule.MONTHLY,
                repeats=-1,
                #next_run= next_month_start,  # First of next month
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled monthly inventory aggregation task")
       
        if not Schedule.objects.filter(func='inventory.tasks.aggregate_sales.aggregate_sales_weekly').exists():
            schedule(
                'inventory.tasks.aggregate_sales.aggregate_sales_weekly',
                schedule_type=Schedule.CRON,
                cron='0 0 1 1,4,7,10 *',  # Example: First day of Jan, Apr, Jul, and Oct
                repeats=-1,
                #next_run=now.replace(month=(now.month - 1) // 3 * 3 + 4, day=1, hour=0, minute=0, second=0, microsecond=0),  # First of next quarter
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled quarterly inventory aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_sales.aggregate_sales_monthly').exists():
            schedule(
                'inventory.tasks.aggregate_sales.aggregate_sales_monthly',
                schedule_type=Schedule.YEARLY,
                repeats=-1,
                #next_run=now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0) + timezone.timedelta(days=365),  # First of next year
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled yearly inventory aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_sales.aggregate_sales_quarterly').exists():
            schedule(
                'inventory.tasks.aggregate_sales.aggregate_sales_quarterly',
                schedule_type=Schedule.CRON,
                cron='0 0 1 1,7 *',
                repeats=-1,
                #next_run=now.replace(day=1, month=(now.month + 6) % 12, hour=0, minute=0, second=0, microsecond=0),  # First of next 6 months
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled quality aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_sales.aggregate_sales_annually').exists():
            schedule(
                'inventory.tasks.aggregate_sales.aggregate_sales_annually',
                schedule_type=Schedule.CRON,
                cron='0 0 1 1,7 *',
                repeats=-1,
                #next_run=now.replace(day=1, month=(now.month + 6) % 12, hour=0, minute=0, second=0, microsecond=0),  # First of next 6 months
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled quality aggregation task")

        # product aggregations
        if not Schedule.objects.filter(func='inventory.tasks.aggregate_product.aggregate_product_month').exists():
            schedule(
                'inventory.tasks.aggregate_product.aggregate_product_month',
                schedule_type=Schedule.CRON,
                cron='0 0 1 1,7 *',
                repeats=-1,
                #next_run=now.replace(day=1, month=(now.month + 6) % 12, hour=0, minute=0, second=0, microsecond=0),  # First of next 6 months
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled quality aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_product.aggregate_product_quarter').exists():
            schedule(
                'inventory.tasks.aggregate_product.aggregate_product_quarter',
                schedule_type=Schedule.CRON,
                cron='0 0 1 1,7 *',
                repeats=-1,
                #next_run=now.replace(day=1, month=(now.month + 6) % 12, hour=0, minute=0, second=0, microsecond=0),  # First of next 6 months
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled quality aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_product.aggregate_product_year').exists():
            schedule(
                'inventory.tasks.aggregate_product.aggregate_product_year',
                schedule_type=Schedule.CRON,
                cron='0 0 1 1,7 *',
                repeats=-1,
                #next_run=now.replace(day=1, month=(now.month + 6) % 12, hour=0, minute=0, second=0, microsecond=0),  # First of next 6 months
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled quality aggregation task")

        # quality aggregations
        if not Schedule.objects.filter(func='inventory.tasks.aggregate_quality.aggregate_quality_quarter').exists():
            schedule(
                'inventory.tasks.aggregate_quality.aggregate_quality_quarter',
                schedule_type=Schedule.CRON,
                cron='0 0 1 1,7 *',
                repeats=-1,
                #next_run=now.replace(day=1, month=(now.month + 6) % 12, hour=0, minute=0, second=0, microsecond=0),  # First of next 6 months
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled quality aggregation task")

        if not Schedule.objects.filter(func='inventory.tasks.aggregate_quality.aggregate_quality_year').exists():
            schedule(
                'inventory.tasks.aggregate_quality.aggregate_quality_year',
                schedule_type=Schedule.CRON,
                cron='0 0 1 1,7 *',
                repeats=-1,
                #next_run=now.replace(day=1, month=(now.month + 6) % 12, hour=0, minute=0, second=0, microsecond=0),  # First of next 6 months
                next_run=timezone.now() + timezone.timedelta(minutes=2),
                cluster='gold_bi'
            )
            logger.info("Scheduled quality aggregation task")




    except Exception as e:
        logger.error("Error scheduling tasks: %s", e, exc_info=True)
