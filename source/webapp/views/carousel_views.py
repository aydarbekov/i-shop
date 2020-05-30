from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, JsonResponse
from django.views import View
import json

from webapp.models import Carousel, Product
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render


class CarouselListView(UserPassesTestMixin, ListView):
    template_name = 'carousel.html'
    model = Carousel
    context_object_name = 'carousel'
    page_kwarg = 'page'

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class CarouselCreateView(UserPassesTestMixin, CreateView):
    model = Carousel
    template_name = 'base_CRUD/add.html'
    fields = ['product']

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def form_valid(self, form):
        product = form.cleaned_data['product']
        if Carousel.objects.filter(product=product):
            messages.error(self.request, 'Объект уже существует!')
            return render(self.request, 'base_CRUD/add.html', {})
        else:
            carousel = Carousel(product=product)
            carousel.save()
        return self.get_success_url()

    def get_success_url(self):
        return redirect('webapp:carousel_list')


class CarouselUpdateView(UserPassesTestMixin, UpdateView):
    model = Carousel
    template_name = 'base_CRUD/edit.html'
    fields = ['product']
    context_object_name = 'product'

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_success_url(self):
        return reverse('webapp:carousel_list')


class CarouselDeleteView(UserPassesTestMixin, DeleteView):
    model = Carousel
    template_name = 'base_CRUD/delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('webapp:carousel_list')
    permission_required = "webapp.delete_category"
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        user = self.request.user
        return user.is_staff


class ProductALLListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'
    # paginate_by = 5
    # paginate_orphans = 1


class CarouselAddView(View):

    def post(self, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        if product.carousel_product.filter(product=product).exists():
            carousel = Carousel.objects.get(product=product)
            carousel.delete()
        else:
            Carousel.objects.get_or_create(product=product)
        return redirect('webapp:products_all')


def carouseldeleteitem(request):
    product = get_object_or_404(Product, pk=request.POST.get('pk'))
    carousel = get_object_or_404(Carousel, product=product)
    carousel.delete()
    return JsonResponse({'pk': product.pk})


def carouseladditem(request):
    product = get_object_or_404(Product, pk=request.POST.get('pk'))
    Carousel.objects.get_or_create(product=product)
    return JsonResponse({'pk': product.pk})
