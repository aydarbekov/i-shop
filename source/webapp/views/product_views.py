from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.models import Product


class IndexView(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = "products"


class ProductView(DetailView):
    model = Product
    template_name = 'product_detail.html'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'add.html'
    fields = ('name', 'category', 'price', 'photo', 'in_stock')
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.add_product'
    permission_denied_message = '403 Доступ запрещён!'


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'edit.html'
    fields = ('name', 'category', 'price', 'photo', 'in_stock')
    context_object_name = 'product'
    permission_required = 'webapp.change_product'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'product'
    permission_required = 'webapp.delete_product'

    def delete(self, request, *args, **kwargs):
        product = self.object = self.get_object()
        product.in_stock = False
        product.save()
        return HttpResponseRedirect(self.get_success_url())
