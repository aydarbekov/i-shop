from django.contrib.auth.mixins import UserPassesTestMixin
# from webapp.forms import ColorForm
from webapp.forms import ColorForm
from webapp.models import Color
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render


class ColorListView(UserPassesTestMixin, ListView):
    template_name = 'color/colors.html'
    model = Color
    context_object_name = 'colors'
    page_kwarg = 'page'

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class ColorCreateView(UserPassesTestMixin, CreateView):
    model = Color
    template_name = 'color/colorpicker.html'
    form_class = ColorForm

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_success_url(self):
        return reverse('webapp:colors_list')


class ColorUpdateView(UserPassesTestMixin, UpdateView):
    model = Color
    template_name = 'base_CRUD/edit.html'
    form_class = ColorForm
    context_object_name = 'color'

    def get_success_url(self):
        return reverse('webapp:colors_list')

    def test_func(self):
        user = self.request.user
        return user.is_staff


class ColorDeleteView(UserPassesTestMixin, DeleteView):
    model = Color
    template_name = 'base_CRUD/delete.html'
    success_url = reverse_lazy('webapp:colors_list')
    permission_required = "webapp.delete_color"
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        user = self.request.user
        return user.is_staff
