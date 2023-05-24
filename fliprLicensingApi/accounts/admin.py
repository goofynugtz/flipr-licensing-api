from django.contrib import admin
from .models import Organization, Employee
from django.contrib.auth.admin import UserAdmin
from .forms import EmployeeCreationForm, EmployeeChangeForm

class EmployeeAdmin(UserAdmin):
  add_form = EmployeeCreationForm
  form = EmployeeChangeForm
  model = Employee
  list_display = ('email', 'name', 'organization', 'is_verified', 'is_staff', 'is_active',)
  list_filter = ('email', 'name', 'organization', 'is_verified', 'is_staff', 'is_active')
  
  fieldsets = (
    (None, {'fields': ('email', 'password')}),
    ('Details', {'fields': (('name', 'organization',), 'phone', 'emp_address')}),
    ('Permissions', {'fields': ('is_verified', 'is_staff', 'is_active', 'confirmation_token',)}),
  )
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': (('email', 'name',), 'password1', 'password2', ('organization', 'phone',), 'emp_address',  'is_staff', 'is_active', ),
    }, ),
  )
  search_fields = ('is_verified', 'email', 'name', 'organization', 'phone')
  ordering = ('organization', 'is_verified', 'name', 'email',)

class OrganizationAdmin(admin.ModelAdmin):
  list_display = ('title', 'url', 'org_address')

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Organization, OrganizationAdmin)

