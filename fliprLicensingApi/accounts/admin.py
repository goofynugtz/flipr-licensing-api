from django.contrib import admin
from .models import Organization, Employee
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class EmployeeInline(admin.TabularInline):
    model = Employee
    can_delete = False
    verbose_name_plural = "employee"

class UserAdmin(UserAdmin):
    inlines = [EmployeeInline]

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'mobile')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Employee, EmployeeAdmin)
