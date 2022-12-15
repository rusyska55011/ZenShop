from django.db import models
from django.core.validators import MinValueValidator


class DiliveryType(models.Model):
    name = models.CharField('Наименование', max_length=50, unique=True)
    price = models.IntegerField('Цена', validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} | {self.price}'
