from django.contrib.auth.mixins import UserPassesTestMixin
from webapp.models import SubCategory, Category
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render


class SubCategoryCreateView(UserPassesTestMixin, CreateView):
    model = SubCategory
    template_name = 'base_CRUD/add.html'
    fields = ['sub_name']


    def form_valid(self, form):
        subname = form.cleaned_data['sub_name']
        category_pk=self.kwargs.get('pk')
        category = get_object_or_404(Category, pk=category_pk)
        if category.subcategories.filter(sub_name=subname):
            messages.error(self.request, 'Подраздел с таким названием уже существует!')
            return render(self.request, 'base_CRUD/add.html', {})
        else:
            category.subcategories.create(sub_name=subname)
        return self.get_success_url()

    def get_success_url(self):
        return redirect('webapp:categories_list')

    def test_func(self):
        user = self.request.user
        return user.is_staff


class SubCategoryUpdateView(UserPassesTestMixin, UpdateView):
    model = SubCategory
    template_name = 'base_CRUD/edit.html'
    fields = ['category','sub_name']


    def form_valid(self, form):
        subname = form.cleaned_data['sub_name']
        category = form.cleaned_data['category']
        if SubCategory.objects.filter(category=category, sub_name=subname):
            messages.error(self.request, 'Подраздел с таким названием уже существует!')
            return render(self.request, 'base_CRUD/edit.html', {})
        else:
            pk = self.kwargs.get('pk')
            subcategory = get_object_or_404(SubCategory, id=pk)
            subcategory.sub_name = subname
            subcategory.category = category
            subcategory.save()
        return self.get_success_url()

    def get_success_url(self):
        return redirect('webapp:categories_list')

    def test_func(self):
        user = self.request.user
        return user.is_staff


class SubCategoryDeleteView(UserPassesTestMixin, DeleteView):
    model = SubCategory
    template_name = 'base_CRUD/delete.html'
    success_url = reverse_lazy('webapp:categories_list')
    permission_required = "webapp.delete_subcategory"
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        user = self.request.user
        return user.is_staff
