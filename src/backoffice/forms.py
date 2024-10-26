from django import forms
from django.core.exceptions import ValidationError

class ReportTypeForm(forms.Form):
    REPORT_CHOICES = [
        ('daily', 'Giornaliero'),
        ('weekly', 'Settimanale'),
        ('monthly', 'Mensile'),
        ('quarterly', 'Trimestrale'),
        ('yearly', 'Annuale'),
    ]

    aggregation_type = forms.ChoiceField(
        choices=REPORT_CHOICES, 
        label="Tipo di Report",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class DailyAggregationForm(forms.Form):
    date = forms.DateField(
        label="Data",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )

class WeeklyAggregationForm(forms.Form):
    year = forms.IntegerField(
        label="Anno",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True
    )
    week = forms.IntegerField(
        label="Settimana",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,
        min_value=1,
        max_value=52
    )

class MonthlyAggregationForm(forms.Form):
    year = forms.IntegerField(
        label="Anno",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True
    )
    month = forms.ChoiceField(
        label="Mese",
        choices=[(i, month) for i, month in enumerate([
            'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
            'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'
        ], 1)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

class QuarterlyAggregationForm(forms.Form):
    year = forms.IntegerField(
        label="Anno",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True
    )
    quarter = forms.ChoiceField(
        label="Trimestre",
        choices=[(1, 'Q1'), (2, 'Q2'), (3, 'Q3'), (4, 'Q4')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

class YearlyAggregationForm(forms.Form):
    year = forms.IntegerField(
        label="Anno",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True
    )
