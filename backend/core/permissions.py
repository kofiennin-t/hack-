"""
Custom permissions for the AI Platform.
"""
from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission that allows only the owner of an object or admin to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.is_staff:
            return True
        
        # Check if object has an owner field
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if object is the user themselves
        if hasattr(obj, 'id') and hasattr(request.user, 'id'):
            return obj.id == request.user.id
            
        return False


class IsUserOrAdmin(permissions.BasePermission):
    """
    Permission that allows users to access their own data or admin to access everything.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.is_staff:
            return True
        
        # Check if object belongs to the user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if object is the user themselves
        return obj == request.user


class IsDeveloperOrAdmin(permissions.BasePermission):
    """
    Permission that allows only developers or admin to access certain views.
    """
    
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_staff:
                return True
            # Check if user has developer profile
            return hasattr(request.user, 'developer_profile')
        return False


class IsOwnerDeveloperOrAdmin(permissions.BasePermission):
    """
    Permission for developers to manage their own models.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.is_staff:
            return True
        
        # Check if object belongs to the developer
        if hasattr(obj, 'developer'):
            return hasattr(request.user, 'developer_profile') and obj.developer == request.user.developer_profile
        
        return False


class ReadOnlyOrAdmin(permissions.BasePermission):
    """
    Permission that allows read-only access to everyone, write access to admin only.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and request.user.is_staff
