from django.contrib import admin
from .models import License

class LicenseAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    
    list_display = ('id', 'name', 'key', 'status', 'user', 'validUpto', 'updatedAt', 'createdAt')

admin.site.register(License, LicenseAdmin)
