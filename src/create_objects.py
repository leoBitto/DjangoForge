import os
import django
import random
from faker import Faker
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')  # Sostituisci con il nome del tuo progetto
django.setup()

from transactions.models.base import BankAccount, FundLog, TransactionCategory, Transaction  # Assicurati di sostituire `your_app` con il nome effettivo della tua app

fake = Faker('it_IT')

def create_bank_accounts():
    account_types = ['checking', 'savings', 'deposit', 'cash']
    for _ in range(5):  # Crea 5 conti bancari
        BankAccount.objects.create(
            balance=round(Decimal(fake.pydecimal(left_digits=4, right_digits=2, positive=True)), 2),
            start_date=fake.date_between(start_date='-2y', end_date='today'),
            account_type=random.choice(account_types),
            institution=fake.company(),
            interest_rate=round(Decimal(fake.pydecimal(left_digits=1, right_digits=2, positive=True)), 2)
        )

def create_transaction_categories():
    # Categorie di entrate e uscite
    transaction_types = ['income', 'expense']
    for transaction_type in transaction_types:
        for _ in range(3):  # Crea 3 categorie per ogni tipo
            category = TransactionCategory.objects.create(
                name=fake.word(),
                description=fake.text(max_nb_chars=100),
                transaction_type=transaction_type
            )
            # Crea alcune sotto-categorie per ogni categoria principale
            for _ in range(random.randint(1, 2)):
                TransactionCategory.objects.create(
                    name=fake.word(),
                    description=fake.text(max_nb_chars=100),
                    transaction_type=transaction_type,
                    parent=category
                )

def create_transactions():
    bank_accounts = BankAccount.objects.all()
    categories_income = TransactionCategory.objects.filter(transaction_type='income')
    categories_expense = TransactionCategory.objects.filter(transaction_type='expense')

    for _ in range(100):  # Crea 100 transazioni
        transaction_type = random.choice(['income', 'expense'])
        category = random.choice(categories_income if transaction_type == 'income' else categories_expense)
        related_fund = random.choice(bank_accounts)
        amount = round(Decimal(fake.pydecimal(left_digits=3, right_digits=2, positive=True)), 2)

        Transaction.objects.create(
            date=fake.date_between(start_date='-1y', end_date='today'),
            amount=amount,
            description=fake.sentence(),
            transaction_type=transaction_type,
            category=category,
            related_fund=related_fund
        )

def create_fund_logs():
    bank_accounts = BankAccount.objects.all()
    for account in bank_accounts:
        # Crea un log per ogni conto
        FundLog.objects.create(
            related_fund=account,
            balance=account.balance,
            timestamp=timezone.now()
        )

def run():
    print("Creazione conti bancari...")
    create_bank_accounts()
    print("Conti bancari creati!")

    print("Creazione categorie di transazione...")
    create_transaction_categories()
    print("Categorie di transazione create!")

    print("Creazione transazioni...")
    create_transactions()
    print("Transazioni create!")

    print("Creazione log di fondo...")
    create_fund_logs()
    print("Log di fondo creati!")

if __name__ == "__main__":
    run()
