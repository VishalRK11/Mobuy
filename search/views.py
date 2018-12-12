from django.views.generic import ListView
from products.models import Product

class SearchProductListView(ListView):
    template_name = 'search/view.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context_data = super(SearchProductListView, self).get_context_data(*args, **kwargs)
        context_data['query'] = self.request.GET.get('q')
        return context_data

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.search(query)
        return Product.objects.featured()
