from rest_framework.permissions import BasePermission
from rest_framework.views import Request, View


class IsAuthenticatedAndStaff(BasePermission):
    """
    Allows access only to authenticated users who are staff (admin).
    
    Used for admin-only views such as vacation editing or deletion.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        """
        Check if the user is authenticated and has staff privileges.

        Args:
            request (Request): The HTTP request object.
            view (View): The view being accessed.

        Returns:
            bool: True if user is authenticated and staff, otherwise False.
        """
        print("[DEBUG Permission] User:", request.user)
        print("[DEBUG Permission] is_authenticated:", request.user.is_authenticated)
        print("[DEBUG Permission] is_staff:", request.user.is_staff)

        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
