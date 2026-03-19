from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from django.utils import timezone
from apps.users.managers.user_manager import UserManager


class User(AbstractBaseUser,PermissionsMixin):
    
    ROLE_CHOICES = (
        ("RENTER", "Renter"),
        ("OWNER", "Owner"),
        ("ADMIN", "Admin"),
    )

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone= models.CharField(max_length=20,unique=True)
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='RENTER'
    )
    
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['name']
    
    def __str__(self):
        return self.email
    
    def is_admin(self):
        return self.role=='ADMIN'
    
    def is_owner(self):
        return self.role =='OWNER'
    
    def is_retner(self):
        return self.role =='RENTER'
    
    