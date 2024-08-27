# Documentazione per la Strutturazione delle Views e dei Modelli in DjangoForge

Questa documentazione descrive la progettazione e l'implementazione delle views e dei modelli nel contesto delle applicazioni derivate da DjangoForge. L'obiettivo è garantire che il modulo `Gold BI` rimanga completamente indipendente dalle applicazioni specifiche, consentendo al contempo la generazione di report personalizzati in ciascuna app, come `Inventory`.

#### **1. Obiettivi Principali**
- **Indipendenza di Gold BI**: `Gold BI` deve essere modulare e non contenere riferimenti diretti a nessuna applicazione specifica (`Inventory`, `CRM`, `ERP`, ecc.). Questo permette di riutilizzare `Gold BI` in diversi progetti senza doverlo modificare.
- **Modularità delle Applicazioni**: Le singole applicazioni devono essere in grado di gestire autonomamente la logica dei propri report, basandosi sulle informazioni fornite da `Gold BI`.
- **Facilità di Manutenzione**: Le applicazioni possono essere estese o modificate senza impattare `Gold BI`. Le nuove applicazioni o i nuovi tipi di report possono essere aggiunti senza necessità di modificare la logica di `Gold BI`.

### **2. Struttura Generale dei Modelli**

I modelli nel sistema DjangoForge sono organizzati in modo da separare chiaramente la logica di base dell'applicazione dalla logica di aggregazione dei dati. Questo approccio assicura che le applicazioni siano modulari, flessibili e facilmente estensibili.

#### **2.1. Modelli di Base nelle Applicazioni**

Ogni applicazione (come `Inventory`) contiene modelli di base necessari per il funzionamento fondamentale dell'app. Questi modelli definiscono la struttura dei dati principali, come prodotti, ordini, vendite, ecc. Sono situati in un file chiamato `base.py` all'interno della directory `models` dell'applicazione.

**Esempio di Modelli di Base in `Inventory`:**

```python
# inventory/models/base.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

class Product(models.Model):
    name = models.CharField(_("nome"), max_length=100)
    internal_code = models.CharField(_("codice interno"), max_length=50, unique=True, db_index=True)
    category = models.ForeignKey('ProductCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    stock_quantity = models.PositiveIntegerField(_("quantità in stock"), default=0)
    description = models.TextField(_("descrizione"), blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.internal_code})"

    def calculate_average_purchase_price(self):
        total_price = Decimal('0')
        total_quantity = 0
        for order in self.order_transactions.filter(status='paid'):
            total_price += order.unit_price * order.quantity
            total_quantity += order.quantity
        return total_price / total_quantity if total_quantity > 0 else Decimal('0')
    
    # Altri metodi e proprietà...

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_transactions')
    quantity = models.PositiveIntegerField(_("quantità"))
    unit_price = models.DecimalField(_("prezzo unitario"), max_digits=10, decimal_places=2)
    status = models.CharField(_("stato"), max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid')])

    # Altri campi, metodi, e proprietà...
```

#### **2.2. Modelli di Aggregazione Temporale in Gold BI**

`Gold BI` contiene i modelli astratti che definiscono la struttura di base per le aggregazioni temporali (giornaliero, settimanale, mensile, trimestrale, annuale). Questi modelli astratti forniscono i campi comuni necessari per qualsiasi tipo di aggregazione, come `date`, `month`, `year`, ecc. 

**Esempio di Modelli Astratti in `Gold BI`:**

```python
# gold_bi/models.py
from django.db import models

class TemporalAggregationBase(models.Model):
    """
    Modello astratto per tutte le aggregazioni temporali.
    """
    date = models.DateField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

class DailyAggregationBase(TemporalAggregationBase):
    """
    Modello astratto per aggregazioni giornaliere.
    """
    class Meta:
        abstract = True

class WeeklyAggregationBase(TemporalAggregationBase):
    """
    Modello astratto per aggregazioni settimanali.
    """
    week = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

class MonthlyAggregationBase(TemporalAggregationBase):
    """
    Modello astratto per aggregazioni mensili.
    """
    class Meta:
        abstract = True

class QuarterlyAggregationBase(TemporalAggregationBase):
    """
    Modello astratto per aggregazioni trimestrali.
    """
    quarter = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

class YearlyAggregationBase(TemporalAggregationBase):
    """
    Modello astratto per aggregazioni annuali.
    """
    class Meta:
        abstract = True
```

#### **2.3. Estensione dei Modelli di Aggregazione nelle Applicazioni**

Le applicazioni estendono i modelli astratti di `Gold BI` per definire le proprie aggregazioni temporali specifiche. Questi modelli ereditano i campi comuni dai modelli astratti e aggiungono campi specifici necessari per l'applicazione.

**Esempio di Estensione dei Modelli di Aggregazione in `Inventory`:**

