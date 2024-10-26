from django.db import models
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class FundBase(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  # Data di chiusura per il fondo

    class Meta:
        abstract = True

    def __str__(self):
        end_date_str = f" - End Date: {self.end_date}" if self.end_date else ""
        return f"Amount: {self.balance} - Start Date: {self.start_date}{end_date_str}"


class BankAccount(FundBase):
    ACCOUNT_TYPES = (
        ('checking', 'Checking Account'),
        ('savings', 'Savings Account'),
        ('deposit', 'Deposit Account'),
        ('other', 'Other'),
    )

    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='checking')
    institution = models.CharField(max_length=100)  # Nome dell'istituto bancario
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Tasso d'interesse per conti con interesse

    def __str__(self):
        return f"{self.institution} ({self.account_type}) - Balance: {self.balance}"


class Cash(FundBase):
    description = models.CharField(max_length=100, blank=True, null=True)  # Descrizione del contante

    def __str__(self):
        end_date_str = f" - End Date: {self.end_date}" if self.end_date else ""
        return f"Amount: {self.balance} - Start Date: {self.start_date}{end_date_str}"


class FundLog(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.content_object} - Balance: {self.balance} at {self.timestamp}"

@receiver(post_save, sender=BankAccount)
@receiver(post_save, sender=Cash)
def log_fund_change(sender, instance, created, **kwargs):
    if not created:
        # Trova il tipo di contenuto del modello
        content_type = ContentType.objects.get_for_model(instance)
        
        # Crea un nuovo log
        FundLog.objects.create(
            content_type=content_type,
            object_id=instance.id,
            balance=instance.balance
        )



class Transaction(models.Model):
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100, blank=True, null=True)
    related_fund = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('related_fund', 'object_id')

    def __str__(self):
        return f"Transaction: {self.amount} on {self.date}"
    
    class Meta:
        indexes = [
            models.Index(fields=['date', 'time']),
        ]



class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Income(Transaction):
    type = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"Income: {self.amount} on {self.date}"


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Expenditure(Transaction):
    type = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"Expenditure: {self.amount} on {self.date}"

