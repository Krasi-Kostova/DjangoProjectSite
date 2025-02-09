'''This module contains the class defining our cart.'''
from store.models import Product, Profile

class Cart():
    '''This class defines the cart of the store
    and the possible functions within it.'''

    def __init__(self, request) -> None:
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product: Product|str, quantity: int, db_add = False) -> None:
        '''This function is used to add a product in the cart.
        It checks first if the product isn't already inside.
        '''
        if db_add:
            # product here is a string
            product_id = product
        else:
            product_id = str(product.id)
        product_qty = str(quantity)

        if product_id not in self.cart:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            str_cart = str(self.cart)
            str_cart = str_cart.replace("\'","\"")
            current_user.update(last_cart=str_cart)


    def __len__(self) -> int:
        return len(self.cart)

    def get_products(self) -> object:
        '''This function lists the products in the cart.'''
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quantities(self)-> dict:
        '''This function returns the cart as a dictionary
        from which we can access the quantities of products.'''
        return self.cart

    def delete(self, product: Product)-> None:
        '''This function removes an element from the cart.'''
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            str_cart = str(self.cart) #'{'3':1}'
            str_cart = str_cart.replace("\'","\"")
            current_user.update(last_cart=str_cart)

    def update(self, product: Product, quantity: int)-> dict:
        '''This function updates the cart 
        after quantities of productss are changed'''
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            str_cart = str(self.cart)
            str_cart = str_cart.replace("\'","\"")
            current_user.update(last_cart=str_cart)

        return self.cart

    def cart_total(self)-> int:
        '''This function calculates the final price of all the products in the cart.'''
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart

        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    total = total + (product.price * value)

        return total
