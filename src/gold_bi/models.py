# gold_bi/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class DailyAggregationBase(models.Model):
    """
    Modello astratto per aggregazioni giornaliere.
    """
    date = models.DateField(null=True, blank=True)
    class Meta:
        abstract = True
        verbose_name = _("Daily Aggregation")
        verbose_name_plural = _("Daily Aggregations")
        ordering = ['-date']

class WeeklyAggregationBase(models.Model):
    """
    Modello astratto per aggregazioni settimanali.
    """
    week = models.IntegerField(null=True, blank=True, validators=[
                    MinValueValidator(1),
                    MaxValueValidator(52)])
    year = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = _("Weekly Aggregation")
        verbose_name_plural = _("Weekly Aggregations")
        ordering = ['-year', '-week']

class MonthlyAggregationBase(models.Model):
    """
    Modello astratto per aggregazioni mensili.
    """
    MONTH_CHOICES = [
        (1, _("January")),
        (2, _("February")),
        (3, _("March")),
        (4, _("April")),
        (5, _("May")),
        (6, _("June")),
        (7, _("July")),
        (8, _("August")),
        (9, _("September")),
        (10, _("October")),
        (11, _("November")),
        (12, _("December")),
    ]
    month = models.IntegerField(choices=MONTH_CHOICES, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    class Meta:
        abstract = True
        verbose_name = _("Monthly Aggregation")
        verbose_name_plural = _("Monthly Aggregations")
        ordering = ['-year', '-month']
class QuarterlyAggregationBase(models.Model):
    """
    Modello astratto per aggregazioni trimestrali.
    """
    QUARTER_CHOICES = [
        (1, _("Q1")),
        (2, _("Q2")),
        (3, _("Q3")),
        (4, _("Q4")),
    ]
    quarter = models.IntegerField(choices=QUARTER_CHOICES, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    class Meta:
        abstract = True
        verbose_name = _("Quarterly Aggregation")
        verbose_name_plural = _("Quarterly Aggregations")
        ordering = ['-year', '-quarter']
class YearlyAggregationBase(models.Model):
    """
    Modello astratto per aggregazioni annuali.
    """
    year = models.IntegerField(null=True, blank=True)
    class Meta:
        abstract = True
        verbose_name = _("Yearly Aggregation")
        verbose_name_plural = _("Yearly Aggregations")
        ordering = ['-year']