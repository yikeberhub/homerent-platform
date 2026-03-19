from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsPropertyOwnerOrAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or (hasattr(request.user, 'role') and request.user.role == 'admin'):
            return True
            
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
            
        return False


class PropertyAccessPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if isinstance(view, (GetProperties, PropertyDetail)):
            return True
            
        if not request.user.is_authenticated:
            return False
            
        if hasattr(request.user, 'role') and request.user.role == 'admin':
            return True
            
        if isinstance(view, AddProperty):
            return hasattr(request.user, 'role') and request.user.role == 'owner'
            
        if isinstance(view, (UpdateProperty, DeleteProperty)):
            return hasattr(request.user, 'role') and request.user.role in ['owner', 'admin']
            
        return False
    
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'role') and request.user.role == 'admin':
            return True
            
        if isinstance(view, (UpdateProperty, DeleteProperty)):
            return obj.owner == request.user
            
        return True


class IsOwner(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                hasattr(request.user, 'role') and 
                request.user.role == 'OWNER')


class IsAdmin(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                hasattr(request.user, 'role') and 
                request.user.role == 'admin')


class IsRenter(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                hasattr(request.user, 'role') and 
                request.user.role == 'renter')