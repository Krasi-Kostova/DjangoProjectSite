'''
This is the module with the information that is shown in the admin section of our site.
'''
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category, Customer, Product, Order, Profile


admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)


class ProfileInLine(admin.StackedInline):
    '''The class is needed so we can show all the information of the profiles in the admin page.'''
    model = Profile


class UserAdmin(admin.ModelAdmin):
    '''The class is used for constructing our user information in the admin section.'''
    model = User
    field = ['username','first_name', 'last_name', 'email']
    inlines = [ProfileInLine]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
