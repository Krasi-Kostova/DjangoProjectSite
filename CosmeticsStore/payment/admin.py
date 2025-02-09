'''This module adds to the admin section of our site
with classes related to payment.'''
from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem


admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInline(admin.StackedInline):
    '''This class creates an Order Item inline.'''
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    '''This class adds to the order in the admin section'''
    model = Order
    readonly_fields = ['date_ordered']
    inlines = [OrderItemInline]


admin.site.unregister(Order)

admin.site.register(Order, OrderAdmin)
