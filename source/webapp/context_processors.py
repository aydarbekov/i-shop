from django.views import View

from webapp.models import Category, Product, OrderProduct


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
        cart.append({'product': product, 'qty': qty, 'total': total, 'cart_total':cart_total})
    return {"cart_products": cart, "cart_total": cart_total}
