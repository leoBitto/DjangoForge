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
    def get_log_content(self, log_path, log_name):
        try:
            with open(log_path, 'r') as file:
                # Leggi le ultime 1000 righe efficientemente
                file.seek(0, os.SEEK_END)
                file_size = file.tell()
                buffer_size = 8192
                file.seek(max(file_size - buffer_size, 0), 0)
                lines = file.readlines()[-1000:]
                return lines
        except FileNotFoundError:
            return f"{log_name} logging file has not been found."

    def get(self, request, *args, **kwargs):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        schedules_path = os.path.join(BASE_DIR, 'schedules.log')
        tasks_path = os.path.join(BASE_DIR, 'tasks.log')
        reports_path = os.path.join(BASE_DIR, 'reports.log')

        schedules_log_content = self.get_log_content(schedules_path, "Scheduler")
        tasks_log_content = self.get_log_content(tasks_path, "Tasks")
        reports_log_content = self.get_log_content(reports_path, "Reports")

        context = {
            'schedules_log_content': schedules_log_content,
            'tasks_log_content': tasks_log_content,
            'reports_log_content': reports_log_content
        }

        return render(request, 'logging_app/log_list.html', context)




