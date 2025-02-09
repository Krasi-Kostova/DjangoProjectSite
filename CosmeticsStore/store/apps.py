'''This module contains the apps of the store directory.'''
from django.apps import AppConfig


class StoreConfig(AppConfig):
    '''This class contains the store app.'''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
