from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django.forms import widgets

from accounts.models import Profile, PROFILE_TYPE_CHOICES, SEX
from django.forms import TextInput

STAFF_TYPE_CHOICES = (
    ('seller', 'Продавец'),
    ('admin', 'Администратор'),
)


class StaffCreationForm(forms.Form):
    username = forms.CharField(max_length=20, label='Username', required=True)
    first_name = forms.CharField(max_length=20, label='Имя', required=True)
    last_name = forms.CharField(max_length=20, label='Фамилия', required=True)
    password = forms.CharField(max_length=20, min_length=8, label='Password', required=True,
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=20, min_length=8, label='Password Comfirm', required=True,
                               widget=forms.PasswordInput)
    phone_number = forms.CharField(required=True, label='Мобильный телефон')
    email = forms.EmailField(label='Email', required=True)
    type = forms.ChoiceField(choices=STAFF_TYPE_CHOICES, required=True, label='Тип')


    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     try:
    #         User.objects.get(email=email)
    #         raise ValidationError('User with this email already exists',
    #                               code='user_email_exists')
    #     except User.DoesNotExist:
    #         return email

    def clean_username(self):
        username=self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            raise ValidationError('User with this username already exists',
                              code='user_username_exists')
        except User.DoesNotExist:
            return username

    def clean_password_confirmn(self):
        super().clean()
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['password_confirm']
        if password_1 != password_2:
            raise ValidationError('Passwords do not match',
                                  code='passwords_do_not_match')
        return password_2

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']


class UserCreationForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username', required=True)
    first_name = forms.CharField(max_length=20, label='Имя', required=True)
    last_name = forms.CharField(max_length=20, label='Фамилия', required=True)
    phone_number = forms.CharField(required=True, label='Мобильный телефон')
    type = forms.ChoiceField(choices=PROFILE_TYPE_CHOICES, required=True, label='Тип')
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(max_length=100, label='Password', required=True,
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=100, label='Password Confirm', required=True,
                                       widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise ValidationError('Пользователь с указанным email существует',
                                  code='user_email_exists')
        except User.DoesNotExist:
            return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            raise ValidationError('Пользователь с указанным именем пользователя существует, введите другое имя пользователя',
                                  code='user_username_exists')
        except User.DoesNotExist:
            return username

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['password_confirm']
        if password_1 != password_2:
            raise ValidationError('Указанные пароли не совпадают, попробуйте снова',
                                  code='passwords_do_not_match')
        return self.cleaned_data


class UserInfoChangeForm(forms.ModelForm):
    photo = forms.ImageField(label='Avatar', required=False)
    mobile_phone = forms.CharField(required=True, label='Мобильный телефон')
    birth_date = forms.DateField(required=False, label='Дата рождения')
    sex = forms.ChoiceField(choices=SEX, required=False, label='Пол')

    def get_initial_for_field(self, field, field_name):
        if field_name in self.Meta.profile_fields:
            return getattr(self.instance.profile, field_name)
        return super().get_initial_for_field(field, field_name)

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.user_profile = self.save_profile(commit)
        return user

    def save_profile(self, commit=True):
        profile, _ = Profile.objects.get_or_create(user=self.instance)
        for field in self.Meta.profile_fields:
            setattr(profile, field, self.cleaned_data.get(field))
        if commit:
            profile.save()
        return profile

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        profile_fields =['mobile_phone', 'sex', 'birth_date', 'photo']


class CompanyInfoChangeForm(forms.ModelForm):
    photo = forms.ImageField(label='Avatar', required=False)
    mobile_phone = forms.CharField(required=True, label='Мобильный телефон')
    birth_date = forms.DateField(required=False, label='Дата рождения')
    sex = forms.ChoiceField(choices=SEX, required=False, label='Пол')
    company_name = forms.CharField(required=True, label='Название компании')
    inn = forms.CharField(required=True, label='ИНН')
    okpo = forms.CharField(required=True, label='ОКПО')
    phone = forms.CharField(required=True, label='Телефон контактного лица')

    def get_initial_for_field(self, field, field_name):
        if field_name in self.Meta.profile_fields:
            return getattr(self.instance.profile, field_name)
        return super().get_initial_for_field(field, field_name)

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.user_profile = self.save_profile(commit)
        return user

    def save_profile(self, commit=True):
        profile, _ = Profile.objects.get_or_create(user=self.instance)
        for field in self.Meta.profile_fields:
            setattr(profile, field, self.cleaned_data.get(field))
        if commit:
            profile.save()
        return profile

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        profile_fields = ['mobile_phone', 'sex', 'birth_date', 'photo', 'phone',  'company_name', 'inn', 'okpo']
        widgets = {
            'phone': TextInput(attrs={'placeholder': 'Моб. номер в формате +996555123456'}),
        }


class UserPasswordChangeForm(forms.ModelForm):
    password = forms.CharField(max_length=20, min_length=8, required=True, label='New Password',
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=20, min_length=8, required=True, label='New Password confirm',
                                       widget=forms.PasswordInput)
    old_password = forms.CharField(max_length=20, min_length=8, required=True, label='Old Password',
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user=self.instance
        if not user.check_password(old_password):
            raise ValidationError('Invalid password.', code='invalid_password')
        return old_password

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_confirm')
        if password_1 != password_2:
            raise ValidationError('Passwords do not match.', code='passwords_do_not_match')
        return self.cleaned_data

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['password', 'password_confirm', 'old_password']