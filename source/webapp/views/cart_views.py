from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.base import View
from webapp.forms import CartOrderCreateForm, FullSearchForm
from webapp.models import Product, Order, OrderProduct, DeliveryCost, DeliveryAddress
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
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

    # success_url = reverse_lazy('webapp:index')

    def get_context_data(self, **kwargs):
        cart, cart_total = self._prepare_cart()
        # shipping_cost, shipping_message = self._get_shipping_cost()
        kwargs['cart'] = cart
        kwargs['cart_total'] = cart_total
        # kwargs['shipping_cost'] = shipping_cost
        # kwargs['shipping_message'] = shipping_message
        # shipping = self.get_shipping_cost(cart_total)
        # if shipping >= 0:
        #     total = shipping + cart_total
        #     shipping_cost = shipping
        #     # kwargs['total'] = shipping + cart_total
        #     # kwargs['shipping_cost'] = shipping
        # else:
        #     total = cart_total
        #     shipping_cost = 0
        #     # kwargs['total'] = cart_total
        #     # kwargs['shipping_cost'] = 0
        #     kwargs['shipping_message'] = "Стоимость доставки будет уточнена операторатором при подтверждении заказа"
        # kwargs['shipping_cost'] = shipping_cost
        # kwargs['total'] = total
        return super().get_context_data(**kwargs)

    # def get_shipping_cost(self, cart_total):
    #     try:
    #         deliverycost_object = DeliveryCost.objects.latest('created_at')
    #         if cart_total >= deliverycost_object.free_from:
    #             shipping = 0
    #         else:
    #             shipping = deliverycost_object.cost
    #     except:
    #         shipping = -1
    #     return shipping

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs

    # def form_valid(self, form):
    #     if self._cart_empty():
    #         form.add_error(None, 'В корзине отсутствуют товары!')
    #         return self.form_invalid(form)
    #     response = super().form_valid(form)
    #     self._save_order_products()
    #     self._clean_cart()
    #     messages.success(self.request, 'Заказ оформлен!')
    #     return response

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

    # def _get_shipping_cost(self):
    #     shipping_cost = self.request.session.get('shipping_cost', [])
    #     print(shipping_cost)
    #     shipping_message = self.request.session.get('shipping_message', [])
    #     return shipping_cost, shipping_message

    # def _cart_empty(self):
    #     products = self.request.session.get('products', [])
    #     return len(products) == 0
    #
    # def _save_order_products(self):
    #     totals = self._get_totals()
    #     for pk, qty in totals.items():
    #         OrderProduct.objects.create(product_id=pk, order=self.object, amount=qty)
    #
    # def _clean_cart(self):
    #     if 'products' in self.request.session:
    #         self.request.session.pop('products')
    #     if 'products_count' in self.request.session:
    #         self.request.session.pop('products_count')


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


