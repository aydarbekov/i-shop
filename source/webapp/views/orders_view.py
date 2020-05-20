from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from webapp.models import Order, OrderProduct
from webapp.forms import OrderProductForm, ManualOrderForm


class OrderListView(ListView):
    template_name = 'order/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if self.request.user.has_perm('webapp:view_order'):
            return Order.objects.all().order_by('-created_at')
        return self.request.user.orders.all().order_by('-created_at')


class OrderUpdateView(PermissionRequiredMixin, UpdateView):
    model = Order
    context_object_name = 'order'
    form_class = ManualOrderForm
    template_name = 'order/update.html'
    permission_required = 'webapp.change_product'
    permission_denied_message = '403 Доступ запрещён!'


class OrderDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'order/detail.html'
    permission_required = 'webapp.view_product'
    permission_denied_message = '403 Доступ запрещён!'

    def get_queryset(self):
        if self.request.user.has_perm('webapp:view_order'):
            return Order.objects.all()
        return self.request.user.orders.all()


class OrderProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'webapp.update_orderproduct'
    permission_denied_message = 'Permission denied'
    model = OrderProduct
    template_name = 'order/update_orderproduct.html'
    form_class = OrderProductForm

    def form_valid(self, form):
        self.object = form.save()
        return redirect('webapp:order_detail', self.kwargs.get('pk'))


class OrderProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = OrderProduct
    context_object_name = 'product'
    template_name = 'order/delete_orderproduct.html'
    form_class = OrderProductForm
    permission_required = 'webapp.delete_orderproduct'
    permission_denied_message = 'Permission denied'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('webapp:order_detail', self.kwargs.get('pk'))