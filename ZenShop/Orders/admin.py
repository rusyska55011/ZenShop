from django.contrib import admin
from .models import DiliveryType, DiliveryPlace

@admin.register(DiliveryType)
class DiliveryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    list_filter = ('name',)

@admin.register(DiliveryPlace)
class DiliveryPlaceAdmin(admin.ModelAdmin):
    list_display = ('mail_index', 'region', 'city', 'street', 'number')
    list_filter = ('region',)
    readonly_fields = ('mail_index', 'region', 'city', 'street', 'number')
