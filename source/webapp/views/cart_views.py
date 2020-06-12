from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.base import View
from webapp.forms import CartOrderCreateForm, FullSearchForm
from webapp.models import Product, Order, OrderProduct, DeliveryCost
from django.contrib import messages
from django.http import JsonResponse
from webapp.views.product_views import SearchView


# class CartChangeView(SearchView):
#     def get(self, request, *args, **kwargs):
#         products = request.session.get('products', [])
#         pk = request.GET.get('pk')
#         action = request.GET.get('action')
#         next_url = request.GET.get('next', reverse('webapp:index'))
#
#         if action == 'add':
#             product = get_object_or_404(Product, pk=pk)
#             # if product.quantity > 0:
#             products.append(pk)
#         elif action == 'delete':
#             new_products = []
#             for product_pk in products:
#                 if product_pk != pk:
#                     new_products.append(product_pk)
#             products = new_products
#         else:
#             for product_pk in products:
#                 if product_pk == pk:
#                     products.remove(product_pk)
#                     break
#
#         request.session['products'] = products
#         request.session['products_count'] = len(products)
#
#         return redirect(next_url)


class CartView(SearchView):
    model = Order
    form_class = FullSearchForm
    template_name = 'cart/cart.html'
    success_url = reverse_lazy('webapp:index')

    def get_context_data(self, **kwargs):
        cart, cart_total = self._prepare_cart()
        kwargs['cart'] = cart
        kwargs['cart_total'] = cart_total
        shipping = self.get_shipping_cost(cart_total)
        if shipping >= 0:
            total = shipping + cart_total
            shipping_cost = shipping
            # kwargs['total'] = shipping + cart_total
            # kwargs['shipping_cost'] = shipping
        else:
            total = cart_total
            shipping_cost = 0
            # kwargs['total'] = cart_total
            # kwargs['shipping_cost'] = 0
            kwargs['shipping_message'] = "Стоимость доставки будет уточнена операторатором при подтверждении заказа"
        kwargs['shipping_cost'] = shipping_cost
        kwargs['total'] = total
        return super().get_context_data(**kwargs)

    def get_shipping_cost(self, cart_total):
        try:
            deliverycost_object = DeliveryCost.objects.latest('created_at')
            if cart_total >= deliverycost_object.free_from:
                shipping = 0
            else:
                shipping = deliverycost_object.cost
        except:
            shipping = -1
        return shipping

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs

    def form_valid(self, form):
        if self._cart_empty():
            form.add_error(None, 'В корзине отсутствуют товары!')
            return self.form_invalid(form)
        response = super().form_valid(form)
        self._save_order_products()
        self._clean_cart()
        messages.success(self.request, 'Заказ оформлен!')
        return response

    def _prepare_cart(self):
        totals = self._get_totals()
        cart = []
        cart_total = 0
        for pk, qty in totals.items():
            product = Product.objects.get(pk=int(pk))
            total = product.price * qty
            cart_total += total
            cart.append({'product': product, 'qty': qty, 'total': total})
        return cart, cart_total

    def _get_totals(self):
        products = self.request.session.get('products', [])
        totals = {}
        for product_pk in products:
            if product_pk not in totals:
                totals[product_pk] = 0
            totals[product_pk] += 1
        return totals

    def _cart_empty(self):
        products = self.request.session.get('products', [])
        return len(products) == 0

    def _save_order_products(self):
        totals = self._get_totals()
        for pk, qty in totals.items():
            OrderProduct.objects.create(product_id=pk, order=self.object, amount=qty)

    def _clean_cart(self):
        if 'products' in self.request.session:
            self.request.session.pop('products')
        if 'products_count' in self.request.session:
            self.request.session.pop('products_count')


def cartdeleteitem(request):
    products = request.session.get('products', [])
    pk = request.POST.get('pk')
    for product_pk in products:
        if product_pk == pk:
            products.remove(product_pk)
            break
    request.session['products'] = products
    request.session['products_count'] = len(products)
    return JsonResponse({'pk': products})

def cart_modal_delete(request):
    products = request.session.get('products', [])
    pk = request.POST.get('pk')
    product = get_object_or_404(Product, pk=request.POST.get('pk'))
    while pk in products:
        products.remove(pk)
    request.session['products'] = products
    request.session['products_count'] = len(products)
    return JsonResponse({'pk': product.pk})


def cartadditem(request):
    products = request.session.get('products', [])
    pk = request.POST.get('pk')
    qty = request.POST.get('qty')
    product = get_object_or_404(Product, pk=request.POST.get('pk'))
    if qty:
        for i in range(int(qty)):
            products.append(pk)
    else:
        products.append(pk)
    request.session['products'] = products
    request.session['products_count'] = len(products)
    return JsonResponse({'pk': product.pk})


