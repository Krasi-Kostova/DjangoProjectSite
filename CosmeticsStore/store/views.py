'''
This module contains the functions needed when a certain page is opened
or a button is clicked.
'''
import json
from django.db.models import Q

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User

from cart.cart import Cart

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from .models import Product, Category, Profile, Wishlist


def wishlist(request: HttpRequest) -> HttpResponse|None:
    '''This function shows the wishlist of a user.'''
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
        context = {'wishlist':wishlist}
        return render(request, 'wishlist.html', context)

def addtowishlist(request: HttpRequest) -> HttpResponse|None:
    '''This function is triggered when the 'Add to wishlist' button is pressed.
    It checks first if the user is logged in and if the product is already in the list/'''
    if  request.POST.get('action') == 'post':
        if request.user.is_authenticated:
            product_id = request.POST.get('product_id')
            if Product.objects.get(id=product_id):
                if Wishlist.objects.filter(user=request.user, product_id=product_id):
                    messages.success(request, "Product Already In Wishlist")
                    return JsonResponse({'status':"yes"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=product_id)
                    #messages.success(request, "Product Added to Wishlist")
                    return JsonResponse({'status':"Product Added to Wishlist"})
            else:
                messages.success(request, "No Such Product Found")
        else:
            messages.success(request, "You Must Be Logged In To Access This Page!")
    else:
        return JsonResponse({'status':"Product Added to Wishlist"})


def search(request: HttpRequest) -> HttpResponse:
    '''This function is used when the search button is pressed.
    It searches through the products for the ones with a match in the description or the name.
    '''
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(
            Q(name__icontains=searched) | Q(description__icontains = searched)
            )

        if not searched:
            messages.success(request, "That Product Does Not Exist.")
            return render(request, 'search.html', {})

        else:
            return render(request, 'search.html', {'searched':searched})

    else:
        return render(request, 'search.html', {})


def update_info(request: HttpRequest) -> HttpResponse:
    '''This function is used when a user needs to fill in 
    or change their billing or shipping information.'''
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your Info Has Been Updated!")
            return redirect('home')
        return render(request, 'update_info.html', {'form':form, 'shipping_form':shipping_form})

    else:
        messages.success(request, "You Must Be Logged In To Access This Page!")
        return redirect('home')


def update_user(request: HttpRequest) -> HttpResponse:
    '''This function is used when a user wants to change their username or email.'''
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated!")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form})

    else:
        messages.success(request, "You Must Be Logged In To Access This Page!")
        return redirect('home')

def update_password(request: HttpRequest) -> HttpResponse|None:
    '''This function is used when a user wants to change their password.'''
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password Has Been Changed!")
                login(request, current_user)
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})

    else:
        messages.success(request, "You Must Be Logged In To Access This Page!")
        return redirect('home')


def category(request: HttpRequest, category_name: str) -> HttpResponse:
    '''This function is used when a customer wants to look through products by a chosen category.'''
    category_name = category_name.replace('-',' ')
    try:
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("That Category Doesn't Exist."))
        return redirect('home')

def category_summary(request: HttpRequest) -> HttpResponse:
    '''This function lists all categories when in the Category page.'''
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})

def product(request: HttpRequest, pk: int) -> HttpResponse:
    '''This function is used when the 'View Product' button is clicked.
    It takes the customer to the product page.
    '''
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request: HttpRequest) -> HttpResponse:
    '''This function is for the Home page where we want all the products to be listed.'''
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request: HttpRequest) -> HttpResponse:
    '''This function is for the About page.'''
    return render(request, 'about.html', {})

def login_user(request: HttpRequest) -> HttpResponse:
    '''This function is used when a customer wants to log in.
    It checks if the username and password a correct and if there was a saved cart.
    '''
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.last_cart
            if saved_cart:
                dict_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in dict_cart.items():
                    #key is a str
                    cart.add(product=key, quantity=value, db_add = True)

            messages.success(request, ("You Have Been Logged In!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, please try again..."))
            return redirect('login')

    else:
        return render(request, 'login.html', {})

def logout_user(request: HttpRequest) -> HttpResponse:
    '''This function logs out the user from their account.'''
    logout(request)
    messages.success(request, ("You have been logget out! Thanks for stopping by :)"))
    return redirect('home')

def register_user(request: HttpRequest) -> HttpResponse:
    '''This function is used when a user wants to register in the site.
    It checks if the form is filled out correctly.
    '''
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Username Created! Please Fill Out Your User Info"))
            return redirect('update_info')
        else:
            messages.success(request, "Oops! There was a problem. Please try again!")
            return redirect('register')

    else:
        return render(request, 'register.html', {'form':form})
