from rest_framework import serializers
from apps.users.models.user import User 

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User 
        fields = ('id','name','email','phone','role','is_verified','created_at')