'''This module contains the models needed for the store app.'''
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    '''This class contains the fields that have the user's information we want for their profile.'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=20, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)


    last_cart = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created: bool, **kwargs):
    '''This function is needed to create a user's profile 
    because first we only created a user, now we want to automatically create a profile too.'''
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()

post_save.connect(create_profile, sender = User)

class Category(models.Model):
    '''This class contains the model of the categories of the products.'''
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Customer(models.Model):
    '''This class contains the model of the first-collected customer information
    Before creating a profile.'''
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(models.Model):
    '''This class contains the model of every product in our site.'''
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=500, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')

    def __str__(self):
        return self.name

class Order(models.Model):
    '''This class contains the model of every order made in our site.'''
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank = False)
    phone = models.CharField(max_length=10, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product

class Wishlist(models.Model):
    '''This class contains the model of the customer's wishlist.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
