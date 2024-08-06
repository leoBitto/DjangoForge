import os
import django
import random
import string
from faker import Faker
from django.utils import timezone
from datetime import timedelta

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')  # Sostituisci con il nome del tuo progetto
django.setup()

from crm.models import CompanyCategory, Company, Supplier, Customer
from inventory.models import Category, Product, Sale, Order
from gold_bi.models import *
from logging_app.models import *

#fake = Faker()
fake = Faker('it_IT')

def create_company_categories():
    for _ in range(10):
        CompanyCategory.objects.create(
            name=fake.word(),
            description=fake.text()
        )

def create_companies():
    categories = CompanyCategory.objects.all()
    for _ in range(10):
        Company.objects.create(
            name=fake.company(),
            address=fake.address(),
            category=random.choice(categories) if categories.exists() else None,
            website=fake.url(),
            phone=fake.phone_number(),
            email=fake.email(),
            notes=fake.text(),
            type=random.choice(['Supplier', 'Customer'])
        )

def create_suppliers_and_customers():
    companies = Company.objects.all()
    for company in companies:
        for _ in range(2):
            Supplier.objects.create(
                name=fake.name(),
                company=company,
                email=fake.email(),
                phone=fake.phone_number(),
                notes=fake.text()
            )
        for _ in range(2):
            Customer.objects.create(
                name=fake.name(),
                company=company,
                email=fake.email(),
                phone=fake.phone_number(),
                status=random.choice(['LEAD', 'ACTIVE', 'INACTIVE', 'LOYAL'])
            )

def create_categories():
    for _ in range(5):
        Category.objects.create(
            name=fake.word(),
            parent=None  # Puoi aggiungere logica per sottocategorie se necessario
        )

def create_products():
    categories = Category.objects.all()
    for _ in range(20):
        Product.objects.create(
            name=fake.word(),
            category=random.choice(categories) if categories.exists() else None,
            stock_quantity=random.randint(0, 100),
            unit_price=fake.random_number(digits=5),
            image=None,  # Puoi aggiungere immagini se necessario
            is_visible=random.choice([True, False]),
            description=fake.text()
        )

def create_sales():
    products = Product.objects.all()
    customers = Customer.objects.all()
    for _ in range(15):
        Sale.objects.create(
            product=random.choice(products) if products.exists() else None,
            sale_date=fake.date_this_year(),
            delivery_date=fake.date_this_year(),
            payment_date=fake.date_this_year(),
            quantity=random.randint(1, 10),
            unit_price=fake.random_number(digits=5),
            status=random.choice(['pending', 'sold', 'delivered', 'paid', 'cancelled']),
            customer=random.choice(customers) if customers.exists() else None
        )

def create_orders():
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    for _ in range(15):
        Order.objects.create(
            product=random.choice(products) if products.exists() else None,
            sale_date=fake.date_this_year(),
            delivery_date=fake.date_this_year(),
            payment_date=fake.date_this_year(),
            quantity=random.randint(1, 10),
            unit_price=fake.random_number(digits=5),
            status=random.choice(['pending', 'sold', 'delivered', 'paid', 'cancelled']),
            supplier=random.choice(suppliers) if suppliers.exists() else None
        )


def create_error_logs():
    for _ in range(50):
        # Genera un timestamp casuale negli ultimi 30 giorni
        timestamp = timezone.now() - timedelta(days=random.randint(0, 30))
        
        # Genera un percorso di richiesta casuale
        request_path = f"/path/to/resource/{random.randint(1, 100)}"
        
        # Genera un metodo di richiesta casuale
        request_method = random.choice(['GET', 'POST', 'PUT', 'DELETE'])
        
        # Genera un codice di risposta casuale
        response_code = random.randint(100, 599)
        
        # Genera un messaggio di errore casuale
        error_message = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=100))
        
        # Genera uno stack trace casuale
        stack_trace = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=200))
        
        ErrorLog.objects.create(
            timestamp=timestamp,
            request_path=request_path,
            request_method=request_method,
            response_code=response_code,
            error_message=error_message,
            stack_trace=stack_trace
        )

def create_access_logs():
    for _ in range(400):
        # Genera un timestamp casuale negli ultimi 30 giorni
        timestamp = timezone.now() - timedelta(days=random.randint(0, 30))
        
        # Genera un percorso di richiesta casuale
        request_path = f"/path/to/resource/{random.randint(1, 100)}"
        
        # Genera un metodo di richiesta casuale
        request_method = random.choice(['GET', 'POST', 'PUT', 'DELETE'])
        
        # Genera un codice di risposta casuale
        response_code = random.randint(100, 599)
        
        AccessLog.objects.create(
            timestamp=timestamp,
            request_path=request_path,
            request_method=request_method,
            response_code=response_code
        )

def create_aggregated_error_logs():
    for _ in range(20):
        AggregatedErrorLog.objects.using('gold').create(
            hour=random.randint(0, 23),
            day=str(random.randint(1, 7)),  # assuming 1 = Monday, 7 = Sunday
            count=random.randint(0, 100)
        )

def create_aggregated_access_logs():
    for _ in range(20):
        AggregatedAccessLog.objects.using('gold').create(
            hour=random.randint(0, 23),
            day=str(random.randint(1, 7)),
            count=random.randint(0, 100)
        )

def create_crm_monthly_snapshots():
    for _ in range(12):
        CRMMontlySnapshot.objects.using('gold').create(
            month=random.randint(1, 12),
            year=fake.year(),
            total_suppliers=random.randint(10, 100),
            total_customers=random.randint(10, 100),
            total_leads=random.randint(1, 50),
            total_active_customers=random.randint(1, 50),
            total_inactive_customers=random.randint(1, 50),
            total_loyal_customers=random.randint(1, 50)
        )

