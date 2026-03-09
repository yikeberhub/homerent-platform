
from django.contrib.auth import authenticate 
from apps.users.models.user import User 
from rest_framework.exceptions import ValidationError 

class AuthService:
    
    @staticmethod
    def register_user(validated_data):
        email = validated_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('User with this email already exists.')
        return User.objects.create_user(**validated_data)
    
    @staticmethod
    def login_user(email,password):
        print('email is',email)
        print('password is',password)
        user = authenticate(email=email,password=password)
        if not user:
            raise ValidationError('Invalid Credentials')
        return user
    
    @staticmethod
    def get_profile(user):
        return user