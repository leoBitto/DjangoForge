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

from django.db.models import Sum

from inventory.models.base import *
from crm.models.base import *
from inventory.models.aggregated_product import *
from crm.models.aggregated import *
from logging_app.models import *
from gold_bi.models import *

fake = Faker('it_IT')

def create_company_categories():
    for _ in range(5):  # Crea 5 categorie aziendali
        CompanyCategory.objects.create(
            name=fake.word(),
            description=fake.text(max_nb_chars=100)
        )

def create_companies():
    categories = CompanyCategory.objects.all()
    for _ in range(30):  # Crea 30 aziende
        Company.objects.create(
            name=fake.company(),
            address=fake.address(),
            category=random.choice(categories) if categories.exists() else None,
            website=fake.url(),
            phone=fake.phone_number(),
            email=fake.email(),
            notes=fake.text(max_nb_chars=200),
            type=random.choice(['Supplier', 'Customer'])
        )

def create_suppliers():
    companies = Company.objects.filter(type='Supplier')
    for company in companies:
        Supplier.objects.create(
            name=fake.company(),
            company=company,
            email=fake.email(),
            phone=fake.phone_number(),
            notes=fake.text(max_nb_chars=200)
        )

def create_customers():
    companies = Company.objects.filter(type='Customer')
    for company in companies:
        Customer.objects.create(
            name=fake.name(),
            company=company,
            email=fake.email(),
            phone=fake.phone_number(),
            status=random.choice(['LEAD', 'ACTIVE', 'INACTIVE', 'LOYAL'])
        )

def create_product_categories():
    # Crea categorie di prodotto
    for _ in range(5):  # Crea 5 categorie di prodotto principali
        category = ProductCategory.objects.create(
            name=fake.word()
        )
        for _ in range(random.randint(1, 3)):  # Crea 1-3 sotto-categorie per ogni categoria principale
            ProductCategory.objects.create(
                name=fake.word(),
                parent=category
            )

def create_products():
    categories = ProductCategory.objects.all()  # Recupera tutte le categorie di prodotto
    for _ in range(20):  # Crea 20 prodotti
        Product.objects.create(
            name=fake.word(),
            category=random.choice(categories) if categories.exists() else None,  # Assegna una categoria casuale se esistono categorie
            stock_quantity=random.randint(0, 1000),
            is_visible=random.choice([True, False]),  # Imposta casualmente se il prodotto è visibile
            description=fake.text(max_nb_chars=200)
        )

def create_sales():
    products = Product.objects.all()
    customers = Customer.objects.all()
    for _ in range(1000):
        sale_date = fake.date_between(start_date='-2y', end_date='today')
        delivery_date = fake.date_between(start_date=sale_date, end_date=timezone.now().date())
        payment_date = fake.date_between(start_date=sale_date, end_date=delivery_date)
        
        Sale.objects.create(
            product=random.choice(products) if products.exists() else None,
            sale_date=sale_date,
            delivery_date=delivery_date,
            payment_date=payment_date,
            quantity=random.randint(1, 10),
            unit_price=fake.pydecimal(left_digits=2, right_digits=3, positive=True),
            status=random.choice(['pending', 'sold', 'delivered', 'paid', 'cancelled']),
            customer=random.choice(customers) if customers.exists() else None
        )

def create_orders():
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    for _ in range(2500):
        order_date = fake.date_between(start_date='-2y', end_date='today')
        delivery_date = fake.date_between(start_date=order_date, end_date=timezone.now().date())
        payment_date = fake.date_between(start_date=order_date, end_date=delivery_date)
        
        Order.objects.create(
            product=random.choice(products) if products.exists() else None,
            sale_date=order_date,
            delivery_date=delivery_date,
            payment_date=payment_date,
            quantity=random.randint(1, 10),
            unit_price=fake.pydecimal(left_digits=2, right_digits=3, positive=True),
            status=random.choice(['pending', 'sold', 'delivered', 'paid', 'cancelled']),
            supplier=random.choice(suppliers) if suppliers.exists() else None
        )

