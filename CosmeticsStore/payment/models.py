'''This module contains the models for the Payment app.'''
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from store.models import Product

class ShippingAddress(models.Model):
    '''This class defines the fields we need for the shipping address.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank = True)
    shipping_full_name = models.CharField(max_length=250)
    shipping_email = models.CharField(max_length=250)
    shipping_address1 = models.CharField(max_length=250)
    shipping_address2 = models.CharField(max_length=250, null=True, blank = True)
    shipping_city = models.CharField(max_length=250)
    shipping_zipcode = models.CharField(max_length=250)
    shipping_country = models.CharField(max_length=250)


    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self) -> str:
        return f'Shipping Address - {str(self.id)}'

def create_shipping_address(sender, instance, created: bool, **kwargs):
    '''This function automatically creates a ShippingAddress object 
    when an account is created.'''
    if created:
        user_shipping = ShippingAddress(user = instance)
        user_shipping.save()


post_save.connect(create_shipping_address, sender = User)


class Order(models.Model):
    '''This class defines what the order consists of.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank = True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=2000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f'Order - {str(self.id)}'

@receiver(pre_save, sender = Order)
def set_shipped_date(sender, instance, **kwargs):
    '''This function sets the shipped date of an order
    automatically after being shipped.'''
    if instance.pk:
        now = datetime.datetime.now()
        object1 = sender._default_manager.get(pk=instance.pk) # object is protected
        if instance.shipped and not object1.shipped:
            instance.date_shipped = now


class OrderItem(models.Model):
    '''This class defines what an order item consists of.'''
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank = True)

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self) -> str:
        return f'Order Item - {str(self.id)}'
