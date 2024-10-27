from django.test import TestCase
from .models.base import BankAccount, Cash, FundLog, Income, IncomeCategory, Expenditure, ExpenseCategory
from django.contrib.contenttypes.models import ContentType

class FundBaseModelTest(TestCase):

    def test_create_bank_account(self):
        account = BankAccount.objects.create(
            balance=1000.00,
            start_date='2024-01-01',
            account_type='savings',
            institution='Bank XYZ',
            interest_rate=1.5
        )
        self.assertEqual(account.balance, 1000.00)
        self.assertEqual(account.account_type, 'savings')
        self.assertEqual(account.institution, 'Bank XYZ')
        self.assertEqual(account.interest_rate, 1.5)

    def test_create_cash(self):
        cash = Cash.objects.create(
            balance=500.00,
            start_date='2024-01-01',
            description='Cash in hand'
        )
        self.assertEqual(cash.balance, 500.00)
        self.assertEqual(cash.description, 'Cash in hand')

class FundLogSignalTest(TestCase):

    def test_fund_log_created_on_bank_account_update(self):
        account = BankAccount.objects.create(
            balance=1000.00,
            start_date='2024-01-01',
            account_type='savings',
            institution='Bank XYZ',
            interest_rate=1.5
        )
        
        account.balance = 1500.00
        account.save()

        log_entry = FundLog.objects.get(content_type=ContentType.objects.get_for_model(account), object_id=account.id)
        self.assertEqual(log_entry.balance, 1500.00)

    def test_fund_log_created_on_cash_update(self):
        cash = Cash.objects.create(
            balance=500.00,
            start_date='2024-01-01',
            description='Cash in hand'
        )
        
        cash.balance = 750.00
        cash.save()

        log_entry = FundLog.objects.get(content_type=ContentType.objects.get_for_model(cash), object_id=cash.id)
        self.assertEqual(log_entry.balance, 750.00)

class TransactionModelTest(TestCase):

    def test_create_transaction_for_bank_account(self):
        account = BankAccount.objects.create(
            balance=1000.00,
            start_date='2024-01-01',
            account_type='savings',
            institution='Bank XYZ'
        )
        
        transaction = Transaction.objects.create(
            date='2024-01-10',
            amount=250.00,
            related_fund=ContentType.objects.get_for_model(account),
            object_id=account.id,
            description="Test transaction"
        )

        self.assertEqual(transaction.content_object, account)
        self.assertEqual(str(transaction), "Transaction: 250.00 on 2024-01-10")

    def test_create_income(self):
        account = BankAccount.objects.create(
            balance=1000.00,
            start_date='2024-01-01',
            account_type='savings',
            institution='Bank XYZ'
        )

        category = IncomeCategory.objects.create(
            name="Salary",
            description="Monthly Salary"
        )

        income = Income.objects.create(
            date='2024-01-10',
            amount=500.00,
            related_fund=ContentType.objects.get_for_model(account),
            object_id=account.id,
            description="January Salary",
            type=category
        )

        self.assertEqual(income.type.name, "Salary")
        self.assertEqual(str(income), "Income: 500.00 on 2024-01-10")

    def test_create_expenditure(self):
        cash = Cash.objects.create(
            balance=500.00,
            start_date='2024-01-01',
            description='Cash in hand'
        )

        category = ExpenseCategory.objects.create(
            name="Food",
            description="Grocery shopping"
        )

        expenditure = Expenditure.objects.create(
            date='2024-01-12',
            amount=100.00,
            related_fund=ContentType.objects.get_for_model(cash),
            object_id=cash.id,
            description="Grocery Shopping",
            type=category
        )

        self.assertEqual(expenditure.type.name, "Food")
        self.assertEqual(str(expenditure), "Expenditure: 100.00 on 2024-01-12")

