from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from webapp.models import DeliveryCost, DeliveryAddress


class DeliveryCostList(ListView):
    model = DeliveryCost
    template_name = 'delivery_cost/list.html'
    # context_object_name = 'deliverycost_list'
    ordering = ['-created_at']


class DeliveryCostAdd(UserPassesTestMixin, CreateView):
    model = DeliveryCost
    template_name = 'base_CRUD/add.html'
    fields = ('cost', 'free_from')
    success_url = reverse_lazy('webapp:delivery_cost')

    def test_func(self):
        user = self.request.user
        return user.is_staff


class DeliveryView(TemplateView):
    template_name = 'delivery.html'
    # return render(request, 'delivery.html')


class ReturnView(TemplateView):
    template_name = 'return.html'


class DeliveryAddressAdd(CreateView):
    model = DeliveryAddress
    template_name = 'base_CRUD/add.html'
    fields = ('city', 'street', 'building_number', 'entrance_number', 'flat_number', 'additional_info')
    success_url = reverse_lazy('webapp:check_cart')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

