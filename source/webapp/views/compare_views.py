from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView

from webapp.models import Product


class CompareView(ListView):
    model = Product
    template_name = 'compare.html'

    def get_context_data(self, **kwargs):
        compare = self.request.session.get('compare', [])
        compare_list = []
        for pk in compare:
            product = Product.objects.get(pk=pk)
            compare_list.append({'product': product})
        kwargs['compare'] = compare_list
        return super().get_context_data(**kwargs)

class CompareChangeView(View):
    def get(self, request, *args, **kwargs):
        compare = request.session.get('compare', [])
        pk = request.GET.get('pk')
        action = request.GET.get('action')
        next_url = request.GET.get('next', reverse('webapp:index'))
        if action == 'delete':
            new_products = []
            for product_pk in compare:
                if product_pk != pk:
                    new_products.append(product_pk)
            compare= new_products
        else:
            for product_pk in compare:
                if product_pk == pk:
                    compare.remove(product_pk)
                    break

        request.session['compare'] = compare

        return redirect(next_url)


def comparedeleteitem(request):
    compare = request.session.get('compare', [])
    pk = request.POST.get('pk')
    for product_pk in compare:
        if product_pk == pk:
            compare.remove(product_pk)
            break
    request.session['compare'] = compare
    return JsonResponse({'pk': pk})


def compareadditem(request):
    compare = request.session.get('compare', [])
    pk = request.POST.get('pk')
    product = get_object_or_404(Product, pk=request.POST.get('pk'))
    if pk in compare:
        compare.remove(pk)
        compare.append(pk)
    elif pk not in compare and len(compare) >= 3:
        compare.pop()
        compare.append(pk)
    elif len(compare) >= 3:
        compare.pop()
        compare.append(pk)
    else:
        compare.append(pk)
    request.session['compare'] = compare
    return JsonResponse({'pk': product.pk})