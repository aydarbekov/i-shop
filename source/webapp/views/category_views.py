from django.contrib.auth.mixins import UserPassesTestMixin
from webapp.models import Category
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render


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
    fields = ['category_name', 'photo']

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def form_valid(self, form):
        category_name = form.cleaned_data['category_name']
        photo = form.cleaned_data['photo']
        if Category.objects.filter(category_name__iexact=category_name):
            messages.error(self.request, 'Категория с таким названием уже существует!')
            return render(self.request, 'base_CRUD/add.html', {})
        else:
            category = Category(category_name=category_name, photo=photo)
            category.save()
        return self.get_success_url()

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

    # def form_valid(self, form):
    #     category = form.cleaned_data['category_name']
    #     if Category.objects.filter(category_name=category):
    #         messages.error(self.request, 'Категория с таким названием уже существует!')
    #         return render(self.request, 'edit.html', {})
    #     else:
    #         pk = self.kwargs.get('pk')
    #         category = get_object_or_404(Category, id=pk)
    #         category.category_name = category
    #         category.save()
    #     return self.get_success_url()

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