def create_inventory_aggregations():
    now = timezone.now().date()
    start_date = now - timedelta(days=365*2)  # Ultimi due anni

    # Aggregazioni giornaliere
    single_date = start_date
    while single_date <= now:
        InventoryDailyAggregation.objects.using('gold').create(
            date=single_date,
            distinct_products_in_stock=Product.objects.filter(stock_quantity__gt=0).count(),
            total_stock_value=Product.objects.aggregate(total=Sum('stock_quantity'))['total'],
            total_sold_units=Sale.objects.filter(sale_date__date=single_date).aggregate(total=Sum('quantity'))['total'],
            total_sales_value=Sale.objects.filter(sale_date__date=single_date).aggregate(total=Sum('unit_price'))['total'],
            total_pending_sales=Sale.objects.filter(sale_date__date=single_date, status='pending').count(),
            total_delivered_sales=Sale.objects.filter(sale_date__date=single_date, status='delivered').count(),
            total_paid_sales=Sale.objects.filter(sale_date__date=single_date, status='paid').count(),
            total_cancelled_sales=Sale.objects.filter(sale_date__date=single_date, status='cancelled').count(),
            total_ordered_units=Order.objects.filter(sale_date__date=single_date).aggregate(total=Sum('quantity'))['total'],
            total_orders_value=Order.objects.filter(sale_date__date=single_date).aggregate(total=Sum('unit_price'))['total'],
            total_pending_orders=Order.objects.filter(sale_date__date=single_date, status='pending').count(),
            total_delivered_orders=Order.objects.filter(sale_date__date=single_date, status='delivered').count(),
            total_paid_orders=Order.objects.filter(sale_date__date=single_date, status='paid').count(),
            total_cancelled_orders=Order.objects.filter(sale_date__date=single_date, status='cancelled').count(),
        )
        single_date += timedelta(days=1)

    # Aggregazioni settimanali
    week_start = start_date - timedelta(days=start_date.weekday())
    while week_start <= now:
        week_end = week_start + timedelta(days=6)
        if week_end > now:
            week_end = now
        InventoryWeeklyAggregation.objects.using('gold').create(
            date=week_start,
            distinct_products_in_stock=Product.objects.filter(stock_quantity__gt=0).count(),
            total_stock_value=Product.objects.aggregate(total=Sum('stock_quantity'))['total'],
            total_sold_units=Sale.objects.filter(sale_date__range=[week_start, week_end]).aggregate(total=Sum('quantity'))['total'],
            total_sales_value=Sale.objects.filter(sale_date__range=[week_start, week_end]).aggregate(total=Sum('unit_price'))['total'],
            total_pending_sales=Sale.objects.filter(sale_date__range=[week_start, week_end], status='pending').count(),
            total_delivered_sales=Sale.objects.filter(sale_date__range=[week_start, week_end], status='delivered').count(),
            total_paid_sales=Sale.objects.filter(sale_date__range=[week_start, week_end], status='paid').count(),
            total_cancelled_sales=Sale.objects.filter(sale_date__range=[week_start, week_end], status='cancelled').count(),
            total_ordered_units=Order.objects.filter(sale_date__range=[week_start, week_end]).aggregate(total=Sum('quantity'))['total'],
            total_orders_value=Order.objects.filter(sale_date__range=[week_start, week_end]).aggregate(total=Sum('unit_price'))['total'],
            total_pending_orders=Order.objects.filter(sale_date__range=[week_start, week_end], status='pending').count(),
            total_delivered_orders=Order.objects.filter(sale_date__range=[week_start, week_end], status='delivered').count(),
            total_paid_orders=Order.objects.filter(sale_date__range=[week_start, week_end], status='paid').count(),
            total_cancelled_orders=Order.objects.filter(sale_date__range=[week_start, week_end], status='cancelled').count(),
        )
        week_start += timedelta(weeks=1)

    # Aggregazioni mensili
    for year in range(start_date.year, now.year + 1):
        for month in range(1, 13):
            month_start = timezone.datetime(year, month, 1).date()
            month_end = (month_start + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            if month_end > now:
                month_end = now
            InventoryMonthlyAggregation.objects.using('gold').create(
                date=month_start,
                distinct_products_in_stock=Product.objects.filter(stock_quantity__gt=0).count(),
                total_stock_value=Product.objects.aggregate(total=Sum('stock_quantity'))['total'],
                total_sold_units=Sale.objects.filter(sale_date__range=[month_start, month_end]).aggregate(total=Sum('quantity'))['total'],
                total_sales_value=Sale.objects.filter(sale_date__range=[month_start, month_end]).aggregate(total=Sum('unit_price'))['total'],
                total_pending_sales=Sale.objects.filter(sale_date__range=[month_start, month_end], status='pending').count(),
                total_delivered_sales=Sale.objects.filter(sale_date__range=[month_start, month_end], status='delivered').count(),
                total_paid_sales=Sale.objects.filter(sale_date__range=[month_start, month_end], status='paid').count(),
                total_cancelled_sales=Sale.objects.filter(sale_date__range=[month_start, month_end], status='cancelled').count(),
                total_ordered_units=Order.objects.filter(sale_date__range=[month_start, month_end]).aggregate(total=Sum('quantity'))['total'],
                total_orders_value=Order.objects.filter(sale_date__range=[month_start, month_end]).aggregate(total=Sum('unit_price'))['total'],
                total_pending_orders=Order.objects.filter(sale_date__range=[month_start, month_end], status='pending').count(),
                total_delivered_orders=Order.objects.filter(sale_date__range=[month_start, month_end], status='delivered').count(),
                total_paid_orders=Order.objects.filter(sale_date__range=[month_start, month_end], status='paid').count(),
                total_cancelled_orders=Order.objects.filter(sale_date__range=[month_start, month_end], status='cancelled').count(),
            )

    # Aggregazioni trimestrali
    for year in range(start_date.year, now.year + 1):
        for quarter in range(1, 5):
            quarter_start = timezone.datetime(year, (quarter - 1) * 3 + 1, 1).date()
            quarter_end = (quarter_start + timedelta(days=90)).replace(day=1) - timedelta(days=1)
            if quarter_end > now:
                quarter_end = now
            InventoryQuarterlyAggregation.objects.using('gold').create(
                date=quarter_start,
                distinct_products_in_stock=Product.objects.filter(stock_quantity__gt=0).count(),
                total_stock_value=Product.objects.aggregate(total=Sum('stock_quantity'))['total'],
                total_sold_units=Sale.objects.filter(sale_date__range=[quarter_start, quarter_end]).aggregate(total=Sum('quantity'))['total'],
                total_sales_value=Sale.objects.filter(sale_date__range=[quarter_start, quarter_end]).aggregate(total=Sum('unit_price'))['total'],
                total_pending_sales=Sale.objects.filter(sale_date__range=[quarter_start, quarter_end], status='pending').count(),
                total_delivered_sales=Sale.objects.filter(sale_date__range=[quarter_start, quarter_end], status='delivered').count(),
                total_paid_sales=Sale.objects.filter(sale_date__range=[quarter_start, quarter_end], status='paid').count(),
                total_cancelled_sales=Sale.objects.filter(sale_date__range=[quarter_start, quarter_end], status='cancelled').count(),
                total_ordered_units=Order.objects.filter(sale_date__range=[quarter_start, quarter_end]).aggregate(total=Sum('quantity'))['total'],
                total_orders_value=Order.objects.filter(sale_date__range=[quarter_start, quarter_end]).aggregate(total=Sum('unit_price'))['total'],
                total_pending_orders=Order.objects.filter(sale_date__range=[quarter_start, quarter_end], status='pending').count(),
                total_delivered_orders=Order.objects.filter(sale_date__range=[quarter_start, quarter_end], status='delivered').count(),
                total_paid_orders=Order.objects.filter(sale_date__range=[quarter_start, quarter_end], status='paid').count(),
                total_cancelled_orders=Order.objects.filter(sale_date__range=[quarter_start, quarter_end], status='cancelled').count(),
            )

    # Aggregazioni annuali
    for year in range(start_date.year, now.year + 1):
        year_start = timezone.datetime(year, 1, 1).date()
        year_end = timezone.datetime(year, 12, 31).date()
        InventoryYearlyAggregation.objects.using('gold').create(
            date=year_start,
            distinct_products_in_stock=Product.objects.filter(stock_quantity__gt=0).count(),
            total_stock_value=Product.objects.aggregate(total=Sum('stock_quantity'))['total'],
            total_sold_units=Sale.objects.filter(sale_date__range=[year_start, year_end]).aggregate(total=Sum('quantity'))['total'],
            total_sales_value=Sale.objects.filter(sale_date__range=[year_start, year_end]).aggregate(total=Sum('unit_price'))['total'],
            total_pending_sales=Sale.objects.filter(sale_date__range=[year_start, year_end], status='pending').count(),
            total_delivered_sales=Sale.objects.filter(sale_date__range=[year_start, year_end], status='delivered').count(),
            total_paid_sales=Sale.objects.filter(sale_date__range=[year_start, year_end], status='paid').count(),
            total_cancelled_sales=Sale.objects.filter(sale_date__range=[year_start, year_end], status='cancelled').count(),
            total_ordered_units=Order.objects.filter(sale_date__range=[year_start, year_end]).aggregate(total=Sum('quantity'))['total'],
            total_orders_value=Order.objects.filter(sale_date__range=[year_start, year_end]).aggregate(total=Sum('unit_price'))['total'],
            total_pending_orders=Order.objects.filter(sale_date__range=[year_start, year_end], status='pending').count(),
            total_delivered_orders=Order.objects.filter(sale_date__range=[year_start, year_end], status='delivered').count(),
            total_paid_orders=Order.objects.filter(sale_date__range=[year_start, year_end], status='paid').count(),
            total_cancelled_orders=Order.objects.filter(sale_date__range=[year_start, year_end], status='cancelled').count(),
        )

def create_inventory_quality_aggregation():
    InventoryQualityAggregation.objects.using('gold').create(
        products_missing_category=Product.objects.filter(category__isnull=True).count(),
        products_missing_image=Product.objects.filter(image__isnull=True).count(),
        products_missing_description=Product.objects.filter(description__exact='').count(),
        products_missing_both=Product.objects.filter(category__isnull=True, image__isnull=True).count()
    )

def create_crm_monthly_snapshot():
    now = timezone.now().date()
    start_date = now - timedelta(days=365*2)  # Ultimi due anni
    for year in range(start_date.year, now.year + 1):
        for month in range(1, 13):
            month_start = timezone.datetime(year, month, 1).date()
            month_end = (month_start + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            if month_end > now:
                month_end = now
            CRMMontlySnapshot.objects.using('gold').create(
                date=month_start,
                total_suppliers=Supplier.objects.count(),
                total_customers=Customer.objects.count(),
                total_leads=Customer.objects.filter(status='LEAD').count(),
                total_active_customers=Customer.objects.filter(status='ACTIVE').count(),
                total_inactive_customers=Customer.objects.filter(status='INACTIVE').count(),
                total_loyal_customers=Customer.objects.filter(status='LOYAL').count()
            )

def run():
    print("Creazione categorie aziendali...")
    create_company_categories()
    print("Categorie aziendali create!")

    print("Creazione aziende...")
    create_companies()
    print("Aziende create!")

    print("Creazione fornitori...")
    create_suppliers()
    print("Fornitori creati!")

    print("Creazione clienti...")
    create_customers()
    print("Clienti creati!")

    print("Creazione categorie di prodotto...")
    create_product_categories()
    print("Categorie di prodotto create!")

    print("Creazione prodotti...")
    create_products()
    print("Prodotti creati!")

    print("Creazione ordini...")
    create_orders()
    print("Ordini creati!")

    print("Creazione vendite...")
    create_sales()
    print("Vendite create!")

    #print("Creazione aggregazioni inventario...")
    #create_inventory_aggregations()
    #print("Aggregazioni inventario create!")

    #print("Creazione aggregazione qualità inventario...")
    #create_inventory_quality_aggregation()
    #print("Aggregazione qualità inventario creata!")

    #print("Creazione snapshot CRM mensili...")
    #create_crm_monthly_snapshot()
    #print("Snapshot CRM mensili creati!")

if __name__ == "__main__":
    run()
