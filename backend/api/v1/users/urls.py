
from django.urls import path 
from apps.users.views.auth_views import RegisterView,LoginView,ProfileView 

urlpatterns = [
    path('register/',RegisterView.as_view(),name='user-register'),
    path('login/',LoginView.as_view(),name='user-login'),
    path('profile/',ProfileView.as_view(),name='user-profile'),
    
]
