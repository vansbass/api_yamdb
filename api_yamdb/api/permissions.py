from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorAdminOrReadOnlyPermission(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role in ['admin', 'moderator']
        )
    
class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
        return(
            request.method in SAFE_METHODS
            or request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
        return(
            request.method in SAFE_METHODS
            or request.user.role == 'admin'
        )