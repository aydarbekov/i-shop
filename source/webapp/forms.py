# from django import forms
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
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from webapp.models import OrderProduct, Order


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