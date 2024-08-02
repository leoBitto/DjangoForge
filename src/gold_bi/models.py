from django.db import models
from django.utils import timezone

class AggregatedErrorLog(models.Model):
    """
    Modello per memorizzare gli errori aggregati.
    """
    hour = models.IntegerField()  # Ora (0-23)
    day = models.CharField(max_length=10)  # Giorno della settimana è un numero memorizzato come stringa
    count = models.IntegerField(default=0, null=True, blank=True)  # Conteggio degli errori

    class Meta:
        verbose_name = "Aggregated Error Log"
        verbose_name_plural = "Aggregated Error Logs"

    def __str__(self):
        return f"Error Log - {self.day} - {self.hour} - Count: {self.count}"


class AggregatedAccessLog(models.Model):
    """
    Modello per memorizzare gli accessi aggregati.
    """
    hour = models.IntegerField()  # Ora (0-23)
    day = models.CharField(max_length=10)  # Giorno della settimana (es. "Monday")
    count = models.IntegerField(default=0, null=True, blank=True)  # Conteggio degli accessi

    class Meta:
        verbose_name = "Aggregated Access Log"
        verbose_name_plural = "Aggregated Access Logs"

    def __str__(self):
        return f"Access Log - {self.day} - {self.hour} - Count: {self.count}"


