from django.db import models
from django.core.validators import MinValueValidator, ValidationError


class GenderType(models.Model):
    name = models.CharField('Название', max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предназначение одежды'
        verbose_name_plural = verbose_name
        ordering = ('name',)

class ClotheType(models.Model):
    name = models.CharField('Название', max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Виды одежды'
        verbose_name_plural = verbose_name
        ordering = ('name',)

class SizeType(models.Model):
    clothe_type = models.ForeignKey(ClotheType, on_delete=models.SET_NULL, null=True)
    name = models.CharField('Название', max_length=10)
    rus_measurement_system_name = models.CharField('Российская система измерения', max_length=10, blank=True, null=True)

    height_from = models.SmallIntegerField('Рост от', validators=[MinValueValidator(0)],
                                           help_text='Торс и ноги. Поля "Рост от" и "Рост до" связаны и будут представлять собой запись, напр. 176-180',
                                           blank=True, null=True)
    height_to = models.SmallIntegerField('Рост до', validators=[MinValueValidator(0)], help_text='Торс и ноги', blank=True, null=True)
    lenght = models.SmallIntegerField('Длина', validators=[MinValueValidator(0)], help_text='Торс и ноги', blank=True, null=True)

    width = models.SmallIntegerField('Ширина', validators=[MinValueValidator(0)], help_text='Торс', blank=True, null=True)
    sleeve_lenght = models.SmallIntegerField('Длина рукава', validators=[MinValueValidator(0)], help_text='Торс', blank=True, null=True)
    bust = models.SmallIntegerField('Обхват груди', validators=[MinValueValidator(0)], help_text='Торс', blank=True, null=True)

    waist = models.SmallIntegerField('Талия', validators=[MinValueValidator(0)], help_text='Ноги', blank=True, null=True)
    hips = models.SmallIntegerField('Бедра', validators=[MinValueValidator(0)], help_text='Ноги', blank=True, null=True)

    head_girth = models.SmallIntegerField('Обхват головы', validators=[MinValueValidator(0)], help_text='Головной убор',
                                          blank=True, null=True)

    foot_size = models.SmallIntegerField('Длина стопы', validators=[MinValueValidator(0)], help_text='Обувь', blank=True, null=True)

    palm_circumference = models.SmallIntegerField('Обхват ладони', validators=[MinValueValidator(0)], help_text='Перчатки',
                                                  blank=True, null=True)

    class Meta:
        verbose_name = 'Типы размеров'
        verbose_name_plural = verbose_name
        ordering = ('clothe_type', 'name',)
        unique_together = ('clothe_type', 'name',)

    def __str__(self):
        return f'{self.product} | {self.size}'

    def valid_data(self):
        torso_legs_features_collection = (self.height_from, self.height_to, self.lenght)

        torso_features_collection = (self.width, self.sleeve_lenght, self.bust,)
        legs_features_collection = (self.waist, self.hips,)
        head_features_collection = (self.head_girth,)
        foot_features_collection = (self.foot_size,)
        palm_features_collection = (self.palm_circumference,)

        # Сумма групп в которых есть хотябы 1 запись
        if checked_groups := (
                any(torso_features_collection) + any(legs_features_collection) + any(torso_legs_features_collection)
                + any(foot_features_collection) + any(palm_features_collection) + any(head_features_collection)):

            # Если имеются заполненные поля в более чем 1 группе
            if checked_groups > 1:
                # Если групп 2
                if checked_groups == 2:

                    # Если одна запись находится в группе для ног и торса
                    if any(torso_legs_features_collection) or any(legs_features_collection) or any(
                            torso_features_collection):
                        # Если есть хотябы 1 запись в группе торс
                        if any(torso_features_collection):
                            # Если НЕ все записи заполнены в группах торс
                            if not all(torso_features_collection + torso_legs_features_collection):
                                raise ValidationError('Группа торс заполнена не полностью')
                        # Если есть хотябы 1 запись в группе торс
                        elif any(legs_features_collection):
                            # Если НЕ все записи заполнены в группах торс
                            if not all(legs_features_collection + torso_legs_features_collection):
                                raise ValidationError('Группа ноги заполнена не полностью')
                    else:
                        raise ValidationError('Заполненые поля в разных группах')

                else:
                    raise ValidationError('Заполненые поля в разных группах')

            elif checked_groups == 1:
                if any(torso_features_collection):
                    raise ValidationError('Заполнены не все поля в группе Торс')
                elif any(legs_features_collection):
                    raise ValidationError('Заполнены не все поля в группе Ноги')
                elif any(torso_legs_features_collection):
                    raise ValidationError(
                        'Заполнены поля только в группе Торс и Ноги. Выберите поля для Торса или Ног')

    def valid_height(self):
        if self.height_from > self.height_to:
            raise ValidationError('Поле "Рост от" не может быть меньше поля "Рост до"')

    def clean(self):
        self.valid_height()
        self.valid_data()