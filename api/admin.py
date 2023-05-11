from django.contrib import admin
from .models import License

class LicenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'key', 'status', 'user', 'updatedAt', 'createdAt')

admin.site.register(License, LicenseAdmin)
