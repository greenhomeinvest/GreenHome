from django.apps import AppConfig
app_name = 'listings' 

class ListingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'listings'
    verbose_name = 'Обяви'
