from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (
            request.user.role == 'admin'
            or request.user.is_staff
        )
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        return (
            request.user.role == 'admin'
            or request.user.is_staff
        )
    

class AdminOrReadOnlyPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
        return(
            request.method in SAFE_METHODS
            or request.user.role == 'admin'
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
        return(
            request.method in SAFE_METHODS
            or request.user.role == 'admin'
            or request.user.is_staff
        )


class AuthorStaffOrReadOnlyPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
        return(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            or request.user.role in ['admin', 'moderator']
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
        return(
            request.method in SAFE_METHODS
            or request.user.role in ['admin', 'moderator']
            or request.user.is_staff
            or obj.author == request.user
        )
