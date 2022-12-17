from django.contrib import admin

from Orders.admin import get_products_in_order
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    def products_in_order(self, obj):
        return get_products_in_order(obj)

    list_display = ('order_datetime', 'products_in_order', 'session')
    readonly_fields = ('order_datetime', 'products', 'session')
    ordering = ('order_datetime',)
    list_filter = ('order_datetime',)
