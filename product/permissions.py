from rest_framework.permissions import BasePermission

class IsAdminUserJWT(BasePermission):
    """
    Allows access only to users with 'is_staff' set to True.
    """
    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated and user.is_staff


class IsCommonUserJWT(BasePermission):
    """
    Allows access only to requests with the static common token.
    """
    def has_permission(self, request, view):
        # Replace with your generated common token
        common_token = 'Bearer your_common_token'
        auth = request.headers.get('Authorization', '')
        return auth == common_token