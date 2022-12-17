# TODO: Создать защиту от аккаунтов, использующие чужие заказы

from django.db import models
from django.core.validators import RegexValidator

from Orders.models import Orders

from phonenumber_field.modelfields import PhoneNumberField

login_banned_symbols = """[+-/\{}`~!@%^&*()"'№;:?*|<>]"""
password_banned_symbols = """[+-/\{}`~%^&*()"'№;:*|<>]"""


class UserAccounts(models.Model):
    login = models.CharField('Логин', max_length=30, validators=[RegexValidator(login_banned_symbols, inverse_match=True)], unique= True)
    password = models.CharField('Пароль', validators=[RegexValidator(password_banned_symbols, inverse_match=True)], max_length=20)
    name = models.CharField('Имя', max_length=30)
    surname = models.CharField('Фамилия', max_length=30)
    email = models.EmailField('E-mail')
    phone = PhoneNumberField(verbose_name='Номер телефона', default='+12125552368')
    order_history = models.ManyToManyField(Orders, verbose_name='История заказов', null=True, blank=True)

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    def __str__(self):
        return f'@{self.login}'

