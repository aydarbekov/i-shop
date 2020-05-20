from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4
from phonenumber_field.modelfields import PhoneNumberField

PROFILE_TYPE_CHOICES = (
    ('client', 'Физическое лицо'),
    ('company', 'Юридическое лицо'),
)

SEX = (
    ('man', 'Мужской'),
    ('woman', 'Женский'),
)

class Token(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                             verbose_name='user', related_name='registration_tokens')
    token = models.UUIDField(verbose_name='Token', default=uuid4)

    def __str__(self):
        return str(self.token)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, verbose_name='User')
    mobile_phone = PhoneNumberField(max_length=20, verbose_name='Мобильный телефон')
    photo = models.ImageField(upload_to='users_photo', null=True, blank=True, verbose_name='Фото')
    type = models.CharField(max_length=20, choices=PROFILE_TYPE_CHOICES, verbose_name='Тип')
    birth_date = models.DateField(max_length=10, verbose_name='Дата рождения', null=True, blank=True)
    sex = models.CharField(max_length=20, choices=SEX, verbose_name='Тип', blank=True, null=True)
    company_name = models.CharField(verbose_name='Название компании', max_length=30, null=True, blank=True)
    inn = models.CharField(verbose_name="ИНН", max_length=50, null=True, blank=True)
    okpo = models.CharField(verbose_name="ИНН", max_length=50, null=True, blank=True)
    phone = PhoneNumberField(max_length=20, verbose_name='Телефон контактного лица',blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