```python
# inventory/models/aggregated.py
from django.db import models
from gold_bi.models import DailyAggregationBase, WeeklyAggregationBase, MonthlyAggregationBase, QuarterlyAggregationBase, YearlyAggregationBase

class InventoryDailyAggregation(DailyAggregationBase):
    distinct_products_in_stock = models.IntegerField(null=True, blank=True)
    total_stock_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_sold_units = models.IntegerField(null=True, blank=True)
    total_sales_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Altri campi specifici per l'aggregazione giornaliera...

    class Meta:
        verbose_name = "Inventory Daily Aggregation"
        verbose_name_plural = "Inventory Daily Aggregations"

class InventoryWeeklyAggregation(WeeklyAggregationBase):
    distinct_products_in_stock = models.IntegerField(null=True, blank=True)
    total_stock_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_sold_units = models.IntegerField(null=True, blank=True)
    total_sales_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Altri campi specifici per l'aggregazione settimanale...

    class Meta:
        verbose_name = "Inventory Weekly Aggregation"
        verbose_name_plural = "Inventory Weekly Aggregations"

# Esempi simili per Monthly, Quarterly, e Yearly...
```

### **3. Task di Aggregazione**

Ogni applicazione definisce i propri task di aggregazione che eseguono le operazioni di calcolo sui modelli di base e memorizzano i risultati nei modelli di aggregazione. Questi task possono essere schedulati per essere eseguiti periodicamente.

**Esempio di Task di Aggregazione Giornaliera in `Inventory`:**

```python
# inventory/tasks/aggregate_inventory_daily.py
import logging
from django.utils import timezone
from django.db.models import Sum, F
from django.db import transaction
from ..models.aggregated import InventoryDailyAggregation
from inventory.models.base import Product, Sale, Order

logger = logging.getLogger('app')

def aggregate_inventory_daily():
    try:
        date = timezone.now().date()
        distinct_products_in_stock = Product.objects.filter(stock_quantity__gt=0).count()
        total_stock_value = Product.objects.aggregate(total_value=Sum(F('stock_quantity') * F('unit_price')))['total_value'] or 0
        total_sold_units = Sale.objects.filter(sale_date=date).aggregate(total_units=Sum('quantity'))['total_units'] or 0
        total_sales_value = Sale.objects.filter(sale_date=date).aggregate(total_sales=Sum(F('quantity') * F('unit_price')))['total_sales'] or 0

        # Creazione del record di aggregazione giornaliera
        with transaction.atomic():
            InventoryDailyAggregation.objects.update_or_create(
                date=date,
                defaults={
                    'distinct_products_in_stock': distinct_products_in_stock,
                    'total_stock_value': total_stock_value,
                    'total_sold_units': total_sold_units,
                    'total_sales_value': total_sales_value,
                }
            )

        logger.info(f'Inventory daily aggregation for {date} completed successfully.')

    except Exception as e:
        logger.error(f'Error

 in inventory daily aggregation for {date}: {e}')
```

### **4. Struttura Generale delle Views**

Le views sono strutturate in modo tale da separare la logica di `Backoffice` dalla logica specifica delle applicazioni. `Backoffice` gestisce la selezione del tipo di report tramite un form generico, mentre le applicazioni gestiscono la visualizzazione dei report specifici.

#### **4.1. Views di Backoffice**

Le views in `Gold BI` permettono all'utente di selezionare il tipo di report (es. giornaliero, settimanale, ecc.) e redirigono l'utente alla view appropriata dell'applicazione selezionata.

**Esempio di Implementazione:**

```python
# gold_bi/views.py
from django.shortcuts import render, redirect
from .forms import ReportTypeForm

def select_report_type(request):
    """
    View per selezionare il tipo di report.
    """
    if request.method == 'POST':
        form = ReportTypeForm(request.POST)
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            return redirect(f"{request.path}report/{report_type}/")
    else:
        form = ReportTypeForm()

    return render(request, 'gold_bi/select_report_type.html', {'form': form})
```

#### **4.2. Views nelle Applicazioni**

Le views nelle applicazioni gestiscono la logica specifica per visualizzare i report, basandosi sul tipo di aggregazione selezionato.

**Esempio di Implementazione in `Inventory`:**

```python
# inventory/views.py
from django.shortcuts import render
from .models.aggregated import InventoryDailyAggregation, InventoryWeeklyAggregation

def view_inventory_report(request, report_type):
    model_map = {
        'daily': InventoryDailyAggregation,
        'weekly': InventoryWeeklyAggregation,
        # Altri modelli per monthly, quarterly, yearly...
    }
    
    model = model_map.get(report_type)
    aggregations = model.objects.all().order_by('-date') if model else []

    context = {
        'report_type': report_type,
        'aggregations': aggregations,
    }
    return render(request, 'inventory/reports/view_inventory_report.html', context)
```

### **5. Vantaggi dell'Architettura Proposta**

- **Indipendenza di Gold BI**: `Gold BI` non dipende da alcuna applicazione specifica, rendendolo riutilizzabile e modulare.
- **Modularità delle Applicazioni**: Ogni applicazione gestisce autonomamente la logica dei propri report e aggregazioni temporali, riducendo la complessità e migliorando la manutenibilità.
- **Facilità di Estensione**: Aggiungere nuove applicazioni o nuovi tipi di report non richiede modifiche a `Gold BI`, garantendo che il sistema sia facilmente estensibile.

### **6. Conclusioni**

Questa architettura fornisce un framework flessibile e scalabile per la gestione delle aggregazioni temporali e la generazione di report nelle applicazioni DjangoForge. Le singole applicazioni possono essere sviluppate e mantenute indipendentemente, mentre `Gold BI` fornisce un'infrastruttura generica per la selezione e la gestione dei report. Questo approccio assicura una facile estendibilità, modularità e manutenzione a lungo termine del sistema.