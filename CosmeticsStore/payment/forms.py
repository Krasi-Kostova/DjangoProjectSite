'''This module contains the forms we use for the payment app.'''
from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    '''This class contains the Shipping Form.'''
    shipping_full_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}),
        required=True)
    shipping_email = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}),
        required=True)
    shipping_address1 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}),
        required=True)
    shipping_address2 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}),
        required=False)
    shipping_city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}),
        required=True)
    shipping_zipcode = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}),
        required=False)
    shipping_country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}),
        required=True)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email',
                'shipping_address1', 'shipping_address2',
                'shipping_city', 'shipping_zipcode', 'shipping_country']

        exclude = ['user',]


class PaymentForm(forms.Form):
    '''This class contains the Payment Form.'''
    card_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name On Card'}),
        required=True)
    card_number = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}),
        required=True)
    card_exp_date = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Expiration Date'}),
        required=True)
    card_cvv = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV Code'}),
        required=True)
