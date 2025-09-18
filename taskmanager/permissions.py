from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group

class IsAdminOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(name__in=['Admin', 'SuperAdmin']).exists()
        )

class IsTaskOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name__in=['Admin', 'SuperAdmin']).exists():
            return True
        return obj.assigned_to == request.user