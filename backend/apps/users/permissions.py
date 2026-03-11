
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    
    def has_permission(self,request,view):
        return request.user.role == 'OWNER'
    
    

class IsAdmin(BasePermission):
    
    def has_permission(self,request,view):
        return request.user.role =='ADMIN'
    
    
    
    