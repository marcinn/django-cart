from django.http import HttpResponseRedirect
from django.conf import settings
from cart import Cart, ItemAlreadyExists, ItemDoesNotExist
from cart.models import Item

# Create your views here.

# TODO: We should provide some built-in views for common actions such 
# as adding an item to cart (addToCart), removing an item from the 
# cart (removeFromCart), updating the info for an item (updateItem), 
# and I'm sure some other stuff. The problem is that we need a way to 
# allow for users to place an arbitrary item in the cart.