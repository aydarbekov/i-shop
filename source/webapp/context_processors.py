from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.views.generic import FormView
from django.utils.http import urlencode
from django.shortcuts import redirect
from django.urls import reverse

from webapp.forms import FullSearchForm
from webapp.models import Category, Product, OrderProduct, DeliveryCost


def category(request):
    return {"categories": Category.objects.all()}


def cart_products(request):
    products = request.session.get('products', [])
    totals = {}
    for product_pk in products:
        if product_pk not in totals:
            totals[product_pk] = 0
        totals[product_pk] += 1
    cart = []
    cart_total = 0
    for pk, qty in totals.items():
        product = Product.objects.get(pk=int(pk))
        total = product.price * qty
        cart_total += total
        cart.append({'product': product, 'qty': qty, 'total': total, 'cart_total': cart_total})
    shipping = get_shipping_cost(cart_total)
    if shipping >= 0:
        total = shipping + cart_total
        shipping_cost = shipping
        shipping_message = None
    else:
        total = cart_total
        shipping_cost = 0
        shipping_message = "Стоимость доставки будет уточнена операторатором при подтверждении заказа"
    return {"cart_products": cart, "cart_total": cart_total, "shipping_message": shipping_message, "shipping_cost": shipping_cost, "total": total}


def get_shipping_cost(cart_total):
    try:
        deliverycost_object = DeliveryCost.objects.latest('created_at')
        if cart_total >= deliverycost_object.free_from:
            shipping = 0
        else:
            shipping = deliverycost_object.cost
    except:
        shipping = -1
    return shipping


def compare_products(request):
    compare_products = request.session.get('compare', [])
    return {"compare_products": compare_products}


def get_search_form(request):
    search_form = FullSearchForm(request.GET or None)
    return {"search_form": search_form}