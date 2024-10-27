from django import forms
from .models.base import Transaction, TransactionCategory, BankAccount, Cash
from django.contrib.contenttypes.models import ContentType



class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['balance', 'start_date', 'end_date', 'account_type', 'institution', 'interest_rate']
        labels = {
            'balance': 'Balance',
            'start_date': 'Start date',
            'end_date': 'End date',
            'account_type': 'Account type',
            'institution': 'Institution',
            'interest_rate': 'Interest rate',
        }
        widgets = {
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the balance'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select the start date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select the end date (optional)'}),
            'account_type': forms.Select(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the institution name'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the interest rate (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['balance'].widget.attrs.update({'placeholder': 'Enter the balance'})
        self.fields['start_date'].widget.attrs.update({'placeholder': 'Select the start date'})
        self.fields['end_date'].widget.attrs.update({'placeholder': 'Select the end date (optional)'})
        self.fields['institution'].widget.attrs.update({'placeholder': 'Enter the name of the institution'})
        self.fields['interest_rate'].widget.attrs.update({'placeholder': 'Enter the interest rate (optional)'})
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if end_date and start_date and end_date <= start_date:
            self.add_error('end_date', "The end date must be after the start date.")

        return cleaned_data
    

class CashForm(forms.ModelForm):
    class Meta:
        model = Cash
        fields = ['balance', 'start_date', 'end_date', 'description']
        labels = {
            'balance': 'Balance',
            'start_date': 'Start date',
            'end_date': 'End date',
            'description': 'Description',
        }
        widgets = {
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the balance'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select the start date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select the end date (optional)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter a description (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['balance'].widget.attrs.update({'placeholder': 'Enter the balance'})
        self.fields['start_date'].widget.attrs.update({'placeholder': 'Select the start date'})
        self.fields['end_date'].widget.attrs.update({'placeholder': 'Select the end date (optional)'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Enter a description (optional)'})

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if end_date and start_date and end_date <= start_date:
            self.add_error('end_date', "The end date must be after the start date.")

        return cleaned_data


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'time', 'amount', 'description', 'transaction_type', 'category', 'related_fund']
        labels = {
            'date': 'Date',
            'time': 'Time',
            'amount': 'Amount',
            'description': 'Description',
            'transaction_type': 'Transaction Type',
            'category': 'Category',
            'related_fund': 'Fund',
        }
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'related_fund': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra le categorie in base al tipo di transazione
        self.fields['category'].queryset = TransactionCategory.objects.none()
        
        if 'transaction_type' in self.data:
            transaction_type = self.data.get('transaction_type')
            self.fields['category'].queryset = TransactionCategory.objects.filter(transaction_type=transaction_type)

        elif self.instance.pk:
            self.fields['category'].queryset = TransactionCategory.objects.filter(transaction_type=self.instance.transaction_type)

        # Filtra i fondi utilizzabili
        self.fields['related_fund'].queryset = ContentType.objects.filter(model__in=['bankaccount', 'cash'])

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be positive.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        category = cleaned_data.get('category')

        if category and transaction_type and category.transaction_type != transaction_type:
            self.add_error('category', "Category must match the transaction type (income or expense).")

        return cleaned_data


class TransferFundsForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        label='Amount',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'})
    )
    source_fund = forms.ModelChoiceField(
        queryset=BankAccount.objects.all() | Cash.objects.all(),
        label='Source Fund',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    destination_fund = forms.ModelChoiceField(
        queryset=BankAccount.objects.all() | Cash.objects.all(),
        label='Destination Fund',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    commission = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        initial=0.00,
        label='Commission',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter commission (optional)'})
    )

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        source_fund = cleaned_data.get('source_fund')
        destination_fund = cleaned_data.get('destination_fund')
        commission = cleaned_data.get('commission')

        if source_fund == destination_fund:
            self.add_error('destination_fund', "The source and destination funds cannot be the same.")
        
        if amount <= 0:
            self.add_error('amount', "Amount must be greater than zero.")

        if source_fund.balance < amount + (commission or 0):
            self.add_error('source_fund', "Insufficient funds in the source fund.")

        return cleaned_data


class RecurringTransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    frequency = forms.ChoiceField(
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('annual', 'Annual')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    description = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=TransactionCategory.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    related_fund = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(model__in=['bankaccount', 'cash']),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if end_date and end_date <= start_date:
            self.add_error('end_date', "End date must be after start date.")
        
        return cleaned_data


class TransactionCategoryForm(forms.ModelForm):
    class Meta:
        model = TransactionCategory
        fields = ['name', 'description', 'transaction_type', 'parent']
        labels = {
            'name': 'Category Name',
            'description': 'Description',
            'transaction_type': 'Type',
            'parent': 'Parent Category',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra il campo parent per mostrare solo categorie dello stesso tipo
        if 'transaction_type' in self.data:
            transaction_type = self.data.get('transaction_type')
            self.fields['parent'].queryset = TransactionCategory.objects.filter(transaction_type=transaction_type)
        elif self.instance.pk:
            self.fields['parent'].queryset = TransactionCategory.objects.filter(transaction_type=self.instance.transaction_type)


