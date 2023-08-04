from rest_framework.permissions import BasePermission


class IsBO(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and obj.is_active == True:
            return True
        return False


class IsPI(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and obj.is_active == True:
            return True
        return False


class IsDYSP(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and obj.is_active == True:
            return True
        return False
    

class IsSP(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and obj.is_active == True:
            return True
        return False


class IsIGP(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and obj.is_active == True:
            return True
        return False
