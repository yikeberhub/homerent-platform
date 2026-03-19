from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status 
from apps.users.serializers.register_serializer import RegisterSerializer 
from apps.users.serializers.login_serializer import LoginSerializer 
from apps.users.serializers.user_serializer import UserSerializer
from apps.users.services.auth_service import AuthService 
from rest_framework.permissions import IsAuthenticated ,AllowAny

from  core.responses import success_response,error_response

class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = AuthService.register_user(serializer.validated_data)
        
        return success_response(
            data={'user':UserSerializer(user).data},
            message='User registered successfully',
            status_code=201
        )
  
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        
        result = AuthService.login_user(**serializer.validated_data)
        user = UserSerializer(result['user']).data 
        access = result['access']
        refresh = result['refresh']
        
        return success_response(
            data={
                'user':user,
                'access_token':access,
                'refresh_token':refresh
            },
            message='Login successfull',
        )
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        
        print('request user',request.user)
        user = AuthService.get_profile(request.user)
        return success_response(
            data={
                'user':user.data
            },
            message = 'User profile fetched successfully'
        )
        
        
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self,request):
        
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            raise ValidationError('Refresh token required')
        
        try:
            token = RefreshToken(refresh_token)
            return success_response(
                data = {
                    'access_token':str(token.access_token)
                },
                message='Token refreshed'
            )
        except:
            raise ValidationError('Invalid refresh token')
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            raise ValidationError('Refresh token required')
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return success_response(
                message='Logged out successfully'
            )
        except:
            raise ValidationError('Invalid refresh token')
        
        
