import logging
from django.utils import timezone
from gold_bi.models import CRMMontlySnapshot
from django.db import transaction
from crm.models import *

logger = logging.getLogger('gold_bi')

def aggregate_crm_monthly():
    try:
        now = timezone.now()

        # Determina il primo giorno del mese corrente
        first_day_of_current_month = timezone.datetime(year=now.year, month=now.month, day=1)

        # Determina l'ultimo giorno del mese precedente
        date = first_day_of_current_month - timezone.timedelta(days=1)

        # Aggregazione dei dati
        total_suppliers = Supplier.objects.using('default').count()
        total_customers = Customer.objects.using('default').count()
        total_leads = Customer.objects.using('default').filter(status='LEAD').count()
        total_active_customers = Customer.objects.using('default').filter(status='ACTIVE').count()
        total_inactive_customers = Customer.objects.using('default').filter(status='INACTIVE').count()
        total_loyal_customers = Customer.objects.using('default').filter(status='LOYAL').count()

        # Aggregazione dei dati
        crm_aggregations = {
            'total_suppliers': total_suppliers,
            'total_customers': total_customers,
            'total_leads': total_leads,
            'total_active_customers': total_active_customers,
            'total_inactive_customers': total_inactive_customers,
            'total_loyal_customers': total_loyal_customers
        }

        # Aggiornamento dei risultati aggregati nel modello AggregatedCRMMonthly
        with transaction.atomic():
            obj, created = CRMMontlySnapshot.objects.using('gold').get_or_create(
                month=date.month,
                year=date.year
            )
            
            # Aggiorna i campi con i valori aggregati
            obj.total_suppliers = crm_aggregations['total_suppliers']
            obj.total_customers = crm_aggregations['total_customers']
            obj.total_leads = crm_aggregations['total_leads']
            obj.total_active_customers = crm_aggregations['total_active_customers']
            obj.total_inactive_customers = crm_aggregations['total_inactive_customers']
            obj.total_loyal_customers = crm_aggregations['total_loyal_customers']
            obj.save()

        logger.info(f'Monthly CRM logs aggregated successfully for {date.month} / {date.year}.')
    except Exception as e:
        logger.error(f'Error aggregating monthly CRM logs for  {date.month} / {date.year}: {e}')
