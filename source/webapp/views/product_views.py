from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import ProductForm, ImageFormset
from webapp.models import Product, Category, Carousel, Favorite, Tag


class IndexView(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.all()
        context['carouseles'] = Carousel.objects.all()
        return context


class ProductView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'products/product_add.html'
    form_class = ProductForm
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.add_product'
    permission_denied_message = '403 Доступ запрещён!'

    def get_context_data(self, **kwargs):
        if 'formset' not in kwargs:
            kwargs['formset'] = ImageFormset()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = ImageFormset(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        return self.form_invalid(form, formset)

    def tags_create(self, tags):
        for tag in tags:
            product_tag, _ = Tag.objects.get_or_create(name=tag)
            self.object.tags.add(product_tag)

    def form_valid(self, form, formset):
        self.object = form.save()
        self.object.save()
        self.tags_create(form.cleaned_data.get('tags'))
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'base_CRUD/edit.html'
    form_class = ProductForm
    context_object_name = 'product'
    permission_required = 'webapp.change_product'

    def get_initial(self):
        return {'tags': self.get_tag_string()}

    def get_tag_string(self):
        tags = self.object.tags.all()
        tag_names = [tag.name for tag in tags]
        return ', '.join(tag_names)

    def form_valid(self, form):
        tags = form.cleaned_data.get('tags')
        self.save_tags(tags)
        return super().form_valid(form)

    def save_tags(self, tags):
        self.object.tags.clear()
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            self.object.tags.add(tag)

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


# class ProductDeleteView(PermissionRequiredMixin, DeleteView):
#     model = Product
#     template_name = 'products/product_delete.html'
#     success_url = reverse_lazy('webapp:index')
#     context_object_name = 'product'
#     permission_required = 'webapp.delete_product'
#
#     def delete(self, request, *args, **kwargs):
#         product = self.object = self.get_object()
#         product.in_stock = False
#         product.save()
#         return HttpResponseRedirect(self.get_success_url())

class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'base_CRUD/delete.html'
    success_url = reverse_lazy('webapp:products_all')
    permission_required = 'webapp.delete_product'
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        user = self.request.user
        return user.is_staff


class ProductListView(ListView):
    template_name = 'products/products.html'
    model = Product

    def get_url(self):
        global site
        site = self.request.path
        return site

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['product_category'] = Category.objects.get(pk=self.kwargs.get('pk'))
        context['products'] = Product.objects.filter(category_id=self.kwargs.get('pk'))
        self.get_url()
        return context


class AddToFavorites(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=request.POST.get('pk'))
        Favorite.objects.get_or_create(user=request.user, product=product)
        return JsonResponse({'pk': product.pk})


class DeleteFromFavorites(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=request.POST.get('pk'))
        Favorite.objects.filter(product=product, user=request.user).delete()
        return JsonResponse({'pk': product.pk})


class FavoritesList(ListView):
    model = Favorite
    template_name = 'favorites.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['favorite_products'] = Favorite.objects.filter(user=self.request.user)
        return context
