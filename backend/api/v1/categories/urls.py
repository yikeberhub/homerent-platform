
from django.urls import path 
from apps.categories.views import GetCategories, AddCategory, CategoryDetail, UpdateCategory, DeleteCategory

urlpatterns = [
    path('', GetCategories.as_view(), name='get-categories'),
    path('add/', AddCategory.as_view(), name='add-category'),
    path('<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('<int:pk>/update/', UpdateCategory.as_view(), name='update-category'),
    path('<int:pk>/delete/', DeleteCategory.as_view(), name='delete-category'),
]
