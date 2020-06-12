from django.contrib.auth.mixins import UserPassesTestMixin
from webapp.forms import BrandForm
from webapp.models import Brand
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect


class BrandListView(UserPassesTestMixin, ListView):
    template_name = 'brands.html'
    model = Brand
    context_object_name = 'brands'
    page_kwarg = 'page'

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class BrandCreateView(UserPassesTestMixin, CreateView):
    model = Brand
    template_name = 'base_CRUD/add.html'
    form_class = BrandForm

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_success_url(self):
        return redirect('webapp:brands_list')


class BrandUpdateView(UserPassesTestMixin, UpdateView):
    model = Brand
    template_name = 'base_CRUD/edit.html'
    fields = ['brand_name', 'photo']
    context_object_name = 'brand'

    def get_success_url(self):
        return reverse('webapp:brands_list')

    def test_func(self):
        user = self.request.user
        return user.is_staff


class BrandDeleteView(UserPassesTestMixin, DeleteView):
    model = Brand
    template_name = 'base_CRUD/delete.html'
    success_url = reverse_lazy('webapp:brands_list')
    permission_required = "webapp.delete_brand"
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        user = self.request.user
        return user.is_staff
