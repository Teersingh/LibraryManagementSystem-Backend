
from rest_framework.permissions import BasePermission

class IsLibrarian(BasePermission):
    """
    Allows access only to users in the Librarian group.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.groups.filter(name='Librarian').exists()
        )
