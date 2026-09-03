from django.apps import AppConfig


class ProductRequestConfig(AppConfig):
    name = 'product_request'

    def ready(self):
        from . import signals
