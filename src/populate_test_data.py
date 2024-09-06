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
from inventory.models.aggregated import *
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
            name=fake.name(),
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

def generate_invoice_number():
    year = timezone.now().year
    random_number = random.randint(0, 100)
    return f"{year}-{random_number:03}"

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
            customer=random.choice(customers) if customers.exists() else None,
            sale_invoice_number=generate_invoice_number()
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
            supplier=random.choice(suppliers) if suppliers.exists() else None,
            order_invoice_number=generate_invoice_number()
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


if __name__ == "__main__":
    run()
