from django import forms
from .models import *


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


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['date', 'time', 'amount', 'description', 'type', 'related_fund']
        labels = {
            'date': 'Date',
            'time': 'Time',
            'amount': 'Amount',
            'description': 'Description',
            'type': 'Type',
            'related_fund': 'Fund',
        }
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select the date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Select the time (optional)'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the amount'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter a description (optional)'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'related_fund': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_fund'].queryset = ContentType.objects.filter(model__in=['bankaccount', 'cash'])

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be positive.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        related_fund = cleaned_data.get('related_fund')

        if related_fund:
            try:
                content_type = ContentType.objects.get_for_id(related_fund.id)
                model_class = content_type.model_class()
                
                if self.instance.pk:  # Usa self.instance.pk se l'oggetto esiste
                    obj = model_class.objects.get(id=self.instance.pk)
                else:
                    raise forms.ValidationError(f"There is no object with that id.")

                self.instance.related_fund = content_type
                self.instance.object_id = obj.id
            except (ContentType.DoesNotExist, model_class.DoesNotExist):
                raise forms.ValidationError("Invalid related fund type or object ID.")

        return cleaned_data


class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ['date', 'time', 'amount', 'description', 'type', 'related_fund']
        labels = {
            'date': 'Date',
            'time': 'Time',
            'amount': 'Amount',
            'description': 'Description',
            'type': 'Type',
            'related_fund': 'Fund',
        }
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select the date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Select the time (optional)'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the amount'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter a description (optional)'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'related_fund': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_fund'].queryset = ContentType.objects.filter(model__in=['bankaccount', 'cash'])

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be positive.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        related_fund = cleaned_data.get('related_fund')

        if related_fund:
            try:
                content_type = ContentType.objects.get_for_id(related_fund.id)
                model_class = content_type.model_class()
                
                if self.instance.pk:  # Usa self.instance.pk se l'oggetto esiste
                    obj = model_class.objects.get(id=self.instance.pk)
                else:
                    raise forms.ValidationError(f"There is no object with that id.")

                self.instance.related_fund = content_type
                self.instance.object_id = obj.id
            except (ContentType.DoesNotExist, model_class.DoesNotExist):
                raise forms.ValidationError("Invalid related fund type or object ID.")

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



class RecurringIncomeForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Amount',
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'})
    )
    frequency = forms.ChoiceField(
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('annual', 'Annual'),
        ],
        label='Frequency',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Start Date'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
        label='End Date'
    )
    description = forms.CharField(
        max_length=100,
        required=False,
        label='Description',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter description (optional)'})
    )
    income_type = forms.ModelChoiceField(
        queryset=IncomeCategory.objects.all(),
        label='Income Type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    related_fund = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(model__in=['bankaccount', 'cash']),
        label='Related Fund',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if end_date and start_date and end_date <= start_date:
            self.add_error('end_date', "End date must be after start date.")

        return cleaned_data


class RecurringExpenseForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Amount',
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'})
    )
    frequency = forms.ChoiceField(
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('annual', 'Annual'),
        ],
        label='Frequency',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Start Date'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
        label='End Date'
    )
    description = forms.CharField(
        max_length=100,
        required=False,
        label='Description',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter description (optional)'})
    )
    expenditure_type = forms.ModelChoiceField(
        queryset=ExpenseCategory.objects.all(),
        label='Expense Type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    related_fund = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(model__in=['bankaccount', 'cash']),
        label='Related Fund',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if end_date and start_date and end_date <= start_date:
            self.add_error('end_date', "End date must be after start date.")

        return cleaned_data




