from django.contrib import admin
from .models import GenderType, ClotheType, SizeType

class HideModel(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

admin.site.register(GenderType, HideModel)
admin.site.register(ClotheType, HideModel)

@admin.register(SizeType)
class SizeTypeAdmin(admin.ModelAdmin):
    list_display = ('clothe_type', 'name', 'rus_measurement_system_name')
    list_filter = ('clothe_type',)