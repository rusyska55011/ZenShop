from django.contrib import admin
from .models import DiliveryType

@admin.register(DiliveryType)
class DiliveryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    list_filter = ('name',)