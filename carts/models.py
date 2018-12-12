from django.db import models
from django.contrib.auth.models import User

from decimal import Decimal
from django.core.validators import MinValueValidator

from products.models import Product
from django.db.models.signals import pre_save, m2m_changed


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.get()
            if request.user.is_authenticated and cart_obj.user is None:
                user_cart = self.model.objects.filter(user=request.user).first()
                if user_cart is not None:
                    cart_obj.products.add(*user_cart.products.all())
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products    = models.ManyToManyField(Product, blank=True)
    subtotal    = models.DecimalField(default=0.00, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
    total       = models.DecimalField(default=0.00, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def calculate_subtotal(sender, instance, action, *args, **kwargs):
    if sender and action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(calculate_subtotal, sender=Cart.products.through)


def set_total(sender, instance, *args, **kwargs):
    if sender and instance.subtotal > 0:
        instance.total = Decimal(instance.subtotal) * Decimal(1.18) # 18% tax
    else:
        instance.total = 0.00

pre_save.connect(set_total, sender=Cart)