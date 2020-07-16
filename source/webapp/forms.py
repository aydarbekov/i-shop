from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, inlineformset_factory
from webapp.models import OrderProduct, Order, Product, Image, Category, SubCategory, Brand, DeliveryAddress, \
    Specifications


class CartOrderCreateForm(ModelForm):
    # address = forms.ChoiceField(label='address_id', widget=forms.Select)
    # address = forms.ModelChoiceField(queryset=DeliveryAddress.objects.all(), empty_label="Адрес доставки")
    # address = forms.ModelChoiceField(queryset=DeliveryAddress.objects.all(), widget=forms.Select(attrs={'class': 'address'}))

    def __init__(self, user=None, *args, **kwargs):
        # super(CartOrderCreateForm, self).__init__(*args, **kwargs)
        self.user = user
        print('user', user)
        print(kwargs)

        # self.fields['address'].queryset = DeliveryAddress.objects.filter(user=user)
        # self.fields['address'].queryset = DeliveryAddress.objects.all()

        # print(self.cleaned_data)
    #     addresses = DeliveryAddress.objects.all()
        # address = [(i.product.id, i.product.name) for i in variants]
        # self.fields['address'] = forms.ChoiceField
        if user and not user.is_authenticated:
            self.user = None
        super().__init__(**kwargs)

    def clean_first_name(self):
        print("self.cleaned_data", self.cleaned_data)
        print('clean_fir_name')
        # print(self.user.first_name)
        print(self.cleaned_data.get('first_name'))
        if not self.user and not self.cleaned_data.get('first_name'):
        # if not self.cleaned_data.get('first_name'):
            raise ValidationError('Вы должны авторизоваться либо указать ваше имя!')
        # if self.cleaned_data.get('first_name') == "Vadim":
        #     raise ValidationError("Вадиму НЕЛЬЗЯ!!!")
        print('FDVT')
        return self.cleaned_data.get('first_name')
    #
    # def clean_email(self):
    #     print(self.user.email)
    #     if not self.user and not self.cleaned_data.get('email'):
    #         raise ValidationError('Вы должны авторизоваться либо указать ваш email!')
    #
    # def clean_phone(self):
    #     print(self.user.profile.mobile_phone)
    #     if not self.user and not self.cleaned_data.get('phone'):
    #         raise ValidationError('Вы должны авторизоваться либо указать ваш телефон!')
    #
    # def save(self, commit=True):
    #     print("|SAVE")
    #     self.instance.user = self.user
    #     return super().save(commit)

    # def clean_address(self):
    #     print("self.cleaned_data", self.cleaned_data)
    #     print('clean_ADDRESS')
    #     # print(self.user.first_name)
    #     print(self.cleaned_data.get('address'))
    #     return self.cleaned_data.get('address')

    class Meta:
        model = Order
        # fields = ['first_name']
        fields = ['first_name', 'last_name', 'email', 'phone']
        # address_fields = ['city', 'street', 'building_number', 'entrance_number', 'flat_number', 'additional_info']


class ManualOrderForm(ModelForm):
    def clean_first_name(self):
        if not self.user and not self.cleaned_data.get('first_name'):
            raise ValidationError('Вы должны указать пользователя либо его имя!')

    def clean_email(self):
        if not self.user and not self.cleaned_data.get('email'):
            raise ValidationError('Вы должны указать пользователя либо его email!')

    def clean_phone(self):
        if not self.user and not self.cleaned_data.get('phone'):
            raise ValidationError('Вы должны указать пользователя либо его телефон!')

    class Meta:
        model = Order
        fields = ['user', 'first_name', 'last_name', 'email', 'address', 'phone']
        # fields = ['products', 'total_sum']


class OrderProductForm(ModelForm):

    class Meta:
        model = OrderProduct
        fields = ['product', 'amount']



class ProductForm(forms.ModelForm):
    tags = forms.CharField(max_length=101, required=False, label='Тэги')

    class Meta:
        model = Product
        exclude = ['in_stock', 'date', 'tags', 'views']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        tags = tags.split(',')
        tags = [tag.strip() for tag in tags]
        tags = filter(lambda tag: len(tag) > 0, tags)
        return tags

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['subcategory'].queryset = SubCategory.objects.none()
        # if 'category' in self.data:
        #     try:
        #         category_id = int(self.data.get('category'))
        #         print(category_id)
        #         self.fields['subcategory'].queryset = SubCategory.objects.filter(category=category_id).order_by('sub_name')
        #     except (ValueError, TypeError):
        #         pass
        # elif self.instance.pk:
        #     self.fields['subcategory'].queryset = self.instance.category.subcategories_set.order_by('sub_name')


ImageFormset = inlineformset_factory(Product, Image, fields='__all__', extra=1, validate_min=False, min_num=0, can_delete=True)
SpecificationFormset = inlineformset_factory(Product, Specifications, fields='__all__', extra=1, validate_min=False, min_num=0, can_delete=True)


ProductsFormset = inlineformset_factory(Order, OrderProduct, OrderProductForm, extra=0,
                                        validate_min=True, min_num=1, can_delete=True)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'photo']

    def clean_category_name(self):
        category_name = self.cleaned_data.get('category_name')
        if Category.objects.filter(category_name__iexact=category_name):
            raise ValidationError('Категория с таким названием уже существует!')
        else:
            return category_name


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['sub_name']

    def clean_sub_name(self):
        sub_name = self.cleaned_data.get('sub_name')
        if SubCategory.objects.filter(sub_name__iexact=sub_name):
            raise ValidationError('Подраздел с таким названием уже существует!')
        else:
            return sub_name


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name', 'photo']

    def clean_brand_name(self):
        brand_name = self.cleaned_data.get('brand_name')
        if Brand.objects.filter(brand_name=brand_name):
            raise ValidationError('Бренд с таким названием уже существует!')
        else:
            return brand_name


class FullSearchForm(forms.Form):
    text = forms.CharField(max_length=100, required=False, label='Поиск')
    # category = forms.ModelChoiceField(label='Категория', queryset=Category.objects.all(), required=True)

    # def clean(self):
    #     super().clean()
    #     data = self.cleaned_data
    #     text = data.get('text')
    #     category_name = self.cleaned_data.get('category')
    #     category = data.get('category')
    #     # print(category_name)
    #     # user = data.get('user')
    #     # if not (category):
    #     #     raise ValidationError('Вы не ввели текст поиска!',
    #     #                           code='text_search_empty')
    #     # if not (text):
    #     #     raise ValidationError('Вы не ввели текст поиска!',
    #     #                           code='text_search_empty')
    #     # errors = []
    #     # # if text:
    #     # #     # in_username = data.get('in_username')
    #     # #     # in_first_name = data.get('in_first_name')
    #     # #     # in_phone = data.get('in_phone')
    #     # #     if not (in_username or in_first_name or in_phone):
    #     # #         errors.append(ValidationError(
    #     # #             'Пожулайста отметте критерии поиска, выставите галочки, где необходимо искать',
    #     # #             code='text_search_criteria_empty'
    #     # #         ))
    #     # if errors:
    #     #     raise ValidationError(errors)
    #     return data
