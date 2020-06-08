# from django.contrib.auth.models import User
# from django.forms import widgets
# from webapp.models import Status, Type, Task, Project, Team


# class TaskForm(forms.ModelForm):
#     def __init__(self, users_list, **kwargs):
#         super().__init__(**kwargs)
#         self.fields['assigned_to'].queryset = User.objects.filter(pk__in=users_list)

#     class Meta:
#         model = Task
#         fields = ['summary', 'description', 'project', 'status', 'type', 'assigned_to']
#         object = 'task'
#         widgets = {
#             'description': widgets.Textarea
#         }


# class StatusForm(forms.ModelForm):
#     class Meta:
#         model = Status
#         fields =['status_name']


# class TypeForm(forms.ModelForm):
#     class Meta:
#         model = Type
#         fields =['type_name']


# class ProjectTaskForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         self.users = kwargs.pop('users')
#         super().__init__(*args, **kwargs)
#         self.fields['assigned_to'].queryset = self.users

#     class Meta:
#         model = Task
#         fields = ['summary', 'description', 'status', 'type', 'assigned_to']


# class ProjectForm(forms.ModelForm):
#     users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=None, widget=forms.SelectMultiple)

#     class Meta:
#         model = Project
#         fields =['name', 'description', 'users']

# class ProjectUserForm(forms.ModelForm):
#     users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=None, widget=forms.SelectMultiple)

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.fields['users'].initial = self.initial.get('users')

#     class Meta:
#         model = Project
#         fields =['users']


# class SimpleSearchForm(forms.Form):
#     search = forms.CharField(max_length=100, required=False, label="Search")
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, inlineformset_factory
from webapp.models import OrderProduct, Order, Product, Image, Category
from django import forms


class CartOrderCreateForm(ModelForm):
    def __init__(self, user=None, **kwargs):
        self.user = user
        if user and not user.is_authenticated:
            self.user = None
        super().__init__(**kwargs)

    def clean_first_name(self):
        if not self.user and not self.cleaned_data.get('first_name'):
            raise ValidationError('Вы должны авторизоваться либо указать ваше имя!')

    def clean_email(self):
        if not self.user and not self.cleaned_data.get('email'):
            raise ValidationError('Вы должны авторизоваться либо указать ваш email!')

    def clean_phone(self):
        if not self.user and not self.cleaned_data.get('phone'):
            raise ValidationError('Вы должны авторизоваться либо указать ваш телефон!')

    def save(self, commit=True):
        self.instance.user = self.user
        return super().save(commit)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone']


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


class OrderProductForm(ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['product', 'amount']

class ProductForm(forms.ModelForm):
    tags = forms.CharField(max_length=101, required=False, label='Тэги')

    class Meta:
        model = Product
        exclude = ['in_stock', 'date', 'tags']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        tags = tags.split(',')
        tags = [tag.strip() for tag in tags]
        tags = filter(lambda tag: len(tag) > 0, tags)
        return tags

ImageFormset = inlineformset_factory(Product, Image, fields='__all__', extra=1, validate_min=False, min_num=0, can_delete=True)


ProductsFormset = inlineformset_factory(Order, OrderProduct, OrderProductForm, extra=0,
                                        validate_min=True, min_num=1, can_delete=True)


class FullSearchForm(forms.Form):
    text = forms.CharField(max_length=100, required=False, label='Поиск')
    category = forms.ModelChoiceField(label='Категория', queryset=Category.objects.all(), required=False)

    def clean(self):
        super().clean()
        data = self.cleaned_data
        text = data.get('text')
        category_name = self.cleaned_data.get('category')
        category = data.get('category')
        # user = data.get('user')
        # if not (text):
        #     raise ValidationError('Вы не ввели текст поиска!',
        #                           code='text_search_empty')
        # errors = []
        # # if text:
        # #     # in_username = data.get('in_username')
        # #     # in_first_name = data.get('in_first_name')
        # #     # in_phone = data.get('in_phone')
        # #     if not (in_username or in_first_name or in_phone):
        # #         errors.append(ValidationError(
        # #             'Пожулайста отметте критерии поиска, выставите галочки, где необходимо искать',
        # #             code='text_search_criteria_empty'
        # #         ))
        # if errors:
        #     raise ValidationError(errors)
        return data