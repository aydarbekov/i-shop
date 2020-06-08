from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.models import DeliveryCost


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