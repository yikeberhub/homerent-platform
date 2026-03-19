from django.urls import path,include

urlpatterns = [
    path('users/',include('api.v1.users.urls')),
    path('categories/',include('api.v1.categories.urls')),
]
