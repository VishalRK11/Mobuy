from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Product


class ProductListView(ListView):
    model = Product
    context_object_name = 'products_data'
    template_name = 'products/list.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, **self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context


class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Product, **self.kwargs)