def create_inventory_daily_aggregations():
    for _ in range(30):
        InventoryDailyAggregation.objects.using('gold').create(
            date=fake.date_this_year(),
            distinct_products_in_stock=random.randint(1, 100),
            total_stock_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_sold_units=random.randint(0, 50),
            total_sales_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_pending_sales=random.randint(0, 20),
            total_delivered_sales=random.randint(0, 20),
            total_paid_sales=random.randint(0, 20),
            total_cancelled_sales=random.randint(0, 20),
            total_ordered_units=random.randint(0, 50),
            total_orders_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_pending_orders=random.randint(0, 20),
            total_delivered_orders=random.randint(0, 20),
            total_paid_orders=random.randint(0, 20),
            total_cancelled_orders=random.randint(0, 20)
        )

def create_inventory_weekly_aggregations():
    for _ in range(52):
        InventoryWeeklyAggregation.objects.using('gold').create(
            week=random.randint(1, 52),
            year=fake.year(),
            distinct_products_in_stock=random.randint(1, 100),
            total_stock_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_sold_units=random.randint(0, 50),
            total_sales_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_pending_sales=random.randint(0, 20),
            total_delivered_sales=random.randint(0, 20),
            total_paid_sales=random.randint(0, 20),
            total_cancelled_sales=random.randint(0, 20),
            total_ordered_units=random.randint(0, 50),
            total_orders_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_pending_orders=random.randint(0, 20),
            total_delivered_orders=random.randint(0, 20),
            total_paid_orders=random.randint(0, 20),
            total_cancelled_orders=random.randint(0, 20)
        )

def create_inventory_monthly_aggregations():
    for _ in range(12):
        InventoryMonthlyAggregation.objects.using('gold').create(
            month=random.randint(1, 12),
            year=fake.year(),
            distinct_products_in_stock=random.randint(1, 100),
            total_stock_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_sold_units=random.randint(0, 50),
            total_sales_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_pending_sales=random.randint(0, 20),
            total_delivered_sales=random.randint(0, 20),
            total_paid_sales=random.randint(0, 20),
            total_cancelled_sales=random.randint(0, 20),
            total_ordered_units=random.randint(0, 50),
            total_orders_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_pending_orders=random.randint(0, 20),
            total_delivered_orders=random.randint(0, 20),
            total_paid_orders=random.randint(0, 20),
            total_cancelled_orders=random.randint(0, 20)
        )

def create_inventory_quarterly_aggregations():
    for _ in range(4):
        InventoryQuarterlyAggregation.objects.using('gold').create(
            quarter=random.randint(1, 4),
            year=fake.year(),
            distinct_products_in_stock=random.randint(1, 100),
            total_stock_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_sold_units=random.randint(0, 50),
            total_sales_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_pending_sales=random.randint(0, 20),
            total_delivered_sales=random.randint(0, 20),
            total_paid_sales=random.randint(0, 20),
            total_cancelled_sales=random.randint(0, 20),
            total_ordered_units=random.randint(0, 50),
            total_orders_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_pending_orders=random.randint(0, 20),
            total_delivered_orders=random.randint(0, 20),
            total_paid_orders=random.randint(0, 20),
            total_cancelled_orders=random.randint(0, 20)
        )

def create_inventory_yearly_aggregations():
    for _ in range(5):  # Generare 5 anni di dati
        InventoryYearlyAggregation.objects.using('gold').create(
            year=fake.year(),
            distinct_products_in_stock=random.randint(1, 100),
            total_stock_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_sold_units=random.randint(0, 50),
            total_sales_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_pending_sales=random.randint(0, 20),
            total_delivered_sales=random.randint(0, 20),
            total_paid_sales=random.randint(0, 20),
            total_cancelled_sales=random.randint(0, 20),
            total_ordered_units=random.randint(0, 50),
            total_orders_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            total_pending_orders=random.randint(0, 20),
            total_delivered_orders=random.randint(0, 20),
            total_paid_orders=random.randint(0, 20),
            total_cancelled_orders=random.randint(0, 20)
        )

def create_inventory_quality_aggregations():
    for _ in range(12):
        InventoryQualityAggregation.objects.using('gold').create(
            month=random.randint(1, 12),
            year=fake.year(),
            products_missing_category=random.randint(0, 10),
            products_missing_image=random.randint(0, 10),
            products_missing_description=random.randint(0, 10),
            products_missing_both=random.randint(0, 5)
        )

def create_inventory_monthly_snapshots():
    for _ in range(12):
        InventoryMonthlySnapshot.objects.using('gold').create(
            month=random.randint(1, 12),
            year=fake.year(),
            total_products=random.randint(50, 100),
            total_stock_quantity=random.randint(1000, 5000),
            total_stock_value=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            average_stock_per_product=fake.pydecimal(left_digits=5, right_digits=2, positive=True)
        )


if __name__ == "__main__":
    print("Generating test data...")

    create_company_categories()
    create_companies()
    create_suppliers_and_customers()
    create_categories()
    create_products()
    create_sales()
    create_orders()

    create_access_logs()
    create_error_logs()

    #create_aggregated_error_logs()
    #create_aggregated_access_logs()
    #create_crm_monthly_snapshots()
    #create_inventory_daily_aggregations()
    #create_inventory_weekly_aggregations()
    #create_inventory_monthly_aggregations()
    #create_inventory_quarterly_aggregations()
    #create_inventory_yearly_aggregations()
    #create_inventory_quality_aggregations()
    #create_inventory_monthly_snapshots()

    print("Test data generation completed.")
