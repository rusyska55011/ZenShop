from django.db import models
from django.contrib.sessions.models import Session

from datetime import datetime

from Clothe.models import ProductSizeType
class Cart(models.Model):
    order_datetime = models.DateTimeField('Дата создания', auto_now_add=datetime.now)
    products = models.ManyToManyField(ProductSizeType, verbose_name='Выбранные товары')
    session = models.OneToOneField(Session, on_delete=models.CASCADE, verbose_name='Сессия', unique=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Сессия {self.session}'
