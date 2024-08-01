from django.apps import AppConfig

class GoldBiConfig(AppConfig):
    name = 'gold_bi'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import gold_bi.signals  # Importa i segnali per assicurarne il collegamento
