from django.db import models
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class FundBase(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

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
    if not created and instance.pk:  # Si assicura di non creare log duplicati al salvataggio iniziale
        last_log = FundLog.objects.filter(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        ).order_by('-timestamp').first()

        if last_log is None or last_log.balance != instance.balance:
            # Crea un log solo se il bilancio è cambiato
            FundLog.objects.create(
                content_type=ContentType.objects.get_for_model(instance),
                object_id=instance.id,
                balance=instance.balance
            )


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100, blank=True, null=True)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    related_fund = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('related_fund', 'object_id')

    def __str__(self):
        return f"{self.get_transaction_type_display()}: {self.amount} on {self.date}"
    
    class Meta:
        indexes = [
            models.Index(fields=['date', 'time']),
        ]


class Income(Transaction):
    income_type = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"Income: {self.amount} on {self.date}"
    

class Expenditure(Transaction):
    expense_type = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"Expenditure: {self.amount} on {self.date}"


class TransactionCategory(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='subcategories'
    )

    def __str__(self):
        return f"{self.name} ({self.transaction_type})"

    def get_hierarchy(self):
        """Ritorna la gerarchia completa, utile per le visualizzazioni"""
        hierarchy = [self]
        parent = self.parent
        while parent is not None:
            hierarchy.append(parent)
            parent = parent.parent
        return hierarchy[::-1]  # Inverte per avere il percorso dal top

    class Meta:
        verbose_name_plural = "Transaction Categories"
