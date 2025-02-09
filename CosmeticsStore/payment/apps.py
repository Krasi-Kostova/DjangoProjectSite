'''This module contains the configuration of payment for our site.'''
from django.apps import AppConfig


class PaymentConfig(AppConfig):
    '''Configuration class for the Payment app.'''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
