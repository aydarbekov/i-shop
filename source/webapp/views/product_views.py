from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import ProductForm, ImageFormset
from webapp.models import Product, Category, Image, Carousel


class IndexView(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.all()
        context['carouseles'] = Carousel.objects.all()
        return context

class ProductView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'products/product_add.html'
    fields = ('name', 'category', 'price','in_stock', 'description', 'color', 'discount', 'quantity', 'brand')
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.add_product'
    permission_denied_message = '403 Доступ запрещён!'


    def get_context_data(self, **kwargs):
        if 'formset' not in kwargs:
            kwargs['formset'] = ImageFormset()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        print('post')
        self.object = None
        form = self.get_form()
        formset = ImageFormset(self.request.POST,self.request.FILES)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'base_CRUD/edit.html'
    fields = ('name', 'category', 'price','in_stock', 'description', 'color', 'discount', 'quantity', 'brand')
    context_object_name = 'product'
    permission_required = 'webapp.change_product'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'product'
    permission_required = 'webapp.delete_product'

    def delete(self, request, *args, **kwargs):
        product = self.object = self.get_object()
        product.in_stock = False
        product.save()
        return HttpResponseRedirect(self.get_success_url())

# class ProductDeleteView(PermissionRequiredMixin, View):
#     model = Product
#     # template_name = 'product_delete.html'
#     # success_url = reverse_lazy('webapp:index')
#     context_object_name = 'product'
#     permission_required = 'webapp.delete_product'
#
#     def get(self, request, *args, **kwargs):
#         pk = self.kwargs.get('pk')
#         product = get_object_or_404(Product, id=pk)
#         # product = self.object
#         if product.in_stock == True:
#             product.in_stock = False
#         else:
#             product.in_stock = True
#         product.save()
#         return HttpResponseRedirect('webapp:product_detail', product.pk)


class ProductListView(ListView):
    template_name = 'products/products.html'
    model = Product

    def get_url(self):
        global site
        site = self.request.path
        return site

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        category_pk = self.kwargs.get('pk')
        product_category = Category.objects.get(pk=category_pk)
        context['product_category'] = product_category
        context['products'] = Product.objects.filter(category_id=category_pk)
        self.get_url()
        return context


