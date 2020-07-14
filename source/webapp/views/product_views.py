import csv

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from webapp.forms import ProductForm, ImageFormset, FullSearchForm, SpecificationFormset
from webapp.models import Product, Category, Carousel, Favorite, Tag, COLOR_CHOICES, Brand, MainCarousel, SubCategory, \
    ProductInCategory
from django.db.models import Q, Count
from django.utils.http import urlencode
from django.shortcuts import redirect
import random


# class SearchView(FormView):
#     form_class = FullSearchForm
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data()
#         search_form = FullSearchForm(self.request.GET or None)
#         context['search_form'] = search_form
#         return context
#
#
#     def form_valid(self, form):
#         query = urlencode(form.cleaned_data)
#         url = reverse('webapp:search_results') + '?' + query
#         return redirect(url)

    # def get(self, request, *args, **kwargs):
    #     search_form = FullSearchForm(self.request.GET or None)
    #     context = self.get_context_data(**kwargs)
    #     context['search_form'] = search_form
    #     return context


class IndexView(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = "products"
    # form_class = FullSearchForm
    #
    #
    # def form_valid(self, form):
    #     query = urlencode(form.cleaned_data)
    #     # url = reverse('webapp:search_results') + '?' + query
    #     url = reverse('webapp:search_results') + '?' + query
    #     return redirect(url)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.all()
        context['carouseles'] = Carousel.objects.all()
        context['main_carousel'] = MainCarousel.objects.all()
        data = csv.reader(open("/home/akyl/attractor/projects/i-shop/source/bumaga_i_bum_izdelia.csv"), delimiter='|')

        for row in data:
            if row[0] != 'Name':
                num_prod = Product.objects.filter(name=row[0]).count()
                print(num_prod)
                if num_prod == 0:
                    product = Product()
                    product.name = row[0]
                    product.description = row[1]
                    category = Category.objects.get_or_create(category_name=row[5])
                    product.category = category[0]
                    subcategory = SubCategory.objects.get_or_create(sub_name=row[4], category_id=category[0].id)
                    product.subcategory = subcategory[0]
                    product.price = 1
                    product.quantity = 1
                    product.save()
                    imgs = row[2]
                    imgs = imgs[1:-1]
                    imgs = imgs.split(',')
                    for img in imgs:
                        # print(img)
                        product.images.create(image=img[1:-1])
                    specs = row[3]
                    specs = specs[1:-1]
                    specs = specs.split(',')
                    for spec in specs:
                        print(spec)
                        spec = spec[2:-1]
                        spec = spec.split(':')

                        product.specifications.create(name=spec[0], value=spec[1])
                    product.save()
                else:
                    continue

        # search_form = FullSearchForm(self.request.GET or None)
        # context['search_form'] = search_form
        return context


class ProductView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        product.views += 1  # инкрементируем счётчик просмотров и обновляем поле в базе данных
        product.save(update_fields=['views'])
        context = super().get_context_data(**kwargs)
        # context['products'] = random.sample(list(Product.objects.filter(category=product.category)), k=4)
        # random_items = random.sample(list(Product.objects.filter(category=product.category)), k=3)
        products = Product.objects.filter(category=product.category)
        item_count = products.count()
        if item_count <= 4:
            context['products'] = random.sample(list(Product.objects.filter(category=product.category)), k=1)
        else:
            context['products'] = random.sample(list(Product.objects.filter(category=product.category)), k=4)
        # print(item_count, "ITEM COUNT")
        # random_item = q[random.randint(1, item_count + 1)]
        # print(random_item, "THIS IS RANDOM ITEMS")
        context['same_products'] = Product.objects.filter(name=self.object, brand=self.object.brand)
        # context['product.images.all'] =
        if self.object.discount:
            context['price_with_discount'] = self.object.price - self.object.discount
        color = self.request.GET.get('color')
        if color:
            context['product'] = Product.objects.get(name=self.object, brand=self.object.brand,color=color)
        return context


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'products/product_add.html'
    form_class = ProductForm
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.add_product'
    permission_denied_message = '403 Доступ запрещён!'

    def get_context_data(self, **kwargs):
        if 'formset' and 'specification_formset' not in kwargs:
            kwargs['formset'] = ImageFormset()
            kwargs['specification_formset'] = SpecificationFormset()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = ImageFormset(request.POST, request.FILES)
        specification_formset = SpecificationFormset(data=request.POST)
        if form.is_valid() and formset.is_valid() and specification_formset.is_valid():
            return self.form_valid(form, formset, specification_formset)
        return self.form_invalid(form, formset, specification_formset)

    def tags_create(self, tags):
        for tag in tags:
            product_tag, _ = Tag.objects.get_or_create(name=tag)
            self.object.tags.add(product_tag)

    def form_valid(self, form, formset, specification_formset):
        self.object = form.save()
        self.object.save()
        self.tags_create(form.cleaned_data.get('tags'))
        formset.instance = self.object
        formset.save()
        specification_formset.instance = self.object
        specification_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset, specification_formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset, specification_formset=specification_formset))

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

    def get_context_data(self, **kwargs):
        if 'formset' not in kwargs:
            kwargs['formset'] = ImageFormset(instance=self.object)
            kwargs['specification_formset'] = SpecificationFormset(instance=self.object)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = ImageFormset(request.POST, request.FILES, instance=self.object)
        specification_formset = SpecificationFormset(instance=self.object, data=request.POST)


        if form.is_valid() and formset.is_valid() and specification_formset.is_valid():
            return self.form_valid(form, formset, specification_formset)
        return self.form_invalid(form, formset, specification_formset)

    def form_valid(self, form, formset, specification_formset):
        formset.instance = self.object
        formset.save()
        specification_formset.instance = self.object
        specification_formset.save()
        self.object = form.save()
        self.object.save()
        tags = form.cleaned_data.get('tags')
        self.save_tags(tags)
        return HttpResponseRedirect(self.get_success_url())
        # return super().form_valid(form)

    def form_invalid(self, form, formset, specification_formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset, specification_formset=specification_formset))

    def save_tags(self, tags):
        self.object.tags.clear()
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            self.object.tags.add(tag)

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


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
        context['product_in_category'] = ProductInCategory.objects.first()
        context['product_category'] = Category.objects.get(pk=self.kwargs.get('pk'))
        context['products'] = Product.objects.filter(category_id=self.kwargs.get('pk'))
        context['colors'] = COLOR_CHOICES
        context['same_color_products'] = Product.objects.filter(category_id=self.kwargs.get('pk')).values_list('color', flat=None).annotate(Count('pk'))
        context['one_category_brands'] = Brand.objects.filter(products__category_id=self.kwargs.get('pk')).distinct()
        brand = self.request.GET.get('brand')
        color = self.request.GET.get('color')
        tag = self.request.GET.get('tag')
        if brand:
            context['products'] = Product.objects.filter(Q(brand__brand_name=brand), Q(category=self.kwargs.get('pk')))
        elif color:
            context['products'] = Product.objects.filter(Q(color=color), Q(category=self.kwargs.get('pk')))
        elif tag:
            context['products'] = Product.objects.filter(tags__name__iexact=tag)
        self.get_url()
        return context


