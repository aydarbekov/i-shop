from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, JsonResponse
from django.views import View
import json

from webapp.models import ProductInCategory, Product
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render



class ProductInCategoryListView(UserPassesTestMixin, ListView):
    template_name = 'product_in_category.html'
    model = ProductInCategory
    context_object_name = 'product'
    page_kwarg = 'page'

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class ProductInCategoryCreateView(UserPassesTestMixin, CreateView):
    model = ProductInCategory
    template_name = 'base_CRUD/add.html'
    fields = ['product']

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def form_valid(self, form):
        product = form.cleaned_data['product']
        if ProductInCategory.objects.filter(product=product):
            messages.error(self.request, 'Объект уже существует!')
            return render(self.request, 'base_CRUD/add.html', {})
        else:
            product_in_category = ProductInCategory(product=product)
            product_in_category.save()
        return self.get_success_url()

    def get_success_url(self):
        return redirect('webapp:product_in_category_list')


class ProductInCategoryUpdateView(UserPassesTestMixin, UpdateView):
    model = ProductInCategory
    template_name = 'base_CRUD/edit.html'
    fields = ['product']
    context_object_name = 'product'

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_success_url(self):
        return reverse('webapp:product_in_category_change')


class ProductInCategoryDeleteView(UserPassesTestMixin, DeleteView):
    model = ProductInCategory
    template_name = 'base_CRUD/delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('webapp:product_in_category_list')
    permission_required = "webapp.delete_category"
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        user = self.request.user
        return user.is_staff


# class CarouselAddView(View):
#
#     def post(self, *args, **kwargs):
#         product = get_object_or_404(Product, pk=kwargs['pk'])
#         if product.carousel_product.filter(product=product).exists():
#             carousel = Carousel.objects.get(product=product)
#             carousel.delete()
#         else:
#             Carousel.objects.get_or_create(product=product)
#         return redirect('webapp:products_all')


def product_in_categorydeleteitem(request):
    product = get_object_or_404(Product, pk=request.POST.get('pk'))
    carousel = get_object_or_404(ProductInCategory, product=product)
    carousel.delete()
    return JsonResponse({'pk': product.pk})


def product_in_categoryadditem(request):
    product = get_object_or_404(Product, pk=request.POST.get('pk'))
    ProductInCategory.objects.get_or_create(product=product)
    return JsonResponse({'pk': product.pk})
