from django.contrib import admin
from .models import Image,Contact,Opening_hour, Gallery


class ImageAdmin(admin.ModelAdmin):
    list_display=('id', 'gallery', 'description', 'is_first', 'show_image')


class GalleryAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'get_images')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'mail')


class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('id', 'weekdays', 'weekend', 'closing_day')


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Opening_hour, OpeningHoursAdmin)