class ProductALLListView(ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    # paginate_by = 5
    # paginate_orphans = 1


class ProductListGetView(ListView):
    template_name = 'products/products_list_get.html'
    model = Product

    def get_url(self):
        global site
        site = self.request.path
        return site

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['product_in_category'] = ProductInCategory.objects.first()
        # context['product_category'] = Category.objects.get(pk=self.kwargs.get('pk'))
        # context['products'] = Product.objects.filter(category_id=self.kwargs.get('pk'))
        context['colors'] = COLOR_CHOICES
        # context['same_color_products'] = Product.objects.filter(category_id=self.kwargs.get('pk')).values_list('color', flat=None).annotate(Count('pk'))
        # context['one_category_brands'] = Brand.objects.filter(products__category_id=self.kwargs.get('pk')).distinct()
        context['same_color_products'] = COLOR_CHOICES
        context['one_category_brands'] = Brand.objects.all()
        news = self.request.GET.get('news')
        popular = self.request.GET.get('popular')
        all = self.request.GET.get('all')
        offer = self.request.GET.get('offer')
        brand = self.request.GET.get('brand')
        color = self.request.GET.get('color')
        if brand:
            brand = Brand.objects.get(brand_name=self.request.GET.get('brand'))
        if color:
            context['products'] = Product.objects.filter(Q(color=color))
        # tag = self.request.GET.get('tag')
        if all:
            context['products'] = Product.objects.all()
        if news:
            context['products'] = Product.objects.order_by('-date')[:12]
        if offer:
            context['products'] = Product.objects.filter(Q(offer=True) | Q(discount__isnull=False))[:12]
        if popular:
            context['products'] = Product.objects.order_by('-views')[:12]
        if brand:
            context['products'] = Product.objects.filter(brand=brand)
        # elif tag:
        #     context['products'] = Product.objects.filter(tags__name__iexact=tag)
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


class SearchResultsView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    # paginate_by = 2
    # paginate_orphans = 1

    def get_url(self):
        global site
        site = self.request.get_full_path()
        return site

    def get_context_data(self, *, text=None, **kwargs):
        form = FullSearchForm(data=self.request.GET)
        if form.is_valid():
            text = form.cleaned_data.get("text")
            category = form.cleaned_data.get('category')
        query = self.get_query_string()
        text = form.cleaned_data.get("text").capitalize()
        category = form.cleaned_data.get("category")
        category_pk = get_object_or_404(Category, pk=category.pk)
        products = Product.objects.filter(Q(name__icontains=text, category_id=category))
        brand = self.request.GET.get('brand')
        color = self.request.GET.get('color')
        colors = COLOR_CHOICES
        same_color_products = Product.objects.filter(category_id=category_pk).values_list('color',flat=None).annotate(Count('pk'))
        one_category_brands = Brand.objects.filter(products__category_id=category_pk).distinct()
        if brand:
            products = Product.objects.filter(Q(brand__brand_name=brand), Q(category=self.kwargs.get('pk')))
        elif color:
            products = Product.objects.filter(Q(color=color), Q(category=self.kwargs.get('pk')))
        return super().get_context_data(
            form=form, query=query, products=products, product_category=category_pk, same_color_products=same_color_products,
            one_category_brands=one_category_brands, colors=colors
        )

    def get_query_string(self):
        data = {}
        for key in self.request.GET:
            if key != 'page':
                data[key] = self.request.GET.get(key)
        return data


class ProductsOfferListView(ListView):
    template_name = 'offers.html'
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['products'] = Product.objects.filter(Q(offer=True)|Q(discount__isnull=False))
        context['colors'] = COLOR_CHOICES
        context['same_color_products'] = Product.objects.filter(Q(offer=True)|Q(discount__isnull=False)).values_list('color',                                                            flat=None).annotate(Count('pk'))
        context['one_category_brands'] = Brand.objects.filter(Q(products__offer=True)|Q(products__discount__isnull=False)).distinct()
        brand = self.request.GET.get('brand')
        color = self.request.GET.get('color')
        if brand:
            context['products'] = Product.objects.filter(Q(offer=True) | Q(discount__isnull=False), brand__brand_name=brand)
        elif color:
            context['products'] = Product.objects.filter(Q(offer=True) | Q(discount__isnull=False), color=color)
        return context


class AddToOffer(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=request.POST.get('pk'))
        product.offer=True
        product.save()
        return JsonResponse({'pk': product.pk})


class DeleteFromOffer(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=request.POST.get('pk'))
        product.offer = False
        product.save()
        return JsonResponse({'pk': product.pk})


class ProductSubCategoryListView(ListView):
    template_name = 'products/products.html'
    model = Product

    def get_url(self):
        global site
        site = self.request.path
        return site

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['product_category'] = Category.objects.get(subcategories=self.kwargs.get('pk'))
        context['products'] = Product.objects.filter(subcategory_id=self.kwargs.get('pk'))
        context['colors'] = COLOR_CHOICES
        context['same_color_products'] = Product.objects.filter(category_id=self.kwargs.get('pk')).values_list('color', flat=None).annotate(Count('pk'))
        context['one_category_brands'] = Brand.objects.filter(products__category_id=self.kwargs.get('pk')).distinct()
        brand = self.request.GET.get('brand')
        color = self.request.GET.get('color')
        tag = self.request.GET.get('tag')
        if brand:
            context['products'] = Product.objects.filter(Q(brand__brand_name=brand), Q(subcategory=self.kwargs.get('pk')))
        elif color:
            context['products'] = Product.objects.filter(Q(color=color), Q(subcategory=self.kwargs.get('pk')))
        elif tag:
            context['products'] = Product.objects.filter(tags__name__iexact=tag)
        self.get_url()
        return context


def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id).order_by('sub_name').values()
    return JsonResponse({'subcategories': list(subcategories)})

