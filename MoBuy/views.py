from django.shortcuts import render
from django.views.generic import TemplateView
from carts.models import Cart
from products.models import Product

def home_page(request):
    # if request.user.is_authenticated:
    #     cart_obj, cart_created = Cart.objects.new_or_get(request)
    #     request.session['cart_products'] = cart_obj.products.count()
    return render(request=request, template_name='mobuy/home.html', context=context)


class HomeTemplateView(TemplateView):
    template_name = 'mobuy/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all().order_by('-id')[:4]
        return context


def login_page(request):
    pass


def register_page(request):
    pass
