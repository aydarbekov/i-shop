from django.contrib.auth.models import User
from django.db import models


CITY_CHOICES = (
    ('Bishkek', 'Бишкек'),
)


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='Категория')

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    sub_name = models.CharField(max_length=50, verbose_name='Подраздел')
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.PROTECT,
                                 verbose_name='Категория')

    def __str__(self):
        return self.sub_name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Товар')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT,
                                verbose_name='Категория')
    photo = models.ImageField(upload_to='product_images', null=True, blank=True, verbose_name='Изображение')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    in_stock = models.BooleanField(verbose_name='В наличии', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class DeliveryAddress(models.Model):
    city = models.CharField(max_length=20, choices=CITY_CHOICES, default=CITY_CHOICES[0][0], verbose_name="Город")
    street = models.CharField(max_length=50, verbose_name="Улица")
    building_number = models.CharField(max_length=10, verbose_name="Номер дома")
    entrance_number = models.CharField(max_length=10, null=True, blank=True, verbose_name="Подъезд")
    flat_number = models.CharField(max_length=5, null=True, blank=True, verbose_name="Номер квартиры/офиса")
    additional_info = models.CharField(max_length=200, null=True, blank=True, verbose_name="Дополнительная информация")

    def __str__(self):
        return f'{self.city}/{self.street}/{self.building_number}'

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'


class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Пользователь', related_name='orders')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(max_length=50, verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.ForeignKey(DeliveryAddress, on_delete=models.PROTECT, verbose_name="Адрес доставки")
    products = models.ManyToManyField(Product, through='OrderProduct', through_fields=('order', 'product'), verbose_name='Товары', related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return "{} / {}".format(self.email, self.phone)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orderproduct", verbose_name='Товар')
    amount = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.product.name} {self.order}'

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'