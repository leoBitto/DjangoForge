from django.contrib import admin
from .models import BankAccount, Cash, Income, Expenditure, IncomeCategory, ExpenseCategory, FundLog

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('institution', 'account_type', 'balance', 'start_date', 'end_date')
    search_fields = ('institution', 'account_type')

@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    list_display = ('description', 'balance', 'start_date', 'end_date')
    search_fields = ('description',)

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'type', 'description')
    list_filter = ('type', 'date')
    search_fields = ('description',)

@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'type', 'description')
    list_filter = ('type', 'date')
    search_fields = ('description',)

@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(FundLog)
class FundLogAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'balance', 'timestamp')
    search_fields = ('content_object',)
