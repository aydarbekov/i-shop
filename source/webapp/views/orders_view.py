from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from webapp.models import Order, OrderProduct, Product
from webapp.forms import OrderProductForm, ManualOrderForm
from django.urls import reverse_lazy


class OrderListView(ListView):
    template_name = 'order/list.html'
    context_object_name = 'orders'


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     context['order_pay_num'] = '{:06}'.format(self.kwargs.get('pk'))
    #     return super().get_context_data(**kwargs)
    #
    # def _prepare_cart(self):
    #     totals = self._get_totals()
    #     cart = []
    #     cart_total = 0
    #     for pk, qty in totals.items():
    #         product = Product.objects.get(pk=int(pk))
    #         total = product.price * qty
    #         cart_total += total
    #         cart.append({'product': product, 'qty': qty, 'total': total})
    #     return cart, cart_total
    #
    # def _get_totals(self):
    #     products = self.request.session.get('products', [])
    #     totals = {}
    #     for product_pk in products:
    #         if product_pk not in totals:
    #             totals[product_pk] = 0
    #         totals[product_pk] += 1
    #     return totals

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
    success_url = reverse_lazy('webapp:orders')


class OrderDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'order/detail.html'
    permission_required = 'webapp.view_product'
    permission_denied_message = '403 Доступ запрещён!'

    def get_queryset(self):
        if self.request.user.has_perm('webapp:view_order'):
            return Order.objects.all()
        return self.request.user.orders.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        summary_price = 0
        for i in self.object.products.all():
            summary_price += i.price
        context['summary_price'] = summary_price
        context['order_pay_num'] = '{:06}'.format(self.kwargs.get('pk'))
        return context


class OrderProductCreateView(CreateView):
    model = OrderProduct
    template_name = 'order/create_orderproduct.html'
    form_class = OrderProductForm

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        order = Order.objects.get(pk=pk)
        print("order", order)
        OrderProduct.objects.create(
            order=order,
            product=form.cleaned_data['product'],
            amount=form.cleaned_data['amount']
        )
        return redirect('webapp:order_detail', self.kwargs.get('pk'))

# PermissionRequiredMixin,
class OrderProductUpdateView(UpdateView):
    # permission_required = 'webapp.update_orderproduct'
    # permission_denied_message = 'Permission denied'
    model = OrderProduct
    template_name = 'order/update_orderproduct.html'
    form_class = OrderProductForm



    def form_valid(self, form):
        self.object = form.save()
        return redirect('webapp:order_detail', self.kwargs.get('id'))


class OrderProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = OrderProduct
    context_object_name = 'object'
    template_name = 'order/delete_orderproduct.html'
    form_class = OrderProductForm
    permission_required = 'webapp.delete_orderproduct'
    permission_denied_message = 'Permission denied'

    def delete(self, request, *args, **kwargs):
        print(self.get_object())
        self.object = self.get_object()
        self.object.delete()
        return redirect('webapp:order_detail', self.kwargs.get('id'))
