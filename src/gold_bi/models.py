from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class DailyAggregationBase(models.Model):
    """
    Modello astratto per aggregazioni giornaliere.
    """
    date = models.DateField(null=True, blank=True, verbose_name=_("Data"))

    class Meta:
        abstract = True
        verbose_name = _("Aggregazione Giornaliera")
        verbose_name_plural = _("Aggregazioni Giornalieri")
        ordering = ['-date']

class WeeklyAggregationBase(models.Model):
    """
    Modello astratto per aggregazioni settimanali.
    """
    week = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(52)
        ],
        verbose_name=_("Settimana")
    )
    year = models.IntegerField(null=True, blank=True, verbose_name=_("Anno"))

    class Meta:
        abstract = True
        verbose_name = _("Aggregazione Settimanale")
        verbose_name_plural = _("Aggregazioni Settimanali")
        ordering = ['-year', '-week']

class MonthlyAggregationBase(models.Model):
    """
    Modello astratto per aggregazioni mensili.
    """
    MONTH_CHOICES = [
        (1, _("Gennaio")),
        (2, _("Febbraio")),
        (3, _("Marzo")),
        (4, _("Aprile")),
        (5, _("Maggio")),
        (6, _("Giugno")),
        (7, _("Luglio")),
        (8, _("Agosto")),
        (9, _("Settembre")),
        (10, _("Ottobre")),
        (11, _("Novembre")),
        (12, _("Dicembre")),
    ]
    month = models.IntegerField(
        choices=MONTH_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Mese")
    )
    year = models.IntegerField(null=True, blank=True, verbose_name=_("Anno"))

    class Meta:
        abstract = True
        verbose_name = _("Aggregazione Mensile")
        verbose_name_plural = _("Aggregazioni Mensili")
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
    quarter = models.IntegerField(
        choices=QUARTER_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Trimestre")
    )
    year = models.IntegerField(null=True, blank=True, verbose_name=_("Anno"))

    class Meta:
        abstract = True
        verbose_name = _("Aggregazione Trimestrale")
        verbose_name_plural = _("Aggregazioni Trimestrali")
        ordering = ['-year', '-quarter']

class YearlyAggregationBase(models.Model):
    """
    Modello astratto per aggregazioni annuali.
    """
    year = models.IntegerField(null=True, blank=True, verbose_name=_("Anno"))

    class Meta:
        abstract = True
        verbose_name = _("Aggregazione Annuale")
        verbose_name_plural = _("Aggregazioni Annuali")
        ordering = ['-year']
