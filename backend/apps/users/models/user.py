from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from django.utils import timezone
from apps.users.managers import UserManager


class User(AbstractBaseUser,PermissionsMixin):
    
    class Role(models.TextChoices):
        RENTER = 'RENTER','Renter'
        LANDLORD = 'LANDLORD','Landlord'
        ADMIN = 'ADMIN', 'Admin'
        
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone= models.CharField(max_length=20,unique=True)
    
    role = models.CharField(
        max_length=20,
        choices=Role.Choices,
        default=Role.RENTER
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