
from django.db import models
from django.conf import settings
from .user import User

class Credit(models.Model):
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='credit',
        null=True 
    )
    total_credits = models.IntegerField(default=0)
    
    used_credits = models.IntegerField(default=0)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def remaining(self):
        return self.total_credits-self.used_credits
    
    
    def __str__(self):
        return f'{self.user.email} credits'