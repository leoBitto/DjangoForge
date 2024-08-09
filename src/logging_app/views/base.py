from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from logging_app.models import AccessRequestLog, ErrorRequestLog
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from pathlib import Path


class AEListView(LoginRequiredMixin, View):
    def get(self, request):
        # Recupera i log aggregati per la lista
        accesslogs = AccessRequestLog.objects.order_by('-timestamp')[:50]
        errorlogs = ErrorRequestLog.objects.order_by('-timestamp')[:50]

        # Passa i dati al template della dashboard
        return render(request, 'logging_app/AElist.html', {
            'accesslogs': accesslogs,
            'errorlogs': errorlogs,
        })


class AccessLogDetailView(LoginRequiredMixin, View):
    def get(self, request, log_id):
        # Recupera il log specifico
        log = get_object_or_404(AccessRequestLog, pk=log_id)

        # Passa il log al template dei dettagli del log
        return render(request, 'logging_app/request_log_detail.html', {'log': log})


class ErrorLogDetailView(LoginRequiredMixin, View):
    def get(self, request, log_id):
        # Recupera il log specifico
        log = get_object_or_404(ErrorRequestLog, pk=log_id)

        # Passa il log al template dei dettagli del log
        return render(request, 'logging_app/request_log_detail.html', {'log': log})


class ReadLogView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        file_path = os.path.join(BASE_DIR, 'app.log')

        try:
            with open(file_path, 'r') as file:
                # Leggi tutte le righe e prendi le ultime 100
                lines = file.readlines()[-1000:]
                # Unisci le righe in un singolo blocco di testo
                lines.reverse()
                log_content = lines
        except FileNotFoundError:
            log_content = "File non trovato."

        return render(request, 'logging_app/log_list.html', {'log_content': log_content})
    




