from django.contrib import admin

from Orders.admin import get_products_in_order
from .models import Cart, CartOfSessions

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    def products_in_order(self, obj):
        products_value, products = get_products_in_order(obj)
        return f'{products_value} товара: ' + ' ; '.join(products)

    list_display = ('order_datetime', 'products_in_order',)
    readonly_fields = ('order_datetime', 'products', 'session',)
    ordering = ('order_datetime',)
    list_filter = ('order_datetime',)

@admin.register(CartOfSessions)
class CartOfSessionsAdmin(admin.ModelAdmin):
    @admin.display(description='Дата создания')
    def get_date(self, obj):
        return obj.cart.order_datetime

    @admin.display(description='Товары в корзине')
    def get_products(self, obj):
        value, items = get_products_in_order(obj.cart)
        return items

    @admin.display(description='Номер корзины (таблицы "Корзины")')
    def get_cart_number(self, obj):
        return f'Корзина №{obj.cart.pk}'

    list_display = ('get_cart_number', 'session', 'get_date', 'get_products')