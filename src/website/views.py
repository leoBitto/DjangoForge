from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from webpush import send_group_notification, send_user_notification
from django.contrib import messages
    
def base(request):

    # Ritorna la risposta al render della pagina di destinazione
    return render(request, 'website/landing.html', {})