# CRM: Fotografie Mensili
class CRMMontlySnapshot(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    month = models.IntegerField()
    year = models.IntegerField()
    total_suppliers = models.IntegerField()
    total_customers = models.IntegerField()
    total_leads = models.IntegerField()
    total_active_customers = models.IntegerField()
    total_inactive_customers = models.IntegerField()
    total_loyal_customers = models.IntegerField()

    class Meta:
        verbose_name = "CRM Monthly Snapshot"
        verbose_name_plural = "CRM Monthly Snapshots"

# Inventory: Aggregazioni Temporali - Daily
class InventoryDailyAggregation(models.Model):
    date = models.DateField()

    # Stock data
    distinct_products_in_stock = models.IntegerField()  # Numero di prodotti distinti in magazzino
    total_stock_value = models.DecimalField(max_digits=15, decimal_places=2)

    # Sales data
    total_sold_units = models.IntegerField()
    total_sales_value = models.DecimalField(max_digits=15, decimal_places=2)
    total_pending_sales = models.IntegerField()
    total_delivered_sales = models.IntegerField()
    total_paid_sales = models.IntegerField()
    total_cancelled_sales = models.IntegerField()

    # Orders data
    total_ordered_units = models.IntegerField()  # Nuovo campo: totale unità ordinate
    total_orders_value = models.DecimalField(max_digits=15, decimal_places=2)  # Nuovo campo: valore totale ordini
    total_pending_orders = models.IntegerField()
    total_delivered_orders = models.IntegerField()
    total_paid_orders = models.IntegerField()
    total_cancelled_orders = models.IntegerField()

    class Meta:
        verbose_name = "Inventory Daily Aggregation"
        verbose_name_plural = "Inventory Daily Aggregations"

# Inventory: Aggregazioni Temporali - Weekly
class InventoryWeeklyAggregation(models.Model):
    week = models.IntegerField()
    year = models.IntegerField()

    # Stock data
    distinct_products_in_stock = models.IntegerField()  # Numero di prodotti distinti in magazzino
    total_stock_value = models.DecimalField(max_digits=15, decimal_places=2)

    # Sales data
    total_sold_units = models.IntegerField()
    total_sales_value = models.DecimalField(max_digits=15, decimal_places=2)
    total_pending_sales = models.IntegerField()
    total_delivered_sales = models.IntegerField()
    total_paid_sales = models.IntegerField()
    total_cancelled_sales = models.IntegerField()

    # Orders data
    total_ordered_units = models.IntegerField()  # Totale unità ordinate
    total_orders_value = models.DecimalField(max_digits=15, decimal_places=2)  # Valore totale ordini
    total_pending_orders = models.IntegerField()
    total_delivered_orders = models.IntegerField()
    total_paid_orders = models.IntegerField()
    total_cancelled_orders = models.IntegerField()

    class Meta:
        verbose_name = "Inventory Weekly Aggregation"
        verbose_name_plural = "Inventory Weekly Aggregations"

# Inventory: Aggregazioni Temporali - Monthly
class InventoryMonthlyAggregation(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()

    # Stock data
    distinct_products_in_stock = models.IntegerField()  # Numero di prodotti distinti in magazzino
    total_stock_value = models.DecimalField(max_digits=15, decimal_places=2)

    # Sales data
    total_sold_units = models.IntegerField()
    total_sales_value = models.DecimalField(max_digits=15, decimal_places=2)
    total_pending_sales = models.IntegerField()
    total_delivered_sales = models.IntegerField()
    total_paid_sales = models.IntegerField()
    total_cancelled_sales = models.IntegerField()

    # Orders data
    total_ordered_units = models.IntegerField()  # Totale unità ordinate
    total_orders_value = models.DecimalField(max_digits=15, decimal_places=2)  # Valore totale ordini
    total_pending_orders = models.IntegerField()
    total_delivered_orders = models.IntegerField()
    total_paid_orders = models.IntegerField()
    total_cancelled_orders = models.IntegerField()

    class Meta:
        verbose_name = "Inventory Monthly Aggregation"
        verbose_name_plural = "Inventory Monthly Aggregations"

# Inventory: Aggregazioni Temporali - Quarterly
class InventoryQuarterlyAggregation(models.Model):
    quarter = models.IntegerField()
    year = models.IntegerField()

    # Stock data
    distinct_products_in_stock = models.IntegerField()  # Numero di prodotti distinti in magazzino
    total_stock_value = models.DecimalField(max_digits=15, decimal_places=2)

    # Sales data
    total_sold_units = models.IntegerField()
    total_sales_value = models.DecimalField(max_digits=15, decimal_places=2)
    total_pending_sales = models.IntegerField()
    total_delivered_sales = models.IntegerField()
    total_paid_sales = models.IntegerField()
    total_cancelled_sales = models.IntegerField()

    # Orders data
    total_ordered_units = models.IntegerField()  # Totale unità ordinate
    total_orders_value = models.DecimalField(max_digits=15, decimal_places=2)  # Valore totale ordini
    total_pending_orders = models.IntegerField()
    total_delivered_orders = models.IntegerField()
    total_paid_orders = models.IntegerField()
    total_cancelled_orders = models.IntegerField()

    class Meta:
        verbose_name = "Inventory Quarterly Aggregation"
        verbose_name_plural = "Inventory Quarterly Aggregations"

# Inventory: Aggregazioni Temporali - Yearly
class InventoryYearlyAggregation(models.Model):
    year = models.IntegerField()

    # Stock data
    distinct_products_in_stock = models.IntegerField()  # Numero di prodotti distinti in magazzino
    total_stock_value = models.DecimalField(max_digits=15, decimal_places=2)

    # Sales data
    total_sold_units = models.IntegerField()
    total_sales_value = models.DecimalField(max_digits=15, decimal_places=2)
    total_pending_sales = models.IntegerField()
    total_delivered_sales = models.IntegerField()
    total_paid_sales = models.IntegerField()
    total_cancelled_sales = models.IntegerField()

    # Orders data
    total_ordered_units = models.IntegerField()  # Totale unità ordinate
    total_orders_value = models.DecimalField(max_digits=15, decimal_places=2)  # Valore totale ordini
    total_pending_orders = models.IntegerField()
    total_delivered_orders = models.IntegerField()
    total_paid_orders = models.IntegerField()
    total_cancelled_orders = models.IntegerField()

    class Meta:
        verbose_name = "Inventory Yearly Aggregation"
        verbose_name_plural = "Inventory Yearly Aggregations"

# Inventory: Controllo Qualità del Magazzino
class InventoryQualityAggregation(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    month = models.IntegerField()
    year = models.IntegerField()
    products_missing_category = models.IntegerField()
    products_missing_image = models.IntegerField()
    products_missing_description = models.IntegerField()
    products_missing_both = models.IntegerField()

    class Meta:
        verbose_name = "Inventory Quality Aggregation"
        verbose_name_plural = "Inventory Quality Aggregations"

# Inventory: Fotografie Mensili del Magazzino
class InventoryMonthlySnapshot(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    month = models.IntegerField()
    year = models.IntegerField()
    total_products = models.IntegerField()
    total_stock_quantity = models.IntegerField()
    total_stock_value = models.DecimalField(max_digits=15, decimal_places=2)
    average_stock_per_product = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Inventory Monthly Snapshot"
        verbose_name_plural = "Inventory Monthly Snapshots"











