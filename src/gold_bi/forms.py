from django import forms
from django.core.exceptions import ValidationError
import datetime

# Lista dei mesi
MONTH_CHOICES = [
    (1, 'Gennaio'),
    (2, 'Febbraio'),
    (3, 'Marzo'),
    (4, 'Aprile'),
    (5, 'Maggio'),
    (6, 'Giugno'),
    (7, 'Luglio'),
    (8, 'Agosto'),
    (9, 'Settembre'),
    (10, 'Ottobre'),
    (11, 'Novembre'),
    (12, 'Dicembre'),
]

class ReportPeriodForm(forms.Form):
    year = forms.IntegerField(
        label="Anno",
        min_value=2000,
        max_value=2100,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    month = forms.ChoiceField(
        label="Mese",
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class TemporalAggregationForm(forms.Form):
    AGGREGATION_TYPE_CHOICES = [
        ('daily', 'Giornaliera'),
        ('weekly', 'Settimanale'),
        ('monthly', 'Mensile'),
        ('quarterly', 'Trimestrale'),
        ('yearly', 'Annuale'),
    ]

    aggregation_type = forms.ChoiceField(
        choices=AGGREGATION_TYPE_CHOICES,
        label="Tipo di Aggregazione Temporale",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    start_date = forms.DateField(
        label="Data Inizio",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    end_date = forms.DateField(
        label="Data Fine",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', 'La data di fine deve essere successiva alla data di inizio.')
        
        return cleaned_data
