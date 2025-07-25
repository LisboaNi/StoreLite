# store/views.py
from django.views.generic import TemplateView
from store.models import Store
from product.models import Product
from django.http import Http404

class StoreFrontView(TemplateView):
    template_name = 'public/public.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store_slug = self.kwargs.get('store_name')
        
        try:
            store = Store.objects.get(slug=store_slug)
        except Store.DoesNotExist:
            raise Http404("Loja não encontrada")
        
        products = Product.objects.filter(store=store)
        context['store'] = store
        context['products'] = products
        return context
