from django import forms

class ReportTypeForm(forms.Form):
    REPORT_CHOICES = [
        ('daily', 'Giornaliero'),
        ('weekly', 'Settimanale'),
        ('monthly', 'Mensile'),
        ('quarterly', 'Trimestrale'),
        ('yearly', 'Annuale'),
    ]

    report_type = forms.ChoiceField(
        choices=REPORT_CHOICES, 
        label="Tipo di Report",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    start_date = forms.DateField(
        label="Data di Inizio",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )
    
    end_date = forms.DateField(
        label="Data di Fine",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        
        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', "La data di fine deve essere successiva alla data di inizio.")
