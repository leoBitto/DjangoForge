# gold_bi/signals.py

#Questo segnale utilizza post_migrate, che viene emesso dopo che le migrazioni sono state applicate. 
#Questo garantisce che tutte le tabelle del database siano presenti prima di tentare di eseguire i compiti.

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .tasks_scheduler import schedule_tasks

@receiver(post_migrate)
def schedule_tasks_handler(sender, **kwargs):
    schedule_tasks()
