from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer, AddCategorySerializer,UpdateCategorySerializer
from .services import CategoryService
from core.responses import success_response, error_response

class GetCategories(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return success_response(
            data={'categories': serializer.data},
            message='Categories retrieved successfully'
            )

class CategoryDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return success_response(
                data={'category': serializer.data},
                message='Category retrieved successfully'
            )
        except Category.DoesNotExist:
            return error_response(
                message='Category not found',
                status_code=404
            )

class AddCategory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddCategorySerializer(data=request.data)
        if serializer.is_valid():
            category = CategoryService.add_category(serializer.validated_data)
            if not category:
                return error_response(
                        message='Category name already exists'
                )
            return success_response(
                data={'category': CategorySerializer(category).data},
                message='Category added successfully',
                status_code=201
            )
        return error_response(
            message='Invalid data provided',
            errors=serializer.errors,
            status_code=400
        )
        
        
class UpdateCategory(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return error_response(
                message='Category not found',
                status_code=404
            )
            
        serializer = UpdateCategorySerializer(data=request.data)
        if serializer.is_valid():
            category = CategoryService.update_category(pk, serializer.validated_data)
            if not category:
                return error_response(
                    message='Category name already exists'
                )
            return success_response(
                message='Category updated successfully',
                data=CategorySerializer(category).data,
                status_code=200,
            )
        else:
            return error_response(
                message='Invalid data provided',
                errors=serializer.errors,
                status_code=400
            )
            

class DeleteCategory(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category_name = category.name
            category.delete()
            return success_response(
                message=f"Category '{category_name}' deleted successfully",
                status_code=204
            )
        except Category.DoesNotExist:
            return error_response(
                message="Category not found",
                status_code=404
            )
        except Exception as e:
            return error_response(
                message="Couldn't delete category",
                status_code=500
            )
