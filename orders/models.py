from django.db import models
from carts.models import Cart

from math import fsum
from decimal import Decimal
from django.core.validators import MinValueValidator

from MoBuy.utils import order_id_generator
from django.db.models.signals import pre_save, post_save

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('cancelled', 'Cancelled'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)

class Order(models.Model):
    order_id        = models.CharField(max_length=120, blank=True, unique=True)
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status          = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total  = models.DecimalField(default=0.00, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
    total           = models.DecimalField(default=0.00, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

    def update_total(self):
        total = format(fsum([self.cart.total, self.shipping_total]), '.2f')
        self.total = total
        self.save()
        return total

def set_order_id(sender, instance, *args, **kwargs):
    if sender and not instance.order_id:
        instance.order_id = order_id_generator(instance)

pre_save.connect(set_order_id, sender=Order)

def get_updated_cart_total(sender, instance, created, *args, **kwargs):
    if sender and not created:
        qs = Order.objects.filter(cart__id=instance.id)
        if qs.count() == 1:
            order_obj = qs.get()
            order_obj.update_total()

post_save.connect(get_updated_cart_total, sender=Cart)

def set_order_total(sender, instance, created, *args, **kwargs):
    if sender and created:
        instance.update_total()

post_save.connect(set_order_total, sender=Order)