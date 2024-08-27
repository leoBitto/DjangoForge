# gold_bi/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

# Aggregazioni Temporali Generiche
class TemporalAggregationBase(models.Model):
    """
    Modello astratto che definisce i campi di base per tutte le aggregazioni temporali.
    """
    date = models.DateField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-date']

class DailyAggregationBase(TemporalAggregationBase):
    """
    Modello astratto per aggregazioni giornaliere.
    """
    class Meta:
        abstract = True
        verbose_name = _("Daily Aggregation")
        verbose_name_plural = _("Daily Aggregations")

class WeeklyAggregationBase(TemporalAggregationBase):
    """
    Modello astratto per aggregazioni settimanali.
    """
    week = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = _("Weekly Aggregation")
        verbose_name_plural = _("Weekly Aggregations")

class MonthlyAggregationBase(TemporalAggregationBase):
    """
    Modello astratto per aggregazioni mensili.
    """
    class Meta:
        abstract = True
        verbose_name = _("Monthly Aggregation")
        verbose_name_plural = _("Monthly Aggregations")

class QuarterlyAggregationBase(TemporalAggregationBase):
    """
    Modello astratto per aggregazioni trimestrali.
    """
    quarter = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = _("Quarterly Aggregation")
        verbose_name_plural = _("Quarterly Aggregations")

class YearlyAggregationBase(TemporalAggregationBase):
    """
    Modello astratto per aggregazioni annuali.
    """
    class Meta:
        abstract = True
        verbose_name = _("Yearly Aggregation")
        verbose_name_plural = _("Yearly Aggregations")
