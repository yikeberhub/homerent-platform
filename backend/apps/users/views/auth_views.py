from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status 
from apps.users.serializers.register_serializer import RegisterSerializer 
from apps.users.serializers.login_serializer import LoginSerializer 
from apps.users.serializers.user_serializer import UserSerializer
from apps.users.services.auth_service import AuthService 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = AuthService.register_user(serializer.validated_data)
        
        return Response({
            'message':'user registered successfully',
            'user':UserSerializer(user).data
        
        },status=status.HTTP_201_CREATED)
        
  
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = AuthService.login_user(email,password)
        
        token = 'This is token...'
        return Response({
            'message':'Login successful',
            'user':UserSerializer(user).data,
            'token':token
        },status = status.HTTP_200_OK)
    
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user = AuthService.get_profile(request.user)
        return Response({
            'user':UserSerializer(user).data
        },status=status.HTTP_200_OK)