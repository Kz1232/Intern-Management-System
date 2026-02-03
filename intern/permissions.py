from rest_framework.permissions import BasePermission

class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user,'userprofile') and request.user.userprofile.role == 'SUPERVISOR':
            return True 
        else:
            return False
