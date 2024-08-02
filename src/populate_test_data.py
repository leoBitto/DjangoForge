import os
import django
import random
from faker import Faker
from django.utils import timezone

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')  # Sostituisci con il nome del tuo progetto
django.setup()

from crm.models import CompanyCategory, Company, Supplier, Customer
from inventory.models import Category, Product, Sale, Order

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
    for _ in range(5):
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

if __name__ == "__main__":
    print("Generating test data...")

    create_company_categories()
    create_companies()
    create_suppliers_and_customers()
    create_categories()
    create_products()
    create_sales()
    create_orders()

    print("Test data generation completed.")
