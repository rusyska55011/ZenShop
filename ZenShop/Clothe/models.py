from django.db import models

class GenderType(models.Model):
    name = models.CharField('Название', max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предназначение одежды'
        verbose_name_plural = verbose_name

class ClotheType(models.Model):
    name = models.CharField('Название', max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Виды одежды'
        verbose_name_plural = verbose_name
        ordering = ('name',)