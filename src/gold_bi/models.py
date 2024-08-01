from django.db import models
from django.utils import timezone

class AggregatedErrorLog(models.Model):
    """
    Modello per memorizzare gli errori aggregati.
    """
    hour = models.IntegerField()  # Ora (0-23)
    day = models.CharField(max_length=10)  # Giorno della settimana è un numero memorizzato come stringa
    count = models.IntegerField(default=0, null=True, blank=True)  # Conteggio degli errori

    class Meta:
        verbose_name = "Aggregated Error Log"
        verbose_name_plural = "Aggregated Error Logs"

    def __str__(self):
        return f"Error Log - {self.day} - {self.hour} - Count: {self.count}"


class AggregatedAccessLog(models.Model):
    """
    Modello per memorizzare gli accessi aggregati.
    """
    hour = models.IntegerField()  # Ora (0-23)
    day = models.CharField(max_length=10)  # Giorno della settimana (es. "Monday")
    count = models.IntegerField(default=0, null=True, blank=True)  # Conteggio degli accessi

    class Meta:
        verbose_name = "Aggregated Access Log"
        verbose_name_plural = "Aggregated Access Logs"

    def __str__(self):
        return f"Access Log - {self.day} - {self.hour} - Count: {self.count}"

