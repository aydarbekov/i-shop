from django.urls import path
from webapp.views.brand_views import BrandListView, BrandCreateView, BrandUpdateView, BrandDeleteView
from webapp.views.category_views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
from webapp.views.product_views import IndexView, ProductView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    ProductListView, AddToFavorites, DeleteFromFavorites, FavoritesList
from webapp.views.review_views import ReviewCreateView
from webapp.views.subcategory_views import SubCategoryDeleteView, SubCategoryCreateView, SubCategoryUpdateView
from .views.cart_views import CartChangeView, CartView, cartdeleteitem, cartadditem
from .views.orders_view import OrderListView, OrderDetailView, OrderUpdateView, OrderProductUpdateView, OrderProductDeleteView
from .views.news_views import NewsView, NewsAddView, NewsDetailView, NewsDeleteView, NewsEditView
from .views.carousel_views import *

app_name = 'webapp'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/<int:pk>/', ProductView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product_category/<int:pk>', ProductListView.as_view(), name='products_category'),
    path('product/add-to-favorites/', AddToFavorites.as_view(), name='add_to_favorites'),
    path('product/delete-from-favorites/', DeleteFromFavorites.as_view(), name='delete_from_favorites'),
    path('products_favorites', FavoritesList.as_view(), name='favorite_products'),
    path('categories/', CategoryListView.as_view(), name='categories_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_add'),
    path('category/change/<int:pk>/', CategoryUpdateView.as_view(), name='category_change'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('category/<int:pk>/subcategory_add/', SubCategoryCreateView.as_view(), name='subcategory_add'),
    path('subcategory/change/<int:pk>/', SubCategoryUpdateView.as_view(), name='subcategory_change'),
    path('subcategory/delete/<int:pk>/', SubCategoryDeleteView.as_view(), name='subcategory_delete'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name="order_detail"),
    path('orders/<int:pk>/update', OrderUpdateView.as_view(), name='order_update'),
    path('orders/product/update/<int:pk>/<int:id>', OrderProductUpdateView.as_view(), name='order_product_update'),
    path('orders/product/delete/<int:pk>/<int:id>', OrderProductDeleteView.as_view(), name='order_product_delete'),
    path('cart/change/', CartChangeView.as_view(), name='cart_change'),
    path('cart/', CartView.as_view(), name='cart'),
    path('review/add/<int:pk>/', ReviewCreateView.as_view(), name='review_create'),
    path('news/', NewsView.as_view(), name='news'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/add/', NewsAddView.as_view(), name='news_add'),
    path('news/change/<int:pk>/', NewsEditView.as_view(), name='news_edit'),
    path('news/delete/<int:pk>/', NewsDeleteView.as_view(), name='news_delete'),
    path('brands/', BrandListView.as_view(), name='brands_list'),
    path('brand/add/', BrandCreateView.as_view(), name='brand_add'),
    path('brand/change/<int:pk>/', BrandUpdateView.as_view(), name='brand_change'),
    path('brand/delete/<int:pk>/', BrandDeleteView.as_view(), name='brand_delete'),
    path('carousel/', CarouselListView.as_view(), name='carousel_list'),
    path('carousel/add/', CarouselCreateView.as_view(), name='carousel_add'),
    path('carousel/change/<int:pk>/', CarouselUpdateView.as_view(), name='carousel_change'),
    path('carousel/delete/<int:pk>/', CarouselDeleteView.as_view(), name='carousel_delete'),
    path('carousel/change/product/<int:pk>/', CarouselAddView.as_view(), name='product_carousel_add'),
    path('carousel/products/all/', ProductALLListView.as_view(), name='products_all'),
    path('carouseldeleteitem/', carouseldeleteitem, name='carouseldeleteitem'),
    path('carouseladditem/', carouseladditem, name='carouseladditem'),
    path('cartdeleteitem/', cartdeleteitem, name='cartdeleteitem'),
    path('cartadditem/', cartadditem, name='cartadditem'),
]
