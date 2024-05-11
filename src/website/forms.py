from django import forms
from .models import Image, Contact, Opening_hour, Gallery
from webpush.models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['gallery', 'description', 'img', 'is_first']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Necessaria ad identificarla'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['phone', 'mail']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Inserisci il numero di telefono'}),
            'mail': forms.TextInput(attrs={'placeholder': 'Inserisci l\'indirizzo email'}),
        }


class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = Opening_hour
        fields = ['weekdays', 'weekend', 'closing_day']
        widgets = {
            'weekdays': forms.TextInput(attrs={'placeholder': 'Inserisci gli orari settimanali'}),
            'weekend': forms.TextInput(attrs={'placeholder': 'Inserisci gli orari del weekend'}),
            'closing_day': forms.TextInput(attrs={'placeholder': 'Inserisci un giorno della settimana'}),
        }


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['name', 'images']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Non usare spazi nel nome'}),            
            'images': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    images = forms.ModelMultipleChoiceField(
        queryset=Image.objects.filter(gallery__isnull=True), 
        required=False
    )

    def save(self, commit=True):
        gallery = super().save(commit=False)
        if commit:
            gallery.save()

            # Associa le immagini selezionate alla galleria
            images = self.cleaned_data.get('images')
            if images:
                for image in images:
                    image.gallery = gallery
                    image.save()

        return gallery