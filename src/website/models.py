from django.db import models
from django.utils.html import format_html
from django.conf import settings
import os

### information models
class Gallery(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Galleries'
        

    def get_images(self):
        return self.images.all()
    
    def __str__(self):
        return self.name
    

class Image(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images', null=True, blank=True, help_text="Non necessario se non deve essere inserita in una galleria")
    description = models.CharField(max_length=300, default="", blank=True, null=True, help_text="identifica l'immagine")
    img = models.ImageField(upload_to="", blank=True, null=True)
    is_first = models.BooleanField(default=False, help_text="clicca se vuoi che sia la prima ad essere visualizzata in un eventuale galleria")


    def show_image(self):
        return format_html('<img src="{}" style="height:250px;" />', self.img.url)

    def __str__(self):
        return self.img.url
    
    def delete(self, *args, **kwargs):
        # Elimina il file dal server
        if self.img:
            path = os.path.join(settings.MEDIA_ROOT, str(self.img))
            os.remove(path)

        super().delete(*args, **kwargs)


class Contact(models.Model):
    phone = models.CharField(max_length=100, blank=True, null=True)
    mail = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return "Contacts"


class Opening_hour(models.Model):
    weekdays = models.CharField(max_length = 200, blank=True, null=True)
    weekend = models.CharField(max_length=300, blank=True, null=True)
    closing_day = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return "Opening hours"