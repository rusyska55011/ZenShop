from django.db import models
from django.contrib.sessions.models import Session

from datetime import datetime

from Clothe.models import ProductSizeType
from UserAccounts.models import UserAccounts

class Cart(models.Model):
    order_datetime = models.DateTimeField('Дата создания', auto_now_add=datetime.now)
    products = models.ManyToManyField(ProductSizeType, verbose_name='Выбранные товары')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина №{self.pk}'

class CartOfSessions(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE, verbose_name='Сессия')
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, verbose_name='Корзина')

    class Meta:
        verbose_name = 'Корзина для незарегестрированных пользователей'
        verbose_name_plural = 'Корзины для незарегестрированных пользователей'

    def __str__(self):
        return f'Запись №{self.pk} сессии {self.session} корзины №{self.cart.pk}'

class CartForAccounts(models.Model):
    account = models.OneToOneField(UserAccounts, on_delete=models.CASCADE, verbose_name='Аккаунт')
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, verbose_name='Корзина')

    class Meta:
        verbose_name = 'Корзина для аккаунтов'
        verbose_name_plural = 'Корзины для аккаунтов'

    def __str__(self):
        return f'Запись №{self.pk} аккаунта {self.account} корзины №{self.cart.pk}'
