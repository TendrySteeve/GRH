from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated and request.user.role == 'ADMIN'
  
class IsResponsable(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated and request.user.role == 'RESP'
  
class IsEmployee(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated and request.user.role == 'EMPLOYEE'
  
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
