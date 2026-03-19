from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models.property import Property
from .models.location import Location
from .serializers.property_serializers import PropertySerializer, PropertyCreateUpdateSerializer
from core.responses import success_response, error_response
from core.pagination import CustomResultPagination

class GetProperties(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        properties = Property.objects.all()
        
        paginator = CustomResultPagination()
        paginated_properties = paginator.paginate_queryset(properties, request)
        serializer = PropertySerializer(paginated_properties, many=True)
        
        return paginator.get_paginated_response(
            success_response(
                data={'properties': serializer.data},
                message='Properties retrieved successfully'
            ).data
        )

class PropertyDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk)
            serializer = PropertySerializer(property_obj)
            return success_response(
                data={'property': serializer.data},
                message='Property retrieved successfully'
            )
        except Property.DoesNotExist:
            return error_response(
                message='Property not found',
                status_code=404
            )

class AddProperty(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PropertyCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            property_obj = serializer.save()
            return success_response(
                data={'property': PropertySerializer(property_obj).data},
                message='Property added successfully',
                status_code=201
            )
        return error_response(
            message='Invalid data provided',
            errors=serializer.errors,
            status_code=400
        )

class UpdateProperty(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return error_response(
                message='Property not found',
                status_code=404
            )
            
        serializer = PropertyCreateUpdateSerializer(property_obj, data=request.data, partial=True)
        if serializer.is_valid():
            updated_property = serializer.save()
            return success_response(
                message='Property updated successfully',
                data=PropertySerializer(updated_property).data,
                status_code=200
            )
        else:
            return error_response(
                message='Invalid data provided',
                errors=serializer.errors,
                status_code=400
            )

class DeleteProperty(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk)
            property_title = property_obj.title
            property_obj.delete()
            return success_response(
                message=f"Property '{property_title}' deleted successfully",
                status_code=204
            )
        except Property.DoesNotExist:
            return error_response(
                message="Property not found",
                status_code=404
            )
        except Exception as e:
            return error_response(
                message="Couldn't delete property",
                status_code=500
            )