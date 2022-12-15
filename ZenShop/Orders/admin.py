from django.contrib import admin
from .models import DiliveryType, DiliveryPlace, Orders

@admin.register(DiliveryType)
class DiliveryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    list_filter = ('name',)

@admin.register(DiliveryPlace)
class DiliveryPlaceAdmin(admin.ModelAdmin):
    list_display = ('mail_index', 'region', 'city', 'street', 'number')
    list_filter = ('region',)
    readonly_fields = ('mail_index', 'region', 'city', 'street', 'number')


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    def products_in_order(self, obj):
        products_name_size_string_collection = [f'{product.product.name} ({product.size.name})' for product in obj.products.all()]
        return f'{len(products_name_size_string_collection)} товара: ' + ' ; '.join(products_name_size_string_collection)

    def order_number(self, obj):
        return f'Заказ №{obj.pk}'

    list_display = ('order_number', 'order_datetime', 'name', 'surname', 'products_in_order')
    list_filter = ('order_datetime',)
    readonly_fields = ('name', 'surname', 'email', 'phone', 'order_datetime', 'products', 'order_type', 'order_adress',
                       'total_price', 'track',)