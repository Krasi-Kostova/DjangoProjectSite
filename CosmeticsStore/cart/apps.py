'''This module conatins the Cart Configuration.'''
from django.apps import AppConfig

class CartConfig(AppConfig):
    '''This class defines the cart configuration.'''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
