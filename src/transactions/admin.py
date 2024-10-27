from django.contrib import admin
from .models.base import BankAccount, Cash, Transaction, TransactionCategory, FundLog

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('institution', 'account_type', 'balance', 'start_date', 'end_date', 'is_active')
    search_fields = ('institution', 'account_type')
    list_filter = ('account_type', 'is_active', 'start_date')
    actions = ['mark_as_active', 'mark_as_inactive']

    @admin.action(description="Mark selected bank accounts as active")
    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Mark selected bank accounts as inactive")
    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    list_display = ('description', 'balance', 'start_date', 'end_date', 'is_active')
    search_fields = ('description',)
    list_filter = ('is_active', 'start_date')
    actions = ['mark_as_active', 'mark_as_inactive']

    @admin.action(description="Mark selected cash as active")
    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Mark selected cash as inactive")
    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'transaction_type', 'category', 'description')
    list_filter = ('transaction_type', 'category', 'date')
    search_fields = ('description', 'category__name')


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'transaction_type', 'parent', 'description')
    search_fields = ('name', 'parent__name')
    list_filter = ('transaction_type',)

    def get_queryset(self, request):
        """Ottieni la gerarchia completa di categorie, utile per la visualizzazione"""
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('parent')
        return queryset


@admin.register(FundLog)
class FundLogAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'balance', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('content_object__name',)
