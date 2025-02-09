'''This module contains a context processor so the cart icon 
is shown correctly throughout all pages.
'''
from .cart import Cart

def cart(request):
    '''This function returns the correct cart of the customer in every page of the site.'''
    return {'cart': Cart(request)}