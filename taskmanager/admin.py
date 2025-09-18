from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import Task

# Unregister defaults
admin.site.unregister(User)
admin.site.unregister(Group)

# Register Task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'assigned_to', 'status', 'due_date', 'worked_hours']
    list_filter = ['status', 'due_date', 'assigned_to']
    search_fields = ['title', 'description']
    readonly_fields = ['completion_report', 'worked_hours']

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_staff', 'get_groups']
    list_filter = ['groups', 'is_staff', 'is_superuser']

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()]) or 'None'
    get_groups.short_description = 'Groups/Roles'

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Append groups to the last fieldset instead of creating duplicate
        fieldsets = list(fieldsets)
        fieldsets[-1] = (fieldsets[-1][0], {'fields': fieldsets[-1][1]['fields'] + ('groups',)})
        return fieldsets

admin.site.register(User, CustomUserAdmin)

# Register Group
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']