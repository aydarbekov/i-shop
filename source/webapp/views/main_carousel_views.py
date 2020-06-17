from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, JsonResponse
from django.views import View
import json

from webapp.models import MainCarousel
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render

from webapp.views.product_views import SearchView


class MainCarouselListView(UserPassesTestMixin, ListView):
    template_name = 'main_carousel.html'
    model = MainCarousel
    context_object_name = 'main_carousel'
    page_kwarg = 'page'

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class MainCarouselCreateView(UserPassesTestMixin, CreateView):
    model = MainCarousel
    template_name = 'base_CRUD/add.html'
    fields = ['title', 'text', 'photo', 'price', 'link']
    success_url = reverse_lazy('webapp:main_carousel_list')

    def test_func(self):
        user = self.request.user
        return user.is_staff

    # def form_valid(self, form):
    #     product = form.cleaned_data['product']
    #     if Carousel.objects.filter(product=product):
    #         messages.error(self.request, 'Объект уже существует!')
    #         return render(self.request, 'base_CRUD/add.html', {})
    #     else:
    #         carousel = Carousel(product=product)
    #         carousel.save()
    #     return self.get_success_url()

    # def get_success_url(self):
    #     return redirect('webapp:main_carousel_list')


class MainCarouselUpdateView(UserPassesTestMixin, UpdateView):
    model = MainCarousel
    template_name = 'base_CRUD/edit.html'
    fields = ['title', 'text', 'photo', 'price', 'link']
    # fields = ['product']
    # context_object_name = 'product'

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_success_url(self):
        return reverse('webapp:main_carousel_list')


class MainCarouselDeleteView(UserPassesTestMixin, DeleteView):
    model = MainCarousel
    template_name = 'base_CRUD/delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('webapp:main_carousel_list')
    permission_required = "webapp.delete_category"
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        user = self.request.user
        return user.is_staff
