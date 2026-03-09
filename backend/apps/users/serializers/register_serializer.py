from rest_framework import serializers
from apps.users.models.user import User 

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=8)
    
    class Meta:
        model = User
        fields = ['name','email','password','phone','role']
        