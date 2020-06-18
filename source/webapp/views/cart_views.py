from django.contrib.auth.models import User
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        basket, basket_total = self._prepare_cart()
        kwargs['basket'] = basket
        kwargs['basket_total'] = basket_total
        user = self.request.user

        if user.is_authenticated:
            first_name = user.first_name
            last_name = user.last_name
            email = user.email
            phone = user.profile.mobile_phone
            addresses = user.address.all()
            context.update({'user': user, 'first_name': first_name, 'last_name': last_name, 'email': email, "phone": phone, "addresses": addresses})
            if user.profile.company_name:
                company_name = user.profile.company_name
                context.update({"company_name": company_name})
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
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
            user = self.request.user
            order.user = user
            # order.user = user
            print(self.request.user)
            print(order.user)
            address = self.request.POST.get('address', '')
            split_address = address.split('/')
            address = DeliveryAddress.objects.get(user=user, street=split_address[1], building_number=split_address[2])
            print("ADDRESS", type(address))
            # order.address = address_2
            # print("address_2", address_2)
            # print("ADDRESS", user.profile.delivery_address)
        else:
            # city = form.cleaned_data['city']
            # print("CITY", city)
            # street = form.cleaned_data['street']
            # building_number = form.cleaned_data['building_number']
            # entrance_number = form.cleaned_data['entrance_number']
            # flat_number = form.cleaned_data['flat_number']
            # additional_info = form.cleaned_data['additional_info']
            city = self.request.POST.get('city', "Бишкек")
            street = self.request.POST.get('street', None)
            building_number = self.request.POST.get('building_number', None)
            entrance_number = self.request.POST.get('entrance_number', None)
            flat_number = self.request.POST.get('flat_number', None)
            additional_info = self.request.POST.get('additional_info', None)
            address = DeliveryAddress.objects.create(city=city, street=street, building_number=building_number,
                                                     entrance_number=entrance_number, flat_number=flat_number,
                                                     additional_info=additional_info)

        first_name = form.cleaned_data['first_name']
        order.first_name = first_name
        last_name = form.cleaned_data['last_name']
        order.last_name = last_name
        email = form.cleaned_data['email']
        order.email = email
        phone = form.cleaned_data['phone']
        order.phone = phone
        shipping_cost = DeliveryCost.objects.latest('created_at')
        # if self.request.user.is_anonymous:
        #     city = form.cleaned_data['city']
        #     street = form.cleaned_data['street']
        #     building_number = form.cleaned_data['building_number']
        #     entrance_number = form.cleaned_data['entrance_number']
        #     flat_number = form.cleaned_data['flat_number']
        #     additional_info = form.cleaned_data['additional_info']
        #     address = DeliveryAddress.objects.first()

        # address = DeliveryAddress.objects.first() #изменить адресс на модель у юзера
        # address = form.cleaned_data.get('address')
        # address = form.cleaned_data['address']
        # address = self.request.POST.get('address', '')
        # splited_addr = address.split('/')
        # address_2 = DeliveryAddress.objects.get(user=self.request.user, street=splited_addr[1], building_number=splited_addr[2])
        # print("ADDRESS", address)
        # print("address_2", address_2)
        # print("AddRess", address)
        order.address = address
        order.shipping_cost = shipping_cost
        order.save()

        create_account = self.request.POST.get('create_account')
        print("create_account".upper(), create_account)
        if create_account == "on":
            user = User(username=email, first_name=first_name, last_name=last_name, email=email)
        self._save_order_products(order)
        self.object = order
        print(self.object.address)
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
        for pk, qty in totals.items():
            OrderProduct.objects.create(order=order, product_id=pk, amount=qty)

    def _cart_empty(self):
        products = self.request.session.get('products', [])
        return len(products) == 0

    def _clean_cart(self):
        if 'products' in self.request.session:
            self.request.session.pop('products')
        if 'products_count' in self.request.session:
            self.request.session.pop('products_count')
