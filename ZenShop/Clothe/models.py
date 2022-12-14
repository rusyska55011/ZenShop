from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, ValidationError
from django.utils.html import mark_safe


allowed_photo_extensions = ['.png', '.jpg', '.jpeg', '.gif']
alloved_video_extensions = ['.mp4',]
def is_valid_media(url: str):
    for item in allowed_photo_extensions + alloved_video_extensions:
        if url.find(item) + 1:
            return True, item
    return False, 'null'


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
    clothe_type = models.ForeignKey(ClotheType, on_delete=models.PROTECT, default=0, verbose_name='Вид одежды')
    name = models.CharField('Название', max_length=10)
    rus_measurement_system_name = models.CharField('Российская система измерения', max_length=10, blank=True, null=True)

    height_from = models.SmallIntegerField('Рост от', validators=[MinValueValidator(0)],
                                           help_text='Торс и ноги. Поля "Рост от" и "Рост до" связаны и будут представлять собой запись, напр. 176-180',
                                           blank=True, null=True)
    height_to = models.SmallIntegerField('Рост до', validators=[MinValueValidator(0)], help_text='Торс и ноги', blank=True, null=True)
    lenght = models.FloatField('Длина', validators=[MinValueValidator(0)], help_text='Торс и ноги', blank=True, null=True)

    width = models.FloatField('Ширина', validators=[MinValueValidator(0)], help_text='Торс', blank=True, null=True)
    sleeve_lenght = models.FloatField('Длина рукава', validators=[MinValueValidator(0)], help_text='Торс', blank=True, null=True)
    bust = models.FloatField('Обхват груди', validators=[MinValueValidator(0)], help_text='Торс', blank=True, null=True)

    waist = models.FloatField('Талия', validators=[MinValueValidator(0)], help_text='Ноги', blank=True, null=True)
    hips = models.FloatField('Бедра', validators=[MinValueValidator(0)], help_text='Ноги', blank=True, null=True)

    head_girth = models.FloatField('Обхват головы', validators=[MinValueValidator(0)], help_text='Головной убор',
                                          blank=True, null=True)

    foot_size = models.SmallIntegerField('Длина стопы', validators=[MinValueValidator(0)], help_text='Обувь', blank=True, null=True)

    palm_circumference = models.FloatField('Обхват ладони', validators=[MinValueValidator(0)], help_text='Перчатки',
                                                  blank=True, null=True)

    class Meta:
        verbose_name = 'Типы размеров'
        verbose_name_plural = verbose_name
        ordering = ('clothe_type', 'name',)
        unique_together = ('clothe_type', 'name',)

    def __str__(self):
        return f'{self.clothe_type} | {self.name}'

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
        if all([self.height_from, self.height_to]):
            if self.height_from > self.height_to:
                raise ValidationError('Поле "Рост от" не может быть меньше поля "Рост до"')

    def clean(self):
        self.valid_height()
        self.valid_data()

class MediaFiles(models.Model):
    url = models.FileField(f'Файл ({" ".join(alloved_video_extensions + allowed_photo_extensions)})', upload_to='Clothe')
    alt = models.CharField('Текст при наведении', max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = 'Медиа файлы'
        verbose_name_plural = verbose_name
        ordering = ('alt',)

    def __str__(self):
        if self.alt:
            return f'{self.url} ALT: {self.alt}'
        return str(self.url)

    def get_img(self):
        return mark_safe(f'<img src="{self.url.url}" width="100" height="100" />')

    def clean(self):
        is_valid, media_extention = is_valid_media(str(self.url))
        if not is_valid:
            raise ValidationError('Файл неподдерживамого формата')


class Products(models.Model):
    name = models.CharField('Название', max_length=50)
    clothe_type = models.ForeignKey(ClotheType, on_delete=models.PROTECT, default=0, verbose_name='Вид одежды')
    gender = models.ForeignKey(GenderType, on_delete=models.PROTECT, default=0, verbose_name='Презначение одежды')
    description = models.CharField('Описание товара', max_length=300, blank=True, null=True)
    photo_video = models.ManyToManyField(MediaFiles, verbose_name=f'Файл ({" ".join(alloved_video_extensions + allowed_photo_extensions)})')
    price = models.IntegerField('Цена, руб.', validators=[MinValueValidator(0)])
    discount = models.SmallIntegerField('Скидка, %', validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = verbose_name
        ordering = ('clothe_type', 'name', 'price', 'discount',)
        unique_together = ('name', 'clothe_type',)

    def discount_result(self):
        return self.price - (self.price / 100) * self.discount

    def __str__(self):
        if self.discount:
            return f'{self.name} | {self.clothe_type} | {self.gender} | {self.price} руб. -{self.discount}% ({self.discount_result()} руб.)'
        return f'{self.name} | {self.clothe_type} | {self.gender} | {self.price} руб.'

class ProductSizeType(models.Model):
    product = models.ForeignKey(Products, on_delete=models.PROTECT, default=0, verbose_name='Товар')
    size = models.ForeignKey(SizeType, on_delete=models.PROTECT, default=0, verbose_name='Размер')
    in_stock = models.SmallIntegerField('В наличии, шт.', default=0)

    class Meta:
        verbose_name = 'Товары и Размеры'
        verbose_name_plural = verbose_name
        ordering = ('product', 'size',)
        unique_together = ('product', 'size',)

    def __str__(self):
        return f'{self.product} | {self.size}'

    def clean(self):
        product_clothe_type = self.product.clothe_type
        size_clothe_type = self.size.clothe_type

        if not(product_clothe_type.pk == size_clothe_type.pk):
            raise ValidationError(f'{self.product} относится к размерам для {product_clothe_type} \
                                    и может не относиться к размеру для {size_clothe_type}')