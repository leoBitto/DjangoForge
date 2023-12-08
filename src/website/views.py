from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Image, Contact, Opening_hour, Gallery
from .forms import ImageForm, ContactForm, OpeningHourForm, GalleryForm
from django.contrib import messages

# this is the part of the website accessible only to admin
@login_required
def dashboard(request):
    
    # Recupera tutte le istanze dei modelli
    gallery_images = Image.objects.all()
    contacts = Contact.objects.all()
    opening_hours = Opening_hour.objects.all()
    gallery = Gallery.objects.all()

    context = {
        'gallery_images': gallery_images,
        'contacts': contacts,
        'opening_hours': opening_hours,
        'gallery': gallery,
    }

    return render(request, 'website/dashboard/dashboard.html', context)

@login_required
def image_page(request):
    images = Image.objects.all()
    form = ImageForm()

    context = {
        'images': images,
        'form': form,
    }

    return render(request, 'website/dashboard/image_page.html', context)
    
@login_required
def add_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Immagine aggiunta con successo.')
            return redirect('website:image_page')
        else:
            messages.error(request, 'Si è verificato un errore. Si prega di correggere il modulo.')
            return render(request, 'website/dashboard/image_page.html', {'form': form})
    else:
        form = ImageForm()

    return render(request, 'website/dashboard/image_page.html', {'form': form})

@login_required
def delete_image(request, image_id):
    # Trova l'immagine nel database
    image = get_object_or_404(Image, id=image_id)

    # Elimina l'immagine
    image.delete()
    messages.success(request, 'Immagine eliminata con successo.')
    return redirect('website:image_page')


@login_required
def gallery_page(request):
    galleries = Gallery.objects.all()
    form = GalleryForm()

    context = {
        'galleries': galleries,
        'form': form,
    }

    return render(request, 'website/dashboard/gallery_page.html', context)
    
@login_required
def add_gallery(request):
    print(request)
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Galleria aggiunta con successo.')
            return redirect('website:gallery_page')
        else:
            messages.error(request, 'Si è verificato un errore. Si prega di correggere il modulo.')
            return render(request, 'website/dashboard/gallery_page.html', {'form': form})
    else:
        form = ImageForm()

    return render(request, 'website/dashboard/gallery_page.html', {'form': form})

@login_required
def delete_gallery(request, gallery_id):
    # Trova l'immagine nel database
    gallery = get_object_or_404(Gallery, id=gallery_id)

    # Elimina l'immagine
    gallery.delete()
    messages.success(request, 'Galleria eliminata con successo.')
    return redirect('website:gallery_page')


@login_required
def contact_page(request):
    contacts = Contact.objects.all()
    form = ContactForm()
    context = {
        'contacts': contacts,
        'form':form,
    }

    return render(request, 'website/dashboard/contact_page.html', context)

@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contatto aggiunto con successo.')
            return redirect('website:contact_page')
        else:
            messages.error(request, 'Si è verificato un errore. Si prega di correggere il modulo.')
            return render(request, 'website/dashboard/contact_page.html', {'form': form})
    else:
        form = ContactForm()

    return render(request, 'website/dashboard/contact_page.html', {'form': form})

@login_required
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    contact.delete()
    messages.success(request, 'Contatto eliminato con successo.')
    return redirect('website:contact_page')


@login_required
def opening_hours_page(request):
    opening_hours = Opening_hour.objects.all()
    form = OpeningHourForm()
    context = {
        'opening_hours': opening_hours,
        'form':form,
    }

    return render(request, 'website/dashboard/opening_hours_page.html', context)

@login_required
def add_opening_hour(request):
    if request.method == 'POST':
        form = OpeningHourForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Orario aggiunto con successo. Ricorda di cambiare gli orari anche su Google.')
            return redirect('website:opening_hours_page')
        else:
            messages.error(request, 'Si è verificato un errore. Si prega di correggere il modulo.')
            return render(request, 'website/dashboard/opening_hours_page.html', {'form': form})
    else:
        form = OpeningHourForm()

    return render(request, 'website/dashboard/opening_hours_page.html', {'form': form})

@login_required
def delete_opening_hour(request, opening_hour_id):
    hours = get_object_or_404(Opening_hour, pk=opening_hour_id)
    hours.delete()
    messages.success(request, 'Orario eliminato con successo.')
    return redirect('website:opening_hours_page')



# this is part of the website accessible to everyone
def base(request):
    
    context = {}

    return render(request, 'website/landing.html', context)