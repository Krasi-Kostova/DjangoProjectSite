'''This module contains the functions needed for the Payment operations.'''
import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest, HttpResponse

from store.models import Profile
from cart.cart import Cart

from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem


def orders(request: HttpRequest, pk:int) -> HttpResponse:
    '''This function shows the admin to see all the orders.'''
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.filter(id=pk)
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            if status == "true":
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order.update(shipped=False)
                messages.success(request, "Shipping Status Updated")
                return redirect('home')

        return render(request, 'payment/orders.html', {"order":order, "items":items})

    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def shipped_dashboard(request: HttpRequest) -> HttpResponse:
    '''This function shows all the shipped orders.'''
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped = True)
        if request.POST:
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)
            messages.success(request, "Shipping Status Updated")
            return redirect('home')
        return render(request, 'payment/shipped_dashboard.html', {'orders':orders})
    else:
        messages.success(request, 'Access Denied!')
        return redirect('home')

def not_shipped_dashboard(request: HttpResponse) -> HttpResponse:
    '''This function shows all the unshipped orders.'''
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped = False)
        if request.POST:
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)
            messages.success(request, "Shipping Status Updated")
            return redirect('home')
        return render(request, 'payment/not_shipped_dashboard.html', {'orders':orders})
    else:
        messages.success(request, 'Access Denied!')
        return redirect('home')

def create_order_items(order, cart_products, quantities, user=None):
    """Helper function for process_order to create order items
    based on cart products and quantities.
    """
    for product in cart_products():
        product_id = product.id
        product_price = product.price
        for key, value in quantities().items():
            if int(key) == product.id:
                OrderItem.objects.create(
                    order=order,
                    product_id=product_id,
                    user=user,
                    quantity=value,
                    price=product_price
                )

def clear_user_cart(user):
    """Helper function for process_order to clear the last cart from the database."""
    current_user = Profile.objects.filter(id=user.id)
    current_user.update(last_cart="")


def clear_session_cart(request):
    """Helper function for process_order to clear the cart from the session."""
    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]

def process_order(request: HttpRequest) -> HttpResponse:
    """This function processes the order, 
    saves the order and its items and clears the cart.
    """
    if not request.POST:
        messages.success(request, "Access denied")
        return redirect('home')

    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities
    totals = cart.cart_total()

    # Get billing info from the last page
    payment_form = PaymentForm(request.POST or None)
    # Get shipping session data
    old_shipping = request.session.get('old_shipping')
    if not old_shipping:
        messages.error(request, "Shipping information is missing!")
        return redirect('home')

    # gather order info - the rest of the stuff from the order model
    full_name = old_shipping['shipping_full_name']
    email = old_shipping['shipping_email']
    # create shipping address from session info
    shipping_address = f"{old_shipping['shipping_address1']}\n{old_shipping['shipping_address2']}\n{old_shipping['shipping_city']}\n{old_shipping['shipping_zipcode']}\n{old_shipping['shipping_country']}"
    amount_paid = totals

    # Determine if the user is logged in
    user = request.user if request.user.is_authenticated else None

    # Create order (whether logged in or not)
    order_data = {
        'full_name': full_name,
        'email': email,
        'shipping_address': shipping_address,
        'amount_paid': amount_paid
    }

    if user:
        # Logged-in user
        order_data['user'] = user
        create_order = Order.objects.create(**order_data)
        # Save cart items (order items)
        create_order_items(create_order, cart_products, quantities, user)
        clear_user_cart(user)
    else:
        # Guest user
        create_order = Order.objects.create(**order_data)
        create_order_items(create_order, cart_products, quantities)

    # Clear session and cart
    clear_session_cart(request)
    messages.success(request, "Order placed successfully!")
    return redirect('home')


def billing_info(request: HttpRequest) -> HttpResponse:
    '''This function shows the Payment form after clicking 'Continue to billing'.'''
    if request.POST:

        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_quantities
        totals = cart.cart_total()

        old_shipping = request.POST
        request.session['old_shipping'] = old_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()

            return render(request, 'payment/billing_info.html',
						  {"cart_products":cart_products, "quantities":quantities,
                           "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})

        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',
						  {"cart_products":cart_products, "quantities":quantities,
                           "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})

    else:
        messages.success(request, 'Access Denied!')
        return redirect('home')

def payment_success(request: HttpRequest)->HttpResponse:
    '''This function handles successfull payment.'''
    return render(request, 'payment/payment_success.html', {})

def checkout(request: HttpRequest)->HttpResponse:
    '''This function handles checkout.'''
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html',
                      {"cart_products":cart_products, "quantities":quantities,
                       "totals":totals, "shipping_form":shipping_form})

    else:
        shipping_form = ShippingForm(request.POST or None)

        return render(request, 'payment/checkout.html', 
                      {"cart_products":cart_products, "quantities":quantities,
                       "totals":totals, "shipping_form":shipping_form})
