import plotly.graph_objs as go
import plotly.io as pio
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.utils import timezone
import logging

logger = logging.getLogger('reports')

def create_field_graph(title, data, x_labels, y_label):
    """
    Crea un grafico a linee utilizzando Plotly e restituisce il grafico come HTML.

    Args:
        title (str): Titolo del grafico.
        data (list): Dati da visualizzare nel grafico.
        x_labels (list): Etichette per l'asse x.
        y_label (str): Etichetta per l'asse y.

    Returns:
        str: Grafico come stringa HTML.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_labels,
        y=data,
        mode='lines+markers',
        name=title
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Periodo',
        yaxis_title=y_label,
        template='plotly_dark'  # Usa un tema scuro, o puoi cambiarlo secondo il tuo design
    )

    # Restituisce il grafico come stringa HTML
    return pio.to_html(fig, full_html=False)


def get_previous_periods(aggregation_model, selected_period, period_type, num_previous_periods):
    """
    Questa funzione restituisce i dati per i 6 periodi precedenti basati su `period_type`.
    - period_type può essere 'day', 'week', 'month', 'quarter', 'year'
    """
    previous_periods = []

    if period_type == 'day':
        for i in range(num_previous_periods):
            period = selected_period - timedelta(days=i)
            logger.info(f"period: {period}")
            query = Q(date=period)
            previous_periods.append(aggregation_model.objects.using('gold').filter(query))
        

    elif period_type == 'week':
        current_week = selected_period['week']
        #logger.info(f"current_week {current_week}, type {type(current_week)}")
        current_year = selected_period['year']
        #logger.info(f"current_year {current_year}, type {type(current_year)}")
        for i in range(num_previous_periods):
            # Gestire il cambio di anno
            if current_week - i <= 0:
                previous_year = current_year - 1
                previous_week = 52 + (current_week - i)  # Considera l'anno precedente
            else:
                previous_year = current_year
                previous_week = current_week - i

            query = Q(week=previous_week, year=previous_year)
            previous_periods.append(aggregation_model.objects.using('gold').filter(query))

    elif period_type == 'month':
        current_month = int(selected_period['month'])
        #logger.info(f"current_month {current_month}, type {type(current_month)}")
        current_year = selected_period['year']
        #logger.info(f"current_year {current_year}, type {type(current_year)}")
        for i in range(num_previous_periods):
            # Gestire il cambio di anno
            if current_month - i <= 0:
                previous_year = current_year - 1
                previous_month = 12 + (current_month - i)
            else:
                previous_year = current_year
                previous_month = current_month - i

            query = Q(month=previous_month, year=previous_year)
            previous_periods.append(aggregation_model.objects.using('gold').filter(query))

    elif period_type == 'quarter':
        current_quarter = int(selected_period['quarter'])
        #logger.info(f"current_quarter {current_quarter}, type {type(current_quarter)}")
        current_year = selected_period['year']
        #logger.info(f"current_year {current_year}, type {type(current_year)}")
        for i in range(num_previous_periods):
            # Gestire il cambio di anno
            if current_quarter - i <= 0:
                previous_year = current_year - 1
                previous_quarter = 4 + (current_quarter - i)
            else:
                previous_year = current_year
                previous_quarter = current_quarter - i

            query = Q(quarter=previous_quarter, year=previous_year)
            previous_periods.append(aggregation_model.objects.using('gold').filter(query))

    elif period_type == 'year':
        current_year = selected_period['year']
        #logger.info(f"current_year {current_year}, type {type(current_year)}")
        for i in range(num_previous_periods):
            previous_year = current_year - i
            query = Q(year=previous_year)

            #logger.info(f"previous year : {previous_year}")
            #logger.info(f"query : {query}")

            previous_periods.append(aggregation_model.objects.using('gold').filter(query))

    logger.info(f"model : {aggregation_model}")
    logger.info(f"selected period : {selected_period}")
    logger.info(f"period type : {period_type}")
    logger.info(f"previous periods : {previous_periods}")


    return previous_periods

# Helper per gli intervalli di date
def get_today():
    return timezone.now().date()

def get_week_params(today):
    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)
    return {'week': today.isocalendar()[1], 'year': today.year}, [start_of_week, end_of_week]

def get_month_params(today):
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)
    return {'month': today.month, 'year': today.year}, [start_of_month, end_of_month]

def get_quarter_params(today):
    quarter = (today.month - 1) // 3 + 1
    start_of_quarter = timezone.datetime(today.year, 3 * quarter - 2, 1).date()
    end_of_quarter = (timezone.datetime(today.year, 3 * quarter + 1, 1) - timezone.timedelta(days=1)).date()
    return {'quarter': quarter, 'year': today.year}, [start_of_quarter, end_of_quarter]

def get_year_params(today):
    start_of_year = today.replace(month=1, day=1)
    end_of_year = today.replace(month=12, day=31)
    return {'year': today.year}, [start_of_year, end_of_year]