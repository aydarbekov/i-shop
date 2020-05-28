from django.contrib.auth.mixins import UserPassesTestMixin
from webapp.models import Category, Brand
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render


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
    fields = ['brand_name', 'photo']

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def form_valid(self, form):
        text = form.cleaned_data['brand_name']
        photo = form.cleaned_data['photo']
        if Brand.objects.filter(brand_name=text.capitalize()):
            messages.error(self.request, 'Бренд с таким названием уже существует!')
            return render(self.request, 'base_CRUD/add.html', {})
        else:
            brand = Brand(brand_name=text.capitalize(), photo=photo)
            brand.save()
        return self.get_success_url()

    def get_success_url(self):
        return redirect('webapp:brands_list')


class BrandUpdateView(UserPassesTestMixin, UpdateView):
    model = Brand
    template_name = 'base_CRUD/edit.html'
    fields = ['brand_name', 'photo']
    context_object_name = 'brand'

    def test_func(self):
        user = self.request.user
        return user.is_staff

    # def form_valid(self, form):
    #     brand = form.cleaned_data['brand_name']
    #     if Brand.objects.filter(brand_name=brand):
    #         messages.error(self.request, 'Бренд с таким названием уже существует!')
    #         return render(self.request, 'edit.html', {})
    #     else:
    #         pk = self.kwargs.get('pk')
    #         brand = get_object_or_404(Brand, id=pk)
    #         brand.brand_name = brand
    #         brand.save()
    #     return self.get_success_url()

    def get_success_url(self):
        return reverse('webapp:brands_list')


class BrandDeleteView(UserPassesTestMixin, DeleteView):
    model = Brand
    template_name = 'base_CRUD/delete.html'
    success_url = reverse_lazy('webapp:brands_list')
    permission_required = "webapp.delete_brand"
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        user = self.request.user
        return user.is_staff
