import os
import django
# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')  # Sostituisci con il nome del tuo progetto
django.setup()

from inventory.models.aggregated import *

models_name= [
    InventoryGlobalAnnualAggregation,
    InventoryGlobalQuarterlyAggregation,
    ProductAnnualAggregation,
    ProductQuarterlyAggregation,
    ProductMonthlyAggregation,
    DataQualityQuarterlyAggregation,
    DataQualityAnnualAggregation,
    SalesDailyAggregation,    
    SalesWeeklyAggregation,
    SalesMonthlyAggregation,
    SalesQuarterlyAggregation,
    SalesAnnualAggregation,
    OrdersDailyAggregation,
    OrdersWeeklyAggregation,
    OrdersMonthlyAggregation,
    OrdersQuarterlyAggregation,
    OrdersAnnualAggregation
]

def run():
    for model_name in models_name:
        print(f"{model_name}:")
        for obj in model_name.objects.using('gold').all():
            print(obj)


if __name__ == "__main__":
    run()