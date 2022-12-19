from django.contrib import admin
from .models import DiliveryType, DiliveryPlace, Orders

def get_products_in_order(obj: Orders.products) -> (int, list):
    products_name_size_string_collection = [f'{product.product.name} ({product.size.name})' for product in
                                            obj.products.all()]
    return len(products_name_size_string_collection), products_name_size_string_collection

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
    @admin.display(description='Товары в заказе')
    def products_in_order(self, obj):
        value, items = get_products_in_order(obj)
        return f'{value} товара: ' + ' ; '.join(items)

    @admin.display(description='Номер заказа')
    def order_number(self, obj):
        return f'Заказ №{obj.pk}'

    list_display = ('order_number', 'order_datetime', 'name', 'surname', 'products_in_order')
    list_filter = ('order_datetime',)
    readonly_fields = ('name', 'surname', 'email', 'phone', 'order_datetime', 'products', 'order_type', 'order_adress',
                       'total_price', 'track',)