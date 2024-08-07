from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
import plotly.graph_objs as go
from django.db.models import Count
from logging_app.models import AccessLog, ErrorLog
from .models import AggregatedAccessLog, AggregatedErrorLog
import logging

logger = logging.getLogger('gold_bi')


class AEGraphsView(View):

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
            error_daily_chart = self.create_weekly_distribution_chart(error_data, 'Errors by Day of Week', 'it')
            access_hourly_chart = self.create_hourly_distribution_chart(access_data, 'Accesses by Hour')
            access_daily_chart = self.create_weekly_distribution_chart(access_data, 'Accesses by Day of Week', 'it')

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
    

    def create_weekly_distribution_chart(self, data, title, language='en'):
        """
        Crea un grafico a barre che mostra il conteggio degli eventi per ogni giorno della settimana.
        """
        # Mappatura dei giorni della settimana in inglese e italiano
        day_mapping = {
            1: {'en': 'sunday', 'it': 'domenica'},
            2: {'en': 'monday', 'it': 'lunedì'},
            3: {'en': 'tuesday', 'it': 'martedì'},
            4: {'en': 'wednesday', 'it': 'mercoledì'},
            5: {'en': 'thursday', 'it': 'giovedì'},
            6: {'en': 'friday', 'it': 'venerdì'},
            7: {'en': 'saturday', 'it': 'sabato'}
        }
        #logger.info(data)
        
        # Controllo della lingua
        if language not in ['en', 'it']:
            raise ValueError(f"Unsupported language: {language}. Supported languages are 'en' and 'it'.")
    
        # Aggregazione dei dati per giorni
        # Inizializza il dizionario con tutti i giorni
        day_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}

        for entry in data:
            if not hasattr(entry, 'day') or not hasattr(entry, 'count'):
                raise ValueError("Data entry is missing 'day' or 'count' attribute.")
            
            day = int(entry.day)  # Assicurati che day sia un numero intero
            count = entry.count

            if day not in day_counts:
                raise ValueError(f"Invalid day value: {day}. Expected values are 1 through 7.")
            
            day_counts[day] += count

        #logger.info(f"day counts {day_counts}")

        # Conversione dei numeri dei giorni in nomi dei giorni
        try:
            day_names = [day_mapping[day][language] for day in sorted(day_counts.keys())]
            counts = [day_counts[day] for day in sorted(day_counts.keys())]
        except KeyError as e:
            raise ValueError(f"Error in day mapping: {e}")
        
        #logger.info(f"day names {day_names}")
        #logger.info(f"counts {counts}")

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

