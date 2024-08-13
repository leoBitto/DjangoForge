from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View
import plotly.graph_objs as go
from gold_bi.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .utils import *


class ReportTypeSelectionView(LoginRequiredMixin, View):
    def get(self, request):
        # Inizializza i form
        monthly_snapshot_form = ReportPeriodForm()
        quality_control_form = ReportPeriodForm()
        temporal_aggregation_form = TemporalAggregationForm()
        return render(request, 'gold_bi/report/select_report_type.html', {
            'monthly_snapshot_form': monthly_snapshot_form,
            'quality_control_form': quality_control_form,
            'temporal_aggregation_form': temporal_aggregation_form
        })

    def post(self, request):
        # Gestione dei form
        if 'monthly_snapshot_submit' in request.POST:
            form = ReportPeriodForm(request.POST)
            if form.is_valid():
                year = form.cleaned_data['year']
                month = form.cleaned_data['month']
                # Elaborare i dati per il report mensile
                return redirect(reverse('goldBI:monthly_snapshot', args=[year, month]))
        
        elif 'quality_control_submit' in request.POST:
            form = ReportPeriodForm(request.POST)
            if form.is_valid():
                year = form.cleaned_data['year']
                month = form.cleaned_data['month']
                # Elaborare i dati per il report di controllo qualità
                return redirect(reverse('goldBI:quality_control', args=[year, month]))
        
        elif 'temporal_aggregation_submit' in request.POST:
            form = TemporalAggregationForm(request.POST)
            if form.is_valid():
                aggregation_type = form.cleaned_data['aggregation_type']
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                # Elaborare i dati per l'aggregazione temporale
                return redirect(reverse('goldBI:temporal_aggregation', args=[aggregation_type, start_date, end_date]))
        
        # Se ci sono errori, renderizza il template con i form
        monthly_snapshot_form = ReportPeriodForm(request.POST)
        quality_control_form = ReportPeriodForm(request.POST)
        temporal_aggregation_form = TemporalAggregationForm(request.POST)
        return render(request, 'gold_bi/report/select_report_type.html', {
            'monthly_snapshot_form': monthly_snapshot_form,
            'quality_control_form': quality_control_form,
            'temporal_aggregation_form': temporal_aggregation_form
        })


class MonthlySnapshotView(LoginRequiredMixin, View):
    def get(self, request, year, month):
        # Calcola i 6 mesi precedenti
        previous_months = get_previous_months(int(year), int(month))
        
        # Inizializziamo le liste per i dati da visualizzare nei grafici
        crm_data = []
        inventory_data = []
        
        # Cicliamo sui mesi precedenti per ottenere i dati dal database
        for y, m in previous_months:
            crm_snapshot = CRMMontlySnapshot.objects.using('gold').filter(year=y, month=m).first()
            inventory_snapshot = InventoryMonthlySnapshot.objects.using('gold').filter(year=y, month=m).first()
            crm_data.append(crm_snapshot)
            inventory_data.append(inventory_snapshot)
        
        # Dati per il mese selezionato
        current_crm_data = CRMMontlySnapshot.objects.using('gold').filter(year=year, month=month).first()
        current_inventory_data = InventoryMonthlySnapshot.objects.using('gold').filter(year=year, month=month).first()
        

        # Prepara i dati per i grafici
        x_labels = [f"{y}-{m:02d}" for y, m in previous_months]

        # Crea i grafici per ciascun campo
        crm_graphs = {
            'total_customers': create_field_graph('Clienti Totali', 
                                                  [data.total_customers for data in crm_data if data],
                                                  x_labels, 'CRM: Clienti totali nel tempo'),
            'total_leads': create_field_graph('Clienti Leads', 
                                              [data.total_leads for data in crm_data if data],
                                              x_labels, 'CRM: Clienti Leads nel tempo'),
            'active_customers': create_field_graph('Clienti Attivi', 
                                                   [data.total_active_customers for data in crm_data if data],
                                                   x_labels, 'CRM: Clienti Attivi nel tempo')
        }

        inventory_graphs = {
            'total_products': create_field_graph('Totale Prodotti', 
                                                [data.total_products for data in inventory_data if data],
                                                x_labels, 'Inventario: Totale Prodotti nel Tempo'),
            'total_stock_value': create_field_graph('Valore Totale del Magazzino', 
                                                    [float(data.total_stock_value) for data in inventory_data if data],
                                                    x_labels, 'Inventario: Valore Totale del Magazzino nel Tempo'),
            'total_stock_quantity': create_field_graph('Quantità Totale del Magazzino', 
                                                    [data.total_stock_quantity for data in inventory_data if data],
                                                    x_labels, 'Inventario: Quantità Totale del Magazzino nel Tempo')
        }

        # Passa i dati al template
        context = {
            'year': year,
            'month': month,
            'crm_graphs': crm_graphs,
            'inventory_graphs': inventory_graphs,
            'current_crm_data': current_crm_data,
            'current_inventory_data': current_inventory_data,
        }

        return render(request, 'gold_bi/report/monthly_snapshot.html', context)


