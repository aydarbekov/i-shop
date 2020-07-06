from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework.reverse import reverse

from webapp.forms import SubCategoryForm
from webapp.models import SubCategory, Category
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404


class SubCategoryCreateView(UserPassesTestMixin, CreateView):
    model = SubCategory
    template_name = 'base_CRUD/add.html'
    form_class = SubCategoryForm

    def get_success_url(self):
        return redirect('webapp:categories_list')

    def form_valid(self, form):
        subname = form.cleaned_data['sub_name']
        category_pk = self.kwargs.get('pk')
        category = get_object_or_404(Category, pk=category_pk)
        # if category.subcategories.filter(sub_name=subname):
        #     messages.error(self.request, 'Подраздел с таким названием уже существует!')
        #     return render(self.request, 'base_CRUD/add.html', {})
        # else:
        category.subcategories.create(sub_name=subname)
        return self.get_success_url()

    def test_func(self):
        user = self.request.user
        return user.is_staff


class SubCategoryUpdateView(UserPassesTestMixin, UpdateView):
    model = SubCategory
    template_name = 'base_CRUD/edit.html'
    fields = ['sub_name']

    def get_success_url(self):
        return reverse('webapp:categories_list')

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
