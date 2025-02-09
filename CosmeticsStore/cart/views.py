'''
This module contains the functions needed when
a certain button from the cart page is clicked.
'''
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpRequest, HttpResponse

from store.models import Product
from .cart import Cart


def cart_summary(request: HttpRequest) -> HttpResponse:
    '''This function is used when we click on the cart button
    and it shows everything in the cart.'''
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities
    totals = cart.cart_total()
    return render(request, 'cart_summary.html',
                  {"cart_products":cart_products, "quantities":quantities, "totals":totals})

def cart_add(request: HttpRequest) -> HttpResponse|None:
    '''This function is used when we add products in the cart.'''
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id = product_id)
        cart.add(product=product, quantity=product_qty)

        cart_quantity = cart.__len__()

        response = JsonResponse({'quantity: ': cart_quantity})
        messages.success(request, ("Product Added To Cart Successfully!"))
        return response


def cart_delete(request: HttpRequest) -> HttpResponse|None:
    '''This function is used when we delete products from the cart.'''
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product':product_id})
        messages.success(request, ("Product Has Been Removed From Cart!"))

        return response

def cart_update(request: HttpRequest) -> HttpResponse|None:
    '''This function is used to update the cart
    after changing quantity of a product.'''
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'quantity':product_qty})
        messages.success(request, ("Your Cart Has Been Updated!"))

        return response