class QualityControlView(LoginRequiredMixin, View):
    def get(self, request, year, month):
        # Recupera i dati dal database 'gold'
        quality_data = InventoryQualityAggregation.objects.using('gold').filter(year=year, month=month).first()

        # Passa i dati al template
        context = {
            'year': year,
            'month': month,
            'quality_data': quality_data,
        }

        return render(request, 'gold_bi/report/quality_control.html', context)


class TemporalAggregationView(LoginRequiredMixin, View):
    def get(self, request, aggregation_type, start_date, end_date):
        # Converti le date in oggetti datetime.date
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Filtra i dati in base al tipo di aggregazione e alle date
        if aggregation_type == 'daily':
            data = InventoryDailyAggregation.objects.using('gold').filter(date__range=[start_date, end_date]).order_by('date')
        elif aggregation_type == 'weekly':
            start_week = start_date.isocalendar()[1]
            start_year = start_date.year
            end_week = end_date.isocalendar()[1]
            end_year = end_date.year
            data = InventoryWeeklyAggregation.objects.using('gold').filter(
                week__range=[start_week, end_week],
                year__range=[start_year, end_year]
            ).order_by('year', 'week')
        elif aggregation_type == 'monthly':
            data = InventoryMonthlyAggregation.objects.using('gold').filter(
                month__range=[start_date.month, end_date.month],
                year__range=[start_date.year, end_date.year]
            ).order_by('year', 'month')
        elif aggregation_type == 'quarterly':
            start_quarter = (start_date.month - 1) // 3 + 1
            end_quarter = (end_date.month - 1) // 3 + 1
            data = InventoryQuarterlyAggregation.objects.using('gold').filter(
                quarter__range=[start_quarter, end_quarter],
                year__range=[start_date.year, end_date.year]
            ).order_by('year', 'quarter')
        elif aggregation_type == 'yearly':
            data = InventoryYearlyAggregation.objects.using('gold').filter(
                year__range=[start_date.year, end_date.year]
            ).order_by('year')
        else:
            data = None

        # Estrai i dati per i grafici
        x_labels = []
        distinct_products = []
        stock_values = []
        sold_units = []
        sales_values = []
        ordered_units = []
        orders_values = []

        if data:
            for item in data:
                if aggregation_type == 'daily':
                    x_labels.append(item.date.strftime("%d-%m-%Y"))
                elif aggregation_type == 'weekly':
                    x_labels.append(f"Week {item.week} {item.year}")
                elif aggregation_type == 'monthly':
                    x_labels.append(f"{item.month}/{item.year}")
                elif aggregation_type == 'quarterly':
                    x_labels.append(f"Q{item.quarter} {item.year}")
                elif aggregation_type == 'yearly':
                    x_labels.append(item.year)
                
                distinct_products.append(item.distinct_products_in_stock)
                stock_values.append(item.total_stock_value)
                sold_units.append(item.total_sold_units)
                sales_values.append(item.total_sales_value)
                ordered_units.append(item.total_ordered_units)
                orders_values.append(item.total_orders_value)

        # Creiamo i grafici per ogni colonna
        graph_titles = [
            'Prodotti Distinti in Magazzino',
            'Valore Totale Magazzino',
            'Unità Vendute Totali',
            'Valore Totale Vendite',
            'Unità Ordinate Totali',
            'Valore Totale Ordini'
        ]

        # Lista di dati per ciascun grafico
        graph_data = [
            distinct_products,
            stock_values,
            sold_units,
            sales_values,
            ordered_units,
            orders_values
        ]

        # Genera i grafici
        graphs = {
            title: create_field_graph(title, data, x_labels, title)
            for title, data in zip(graph_titles, graph_data)
        }
        # Passa i dati al template
        context = {
            'aggregation_type': aggregation_type,
            'start_date': start_date,
            'end_date': end_date,
            'data': data,
            'graphs': graphs
        }

        return render(request, 'gold_bi/report/temporal_aggregation.html', context)