class Check(CreateView):
    model = Order
    form_class = CartOrderCreateForm
    # fields = ['user', 'first_name', 'last_name', 'email', 'phone']
    template_name = "check.html"
    # template_name = 'test.html'
    # template_name = 'base_CRUD/add.html'
    success_url = reverse_lazy('webapp:index')

    # def get_context_data(self, **kwargs):
    #     self.first_name = "Vasys"
    #     kwargs['first_name'] = self.first_name
    #     return super().get_context_data(**kwargs)

    # def get(self, request, *args, **kwargs):
    #     user = self.request.user
    #     print("USER", user)
    #     if user.is_authenticated:
    #         print("user", user)
    #         first_name = user.first_name
    #         last_name = user.last_name
    #         email = user.email
    #         phone = user.profile.mobile_phone
    #         # address = user.address
    #         print("first-name", first_name)
    #         print("last-name", last_name)
    #         print("PHoNE", phone)
    #         print("email", email)
    #         # self.request['first_name'] = first_name
    #     else:
    #         first_name = "NNNNNN"
    #     return render(request, 'check.html', context={'first_name': first_name})
    #
    # def form_valid(self, form):
    #     name = self.kwargs.get('name')
    #     print("NAME", name)

    # def post(self, request, *args, **kwargs):
    #     user = self.request.user
    #     name = self.request.POST.get("first_name", '')
    #     last_name = self.request.POST.get('last_name', '')
    #     email = self.request.POST.get('email', '')
    #     phone = self.request.POST.get('phone', '')
    #     # print(first_name)
    #     print("NAME", name)
    #     delivery = DeliveryCost.objects.latest('created_at')
    #     return redirect('webapp:index')
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = User.objects.filter(pk=self.kwargs['pk'])
    #     groups = StudyGroup.objects.all()
    #     context.update({
    #         'user': user,
    #         'groups': groups,
    #     })
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        basket, basket_total = self._prepare_cart()
        kwargs['basket'] = basket
        kwargs['basket_total'] = basket_total
        user = self.request.user

        if user.is_authenticated:
            print("self.request.user", self.request.user)
            print(self.request.method)
            first_name = user.first_name
            print("user.first_name", user.first_name)
            last_name = user.last_name
            email = user.email
            print('email', email)
            phone = user.profile.mobile_phone
            context.update({'first_name': first_name, 'last_name': last_name, 'email': email, "phone": phone})
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        print("Form", form)
        print("VALID VALID VALID")
        if self._cart_empty(): #проверить _cart_empty
            form.add_error(None, 'В корзине отсутствуют товары!')
            return self.form_invalid(form)
        # shipping_cost = DeliveryCost.objects.latest('created_at')
        # address = DeliveryAddress.objects.first() #изменить адресс на модель у юзера
        # print("Shipping cost", shipping_cost)
        # print("AddRess", address)
        # print(self.get_object())
        # print(dir(self))
        print("SELF>OBJECT", self.object)
        order = Order()
        # order = self.object
        if self.request.user.is_authenticated:
            print("YES")
            order.user = self.request.user
            # order.user = user
            print(self.request.user)
            print(order.user)
        order.first_name = form.cleaned_data['first_name']
        # first_name = user.first_name
        order.last_name = form.cleaned_data['last_name']
        order.email = form.cleaned_data['email']
        order.phone = form.cleaned_data['phone']
        shipping_cost = DeliveryCost.objects.latest('created_at')
        address = DeliveryAddress.objects.first() #изменить адресс на модель у юзера
        print("Shipping cost", shipping_cost)
        print("AddRess", address)
        order.address = address
        order.shipping_cost = shipping_cost

        # order = order(first_name=first_name, last_name=last_name, email=email, phone=phone,
        #               address=address, shipping_cost=shipping_cost)
        # order.shipping_cost = shipping_cost
        order.save()
        # response = super().form_valid(form)
        self._save_order_products(order)
        # order.save()
        # self._clean_cart()
        # response = super().form_valid(form)
        # print("ДОШЛИ ДО СЮДА")
        self.object = order
        print(self.object.address)
        # order.user = request.user
        # order.save()
        messages.success(self.request, 'Заказ оформлен!')
        # return super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print("Form", form)
        print("Form", dir(form))
        print("Form", form.is_valid())

        print("NE RABOTAET")
        return super().form_invalid(form)

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

    def _save_order_products(self, order):
        totals = self._get_totals()
        print("TOTALS", totals)
        # shipping_cost = DeliveryCost.objects.latest('created_at')
        # address = DeliveryAddress.objects.latest('created_at')
        # print("Shipping cost", shipping_cost)
        # print("AddRess", address)
        # order = self.object
        # order.address = address
        # order.shipping_cost = shipping_cost
        # order.save()
        # print("ThIS is ORDER", order)
        for pk, qty in totals.items():
            OrderProduct.objects.create(order=order, product_id=pk, amount=qty)

            # OrderProduct.objects.create(product_id=pk, order=self.object, amount=qty)

    def _cart_empty(self):
        products = self.request.session.get('products', [])
        return len(products) == 0

    def _clean_cart(self):
        if 'products' in self.request.session:
            self.request.session.pop('products')
        if 'products_count' in self.request.session:
            self.request.session.pop('products_count')

    # def form_valid(self, form):
    #     product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
    #     review = Review(
    #         product=product,
    #         grade=self.request.POST.get('example'),
    #         text=form.cleaned_data['text'],
    #         author=self.request.user
    #     )
    #     review.save()
    #     return render(request, 'check.html', context={'order': order})

