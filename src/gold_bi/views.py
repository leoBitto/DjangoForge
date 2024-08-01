from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
import plotly.graph_objs as go
from django.db.models import Count
from logging_app.models import AccessLog, ErrorLog
from .models import AggregatedAccessLog, AggregatedErrorLog
import logging

logger = logging.getLogger('gold_bi')


class GraphsView(View):

    def get(self, request):
        try:

            error_data = AggregatedErrorLog.objects.using('gold').all()
            access_data = AggregatedAccessLog.objects.using('gold').all()

            # Controlla se i dati sono stati trovati
            if not error_data:
                logger.info("No aggregated errors found.")
            if not access_data:
                logger.info("No aggregated access logs found.")



            # Grafici
            error_hourly_chart = self.create_hourly_distribution_chart(error_data, 'Errors by Hour')
            error_daily_chart = self.create_weekly_distribution_chart(error_data, 'Errors by Day of Week')
            access_hourly_chart = self.create_hourly_distribution_chart(access_data, 'Accesses by Hour')
            access_daily_chart = self.create_weekly_distribution_chart(access_data, 'Accesses by Day of Week')

            logger.info('Graphs created successfully.')

            # Passa i dati al template della dashboard
            return render(request, 'gold_bi/graphs.html', {
                'error_hourly_chart': error_hourly_chart,
                'error_daily_chart': error_daily_chart,
                'access_hourly_chart': access_hourly_chart,
                'access_daily_chart': access_daily_chart,
            })
        except Exception as e:
            logger.error('Error in GraphsView: %s', e)
            return render(request, 'gold_bi/graphs.html', {
                'error': 'An error occurred while generating the graphs.',
                'error_message': str(e),
            })



    def create_response_code_pie_chart(self, response_codes):
        """
        Crea un grafico a torta che visualizza la distribuzione dei codici di stato delle risposte.
        """
        fig = go.Figure(data=[go.Pie(labels=[entry['response_code'] for entry in response_codes], values=[entry['count'] for entry in response_codes])])
        fig.update_layout(title='Response Code Distribution')
        return fig.to_html(full_html=False)
    

    def create_weekly_distribution_chart(self, data, title):
        """
        Crea un grafico a barre che mostra il conteggio degli eventi per ogni giorno della settimana.
        """
        # Mappatura dei giorni della settimana (Domenica = 1, ..., Sabato = 7)
        day_mapping = {
            '1': 'Sunday',
            '2': 'Monday',
            '3': 'Tuesday',
            '4': 'Wednesday',
            '5': 'Thursday',
            '6': 'Friday',
            '7': 'Saturday'
        }

        # Aggregazione dei dati per giorni
        day_counts = {}
        for entry in data:
            day = entry.day
            count = entry.count
            if day in day_counts:
                day_counts[day] += count
            else:
                day_counts[day] = count

        # Conversione dei numeri dei giorni in nomi dei giorni
        day_names = [day_mapping[day] for day in sorted(day_counts.keys())]
        counts = [day_counts[day] for day in sorted(day_counts.keys())]

        # Creazione del grafico a barre
        fig = go.Figure()
        fig.add_trace(go.Bar(x=day_names, y=counts))

        # Aggiornamento del layout del grafico
        fig.update_layout(
            title=title,
            xaxis_title='Day of Week',
            yaxis_title='Count'
        )
        return fig.to_html(full_html=False)


    def create_hourly_distribution_chart(self, data, title):
        """
        Crea un grafico a barre che mostra il conteggio degli eventi per ogni ora della giornata.
        """
        # Aggregazione dei dati per ore
        hour_counts = {}
        for entry in data:
            hour = entry.hour
            count = entry.count
            if hour in hour_counts:
                hour_counts[hour] += count
            else:
                hour_counts[hour] = count


        # Creazione del grafico a barre
        fig = go.Figure()
        fig.add_trace(go.Bar(x=list(sorted(hour_counts.keys())), y=[hour_counts[hour] for hour in sorted(hour_counts.keys())]))
        fig.update_layout(title=title, xaxis_title='Hour of Day', yaxis_title='Count')
        return fig.to_html(full_html=False)



class AEListView(View):
    def get(self, request):
        # Recupera i log aggregati per la lista
        accesslogs = AccessLog.objects.order_by('-timestamp')[:50]
        errorlogs = ErrorLog.objects.order_by('-timestamp')[:50]

        # Passa i dati al template della dashboard
        return render(request, 'gold_bi/AElist.html', {
            'accesslogs': accesslogs,
            'errorlogs': errorlogs,
        })


class AccessLogDetailView(View):
    def get(self, request, log_id):
        # Recupera il log specifico
        log = get_object_or_404(AccessLog, pk=log_id)

        # Passa il log al template dei dettagli del log
        return render(request, 'gold_bi/log_detail.html', {'log': log})


class ErrorLogDetailView(View):
    def get(self, request, log_id):
        # Recupera il log specifico
        log = get_object_or_404(ErrorLog, pk=log_id)

        # Passa il log al template dei dettagli del log
        return render(request, 'gold_bi/log_detail.html', {'log': log})

