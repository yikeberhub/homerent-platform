
from django.urls import path 
from apps.users.views.auth_views import *
from apps.users.views.password_views import *

urlpatterns = [
    path('register/',RegisterView.as_view(),name='user-register'),
    path('login/',LoginView.as_view(),name='user-login'),
    path('profile/',ProfileView.as_view(),name='user-profile'),
    path('token/refresh/',RefreshTokenView.as_view(),name='token-refresh'),
    path('logout/',LogoutView.as_view(),name='user-logout'),
    
    path('change-password/',ChangePasswordView.as_view(),name='change-password'),
    path('forgot-password/',ForgotPassword.as_view,name='forgot-password'),
    path('reset-password/',ResetPasswordView.as_view(),name='reset-password'),
    
]
