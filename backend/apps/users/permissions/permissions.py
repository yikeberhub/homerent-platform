
from rest_framework.permissions import BasePermission

class IsLandLord(BasePermission):
    
    def has_permission(self,request,view):
        return request.user.role == 'LANDLORD'
    
    

class IsAdmin(BasePermission):
    
    def has_permission(self,request,view):
        return request.user.role =='ADMIN'
    
    
    
    