from django.shortcuts import render, redirect

from decimal import Decimal
from products.models import Product
from carts.models import Cart
from orders.models import Order

def cart_home(request):
    cart_obj, created = Cart.objects.new_or_get(request)
    if created or cart_obj.products.count() == 0:
        order_obj = None
    else:
        order_obj, new_obj = Order.objects.get_or_create(cart=cart_obj)
    return render(request=request, template_name='cart/home.html', context={'cart': cart_obj,
                                                                            'object': order_obj,
                                                                            'tax': Decimal(cart_obj.total) - Decimal(cart_obj.subtotal)})


def cart_update(request):
    product_id = request.POST.get('product_id')

    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("carts:home")

        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
        return redirect(product_obj.get_absolute_url())


def checkout_home(request):
    cart_obj, created = Cart.objects.new_or_get(request)
    if created or cart_obj.products.count() == 0:
        return redirect('carts:home')
    else:
        order_obj, new_obj = Order.objects.get_or_create(cart=cart_obj)
    return render(request=request, template_name='cart/checkout.html', context={'order': order_obj})