from django.contrib import admin
from .models import GenderType, ClotheType, SizeType, Products, ProductSizeType, MediaFiles

class HideModel(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

admin.site.register(GenderType, HideModel)
admin.site.register(ClotheType, HideModel)

@admin.register(SizeType)
class SizeTypeAdmin(admin.ModelAdmin):
    list_display = ('clothe_type', 'name', 'rus_measurement_system_name',)
    list_filter = ('clothe_type',)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'clothe_type', 'gender', 'price', 'discount',)
    list_filter = ('clothe_type', 'name',)
    search_fields = ('name', 'description',)

@admin.register(ProductSizeType)
class ProductsSizeTypeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'in_stock',)
    list_filter = ('size',)

@admin.register(MediaFiles)
class MediaFilesAdmin(admin.ModelAdmin):
    list_display = ('get_img', 'alt',)
    list_filter = ('alt',)
    readonly_fields = ('get_img',)
