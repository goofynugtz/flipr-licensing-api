from django.contrib import admin
from .models import Organization, Employee
from django.contrib.auth.admin import UserAdmin
from .forms import EmployeeCreationForm, EmployeeChangeForm

class EmployeeAdmin(UserAdmin):
    add_form = EmployeeCreationForm
    form = EmployeeChangeForm
    model = Employee
    list_display = ('email', 'name', 'organization', 'is_staff', 'is_active')
    list_filter = ('email', 'name', 'organization', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Details', {'fields': (('name', 'organization',), 'phone', 'address')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', )
        })
    )
    search_fields = ('email', 'name', 'organization', 'phone')
    ordering = ('organization', 'name', 'email',)


admin.site.register(Employee, EmployeeAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')

admin.site.register(Organization, OrganizationAdmin)

