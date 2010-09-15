from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name=_('creation date'),
                                        auto_now_add=True)
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)

    def get_total(self):
        return sum([price*qty for price,qty in self.item_set.values_list(
            'unit_price', 'quantity')]) or 0

    def get_total_net(self):
        return sum([price*qty for price,qty in self.item_set.values_list(
            'net_price', 'quantity')]) or 0

class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)

class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, 
                                     verbose_name=_('unit price'))
    net_price = models.DecimalField(max_digits=18, decimal_places=2, 
                null=True, blank=True, verbose_name=_('net price'))
    # product as generic relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    objects = ItemManager()

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('cart',)

    def __unicode__(self):
        return 'Item in cart: ' + unicode(self.cart)

    def total_price(self):
        return self.quantity * self.unit_price
    total_price = property(total_price)

    def total_price_net(self):
        return self.quantity * self.net_price
    total_price_net = property(total_price_net)

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    product = property(get_product, set_product)

