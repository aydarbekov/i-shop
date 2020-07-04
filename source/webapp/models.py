from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


CITY_CHOICES = (
    ('Бишкек', 'Бишкек'),
)
COLOR_CHOICES = (
    ('none', 'Любой'),
    ('white', 'Белый'),
    ('green', 'Зеленый'),
    ('grey', 'Серый'),
    ('blue', 'Синий'),
    ('red', 'Красный'),
    ('yellow', 'Желтый'),
    ('black', 'Черный'),
    ('orange', 'Оранжевый'),
    ('brown', 'Коричневый'),
    ('beige', 'Бежевый'),
    ('pink', 'Розовый'),
    ('purple', 'Фиолетовый'),
)


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='Категория')
    photo = models.ImageField(upload_to='category_images', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(models.Model):
    sub_name = models.CharField(max_length=50, verbose_name='Подраздел')
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.PROTECT,
                                 verbose_name='Категория')

    def __str__(self):
        return self.sub_name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегория'


class Brand(models.Model):
    brand_name = models.CharField(max_length=50, verbose_name='Название')
    photo = models.ImageField(upload_to='brand_images', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.brand_name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Tag(models.Model):
    name = models.CharField(max_length=31, verbose_name='Тег')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Товар')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT,
                                verbose_name='Категория')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='product', verbose_name='Подраздел')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    in_stock = models.BooleanField(verbose_name='В наличии', default=True)
    description = models.TextField(max_length=3000, verbose_name='Описание', null=True, blank=True)
    color = models.CharField(max_length=20,choices=COLOR_CHOICES, default=COLOR_CHOICES[0][0], verbose_name="Цвет", null=True, blank=True)
    discount = models.IntegerField(verbose_name='Скидка', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    quantity = models.IntegerField(verbose_name='Количество')
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Бренд', related_name='products')
    tags = models.ManyToManyField(Tag, blank=True, related_name='products', verbose_name='Теги')
    offer = models.BooleanField(verbose_name='Акция', default=False)
    views = models.IntegerField('Просмотры', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class DeliveryAddress(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='address')
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


class DeliveryCost(models.Model):
    cost = models.IntegerField(verbose_name='Стоимость доставки')
    free_from = models.IntegerField(verbose_name='Бесплатная доставка при сумме заказа от')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.cost} / бесплатно от {self.free_from} / {self.created_at.date()}'

    class Meta:
        verbose_name = 'Стоимость доставки'
        verbose_name_plural = 'Стоимость доставки'


class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Пользователь', related_name='orders')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(max_length=50, verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.ForeignKey(DeliveryAddress, on_delete=models.PROTECT, verbose_name="Адрес доставки")
    shipping_cost = models.ForeignKey(DeliveryCost, on_delete=models.PROTECT, verbose_name="Стоимость доставки", null=True)
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


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, verbose_name='Товар', default=None)
    grade = models.IntegerField(verbose_name='Оценка', default=None)
    text = models.TextField(max_length=500, verbose_name='Отзыв', null=True, blank=True)
    author = models.ForeignKey('auth.User', related_name='review_author', on_delete=models.CASCADE, verbose_name='Автор', default=None)
    date = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name='Дата')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Image(models.Model):
    image = models.ImageField(upload_to='product_images', verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Объявление')

    def _str_(self):
        return self.product

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class News(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Заголовок')
    text = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    photo = models.ImageField(upload_to='news_images', null=True, blank=True, verbose_name='Фото')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Carousel(models.Model):
    product = models.ForeignKey(Product, related_name='carousel_product', on_delete=models.CASCADE,
                                verbose_name='Карусель', null=True, blank=True)

    def _str_(self):
        return self.product.name


class Favorite(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='favored_by')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class MainCarousel(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Заголовок')
    text = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Текст')
    photo = models.ImageField(upload_to='main_carousel_images', null=True, blank=True, verbose_name='Картинка')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', null=True, blank=True)
    link = models.URLField(null=True, blank=True, verbose_name='Ссылка')
    image = models.ImageField(upload_to='main_carousel_images', null=True, blank=True, verbose_name='Картинка карусели (фон)')


    def _str_(self):
        return self.title

    class Meta:
        verbose_name = 'Главная карусель'
        verbose_name_plural = 'Главная карусель'


class ProductInCategory(models.Model):
    product = models.ForeignKey(Product, related_name='product_in_category', on_delete=models.CASCADE,
                                verbose_name='Рекоммендуемы товар в категории', null=True, blank=True)

    def _str_(self):
        return self.product.name

    class Meta:
        verbose_name = 'Товар в категории'
        verbose_name_plural = 'Товар в категории'


class Specifications(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='speсifications')
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name='Название')
    value = models.CharField(max_length=200, null=False, blank=False, verbose_name='Значение')

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"

    class Meta:
        verbose_name = 'Характеристи'
        verbose_name_plural = 'Характеристика'
