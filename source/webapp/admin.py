from django.contrib import admin
from webapp.models import Category, Product, SubCategory, DeliveryAddress, Order, OrderProduct


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'category_name']
    list_filter = ['category_name']
    list_display_links = ['pk', 'category_name']


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sub_name']
    list_filter = ['sub_name']
    list_display_links = ['pk', 'sub_name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'category', 'price', 'in_stock']
    list_filter = ['name', 'category', 'price', 'in_stock']
    list_display_links = ['name', 'category', 'price', 'in_stock']


class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ['pk', 'city', 'street', 'building_number', 'entrance_number', 'flat_number', 'additional_info']


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    fields = ('product', 'amount')
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'phone', 'email', 'address', 'created_at')
    inlines = (OrderProductInline, )


admin.site.register(Order, OrderAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(DeliveryAddress, DeliveryAddressAdmin)

