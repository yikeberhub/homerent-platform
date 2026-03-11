
from rest_framework.exceptions import ValidationError 
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail  
from django.contrib.auth import get_user_model
from apps.users.models.user import User

user = get_user_model()

class PasswordService:
    
    @staticmethod
    def change_password(user,old_password,new_password):
        
        if not user.check_password(old_password):
            raise ValidationError('Old password incorrect')
        
        user.set_password(new_password)
        user.save()
        
        return user
    
    @staticmethod 
    def send_reset_email(email, request):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError('User with this email does not exist')
        
        token = PasswordResetTokenGenerator().make_token(user)
    
        result_url = f'{request.scheme}://{request.get_host()}/api/v1/users/reset-password/?token={token}${user.pk}'
        
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {result_url}',
            'noreply@homerent.com',
            [email],
            fail_silently=False
        )
    
    
    @staticmethod 
    def reset_password(uid,token,new_password):
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            raise ValidationError('Invalid user')
        
        valid = PasswordResetTokenGenerator().check_token(user,token)
        
        if not valid:
            raise ValidationError('Invalid or expired token')
        
        user.set_password(new_password)
        user.save()
        return user 