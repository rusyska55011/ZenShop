from django.contrib import admin
from .models import UserAccounts

@admin.register(UserAccounts)
class UserAccountsAdmin(admin.ModelAdmin):

    @admin.display(description='Число всех заказов')
    def orders_value_history(self, obj):
        return len(obj.order_history.all())

    list_display = ('login', 'name', 'surname', 'orders_value_history',)
    readonly_fields = ('login', 'password', 'name', 'surname', 'email', 'phone', 'order_history',)
    search_fields = ('login',)
