import plotly.graph_objs as go
import plotly.io as pio
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


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


def get_previous_months(year, month, num_months=6):
    """
    Calcola i mesi precedenti a partire da una data specificata.

    Questa funzione genera una lista di tuple che rappresentano i mesi precedenti, a partire dal mese e anno forniti.
    La lista includerà il mese e anno specificati e i `num_months - 1` mesi precedenti.

    Args:
        year (int): L'anno del mese di partenza.
        month (int): Il mese di partenza (1-12).
        num_months (int, opzionale): Il numero totale di mesi da includere nella lista, inclusi il mese corrente. 
                                      Il valore predefinito è 6.

    Returns:
        List[Tuple[int, int]]: Una lista di tuple, ciascuna rappresentante un mese e anno precedenti, 
                               ordinate dal mese più recente al meno recente.

    Examples:
        >>> get_previous_months(2024, 8)
        [(2024, 8), (2024, 7), (2024, 6), (2024, 5), (2024, 4), (2024, 3)]

        >>> get_previous_months(2023, 1, num_months=3)
        [(2023, 1), (2022, 12), (2022, 11)]
    """
    # Creiamo una lista per salvare i risultati
    previous_months = []

    # Partiamo dal mese e dall'anno corrente
    current_date = datetime(year, month, 1)

    # Calcoliamo i mesi precedenti
    for _ in range(num_months):
        # Aggiungiamo la coppia (anno, mese) alla lista
        previous_months.append((current_date.year, current_date.month))
        # Sottraiamo un mese
        current_date -= relativedelta(months=1)

    return previous_months


def create_field_graph(field_name, data, labels, title):
    """
    Crea un grafico per un campo specifico.

    :param field_name: Nome del campo da graficare.
    :param data: I valori da visualizzare.
    :param labels: Le etichette delle ascisse (tipicamente i mesi o le date).
    :param title: Titolo del grafico.
    :return: Il grafico in formato HTML.
    """
    trace = go.Scatter(x=labels, y=data, mode='lines', name=field_name)
    
    layout = go.Layout(
        title=title,
        xaxis={'title': 'Period'},
        yaxis={'title': field_name},
        height=400
    )

    fig = go.Figure(data=[trace], layout=layout)
    graph_html = pio.to_html(fig, full_html=False)

    return graph_html
