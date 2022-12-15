from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


class DiliveryType(models.Model):
    name = models.CharField('Наименование', max_length=50, unique=True)
    price = models.IntegerField('Цена', validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} | {self.price} руб.'

class DiliveryPlace(models.Model):
    mail_index = models.IntegerField('Почтовый индекс', validators=[MinValueValidator(100000), MaxValueValidator(999999)])
    region = models.CharField('Регион', max_length=50)
    city = models.CharField('Населенный пункт', max_length=15)
    street = models.CharField('Улица', max_length=30)
    number = models.CharField('Номер дома', max_length=7)

    class Meta:
        verbose_name = 'Места доставки'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.mail_index} | {self.region} | {self.city} | {self.street} | {self.number}'
