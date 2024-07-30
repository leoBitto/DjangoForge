from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from webpush import send_group_notification, send_user_notification

    
def base(request):
    # Verifica se l'utente esiste prima di tentare di inviare la notifica
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        # Gestione nel caso l'utente non esista
        # Ad esempio, mostra un messaggio di errore o esegui un'altra azione
        return render(request, 'website/landing.html', {'error_message': 'L\'utente specificato non esiste'})

    # Costruisci il payload della notifica
    payload = {
        "head": "Benvenuto! " + user.username,
        "body": "Ciao Mondo",
        "icon": "https://i.imgur.com/dRDxiCQ.png",
        "url": "https://www.example.com"
    }

    # Invia la notifica all'utente specificato
    send_user_notification(user=user, payload=payload, ttl=1000)

    # Ritorna la risposta al render della pagina di destinazione
    return render(request, 'website/landing.html', {'success_message': 'Notifica inviata con successo'})