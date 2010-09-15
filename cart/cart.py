import datetime
import models

CART_ID = 'CART-ID'

class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

class Cart:
    def __init__(self, request, prefix=CART_ID):
        self.prefix = prefix
        cart_id = request.session.get(prefix)
        if cart_id:
            try:
                cart = models.Cart.objects.get(id=cart_id, checked_out=False)
            except models.Cart.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def new(self, request):
        cart = models.Cart(creation_date=datetime.datetime.now())
        cart.save()
        request.session[self.prefix] = cart.id
        return cart

    def add(self, product, unit_price, quantity=1, net_price=None):
        try:
            item = models.Item.objects.get(cart=self.cart, product=product,)
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.product = product
            item.unit_price = unit_price
            item.net_price = net_price
            item.quantity = quantity
            item.save()
        else:
            raise ItemAlreadyExists

    def remove(self, item):
        try:
            item = models.Item.objects.get(pk=item.pk)
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, product, unit_price, quantity, net_price=None):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
            item.cart = self.cart
            item.product = product
            item.unit_price = unit_price
            item.net_price = net_price
            item.quantity = quantity
            item.save(force_update = True)
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist

    def clear(self):
        for item in self.cart.item_set.all():
            item.delete()

    # There's all sort of info you might want to easily get from your cart
    
    def getQuantity(self, product):
        try: 
            item = models.Item.objects.get(cart = self.cart, product = product)
            return item.quantity
            
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
    
    def checkout_cart(self):
        self.cart.checked_out = True
        self.cart.save()
        return True
