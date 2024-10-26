from django.shortcuts import render
from django.views.generic import View
import plotly.graph_objs as go
from logging_app.models import AggregatedAccessLog, AggregatedErrorLog
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger('app')


class AEGraphsView(LoginRequiredMixin, View):

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
            return render(request, 'logging_app/graphs.html', {
                'error_hourly_chart': error_hourly_chart,
                'error_daily_chart': error_daily_chart,
                'access_hourly_chart': access_hourly_chart,
                'access_daily_chart': access_daily_chart,
            })
        except Exception as e:
            logger.error('Error in GraphsView: %s', e)
            return render(request, 'logging_app/graphs.html', {
                'error': 'An error occurred while generating the graphs.',
                'error_message': str(e),
            })



    def create_response_code_pie_chart(self, response_codes):
        """
        Crea un grafico a torta che visualizza la distribuzione dei codici di stato delle risposte.
        """
        try:
            fig = go.Figure(data=[go.Pie(labels=[entry['response_code'] for entry in response_codes], values=[entry['count'] for entry in response_codes])])
            fig.update_layout(title='Response Code Distribution')
            return fig.to_html(full_html=False)
        except Exception as e:
            raise Exception(f"Errore durante la creazione del grafico: {str(e)}") from e
    
    def create_weekly_distribution_chart(self, data, title):
        try:
            day_mapping = {
                1: 'Sunday',
                2: 'Monday',
                3: 'Tuesday',
                4: 'Wednesday',
                5: 'Thursday',
                6: 'Friday',
                7: 'Saturday'
            }

            day_counts = {}
            for entry in data:
                day = entry.day
                count = entry.count
                if day in day_counts:
                    day_counts[day] += count
                else:
                    day_counts[day] = count

            day_names = [day_mapping[day] for day in sorted(day_counts.keys())]
            counts = [day_counts[day] for day in sorted(day_counts.keys())]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=day_names, y=counts))

            fig.update_layout(
                title=title,
                xaxis_title='Day of Week',
                yaxis_title='Count'
            )
            return fig.to_html(full_html=False)
        except Exception as e:
            raise Exception(f"Errore durante la creazione del grafico settimanale: {str(e)}") from e


    def create_hourly_distribution_chart(self, data, title):
            try:
                hour_counts = {}
                for entry in data:
                    hour = entry.hour
                    count = entry.count
                    if hour in hour_counts:
                        hour_counts[hour] += count
                    else:
                        hour_counts[hour] = count

                fig = go.Figure()
                fig.add_trace(go.Bar(x=list(sorted(hour_counts.keys())), y=[hour_counts[hour] for hour in sorted(hour_counts.keys())]))
                fig.update_layout(title=title, xaxis_title='Hour of Day', yaxis_title='Count')
                return fig.to_html(full_html=False)
            except Exception as e:
                raise Exception(f"Errore durante la creazione del grafico orario: {str(e)}") from e



