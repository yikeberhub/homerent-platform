from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.views import APIView
from apps.users.serializers.password_serializer import ChangePasswordSerializer,ForgotPasswordSerializer,ResetPasswordSerializer
from apps.users.services.password_service import PasswordService 

from  core.responses import success_response,error_response 

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        PasswordService.change_password(
            request.user,
            **serializer.validated_data
        )
        
        return success_response(
            message='Password changed successfully'
        )
        
class ForgotPassword(APIView):
    permission_classes=[AllowAny]
    authentication_classes=[]
    
    def post(self,request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        PasswordService.send_reset_email(serializer.validated_data['email',request])
        
        return success_response(
            message='If an account exists with this email, a reset link has been sent.'
        )
        
        
class ResetPasswordView(APIView):
    permission_class = [AllowAny]
    
    def post(self,request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = request.data.get('uid')
        token = serializer.validated_data.get('token')
        new_password = serializer.validated_data.gete('new_password')
        
        PasswordService.reset_password(uid,token,new_password)
        
        return success_response(
            message='Password reset successfully'
        )
        