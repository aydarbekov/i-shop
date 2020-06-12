from django.contrib.auth.mixins import UserPassesTestMixin
from webapp.forms import CategoryForm
from webapp.models import Category
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect


class CategoryListView(UserPassesTestMixin, ListView):
    template_name = 'categories.html'
    model = Category
    context_object_name = 'categories'
    page_kwarg = 'page'

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class CategoryCreateView(UserPassesTestMixin, CreateView):
    model = Category
    template_name = 'base_CRUD/add.html'
    form_class = CategoryForm

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_success_url(self):
        return redirect('webapp:categories_list')


class CategoryUpdateView(UserPassesTestMixin, UpdateView):
    model = Category
    template_name = 'base_CRUD/edit.html'
    fields = ['category_name', 'photo']
    context_object_name = 'category'

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_success_url(self):
        return reverse('webapp:categories_list')


class CategoryDeleteView(UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'base_CRUD/delete.html'
    success_url = reverse_lazy('webapp:categories_list')
    permission_required = "webapp.delete_category"
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        user = self.request.user
        return user.is_staff
