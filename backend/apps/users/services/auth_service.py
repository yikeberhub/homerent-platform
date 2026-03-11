
from django.contrib.auth import authenticate 
from rest_framework.exceptions import ValidationError 
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models.user import User 

class AuthService:
    
    @staticmethod
    def register_user(data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('User with this email already exists.')
        user= User.objects.create_user(**data)
        return user
    
    @staticmethod
    def login_user(email,password):
        user = authenticate(email=email,password=password)
        
        if not user:
            raise ValidationError('Invalid Credentials')
        refresh = RefreshToken.for_user(user)
        
        return {
            'user':user,
            'access':str(refresh.access_token),
            'refresh':str(refresh)
        }
    
    @staticmethod
    def get_profile(user):
        return user