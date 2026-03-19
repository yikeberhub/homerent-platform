from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models.property import Property
from .models.location import Location
from .serializers.property_serializers import PropertySerializer, PropertyCreateUpdateSerializer
from .permissions import PropertyAccessPermission, IsPropertyOwnerOrAdmin, IsOwner,IsRenter
from core.responses import success_response, error_response
from core.pagination import CustomResultPagination


class GetProperties(APIView):
    permission_classes = []
    
    def get(self, request):
        properties = Property.objects.all()
        
        if (request.user.is_authenticated and 
            hasattr(request.user, 'role') and 
            request.user.role == 'renter'):
            properties = properties.filter(is_active=True, is_available=True)
            
        elif (request.user.is_authenticated and 
              hasattr(request.user, 'role') and 
              request.user.role == 'owner' and 
              not (hasattr(request.user, 'role') and request.user.role == 'admin')):
            properties = properties.filter(owner=request.user)
        
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
    permission_classes = []
    
    def get(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk)
            
            if (request.user.is_authenticated and 
                hasattr(request.user, 'role') and 
                request.user.role == 'renter'):
                if not property_obj.is_active or not property_obj.is_available:
                    return error_response(
                        message='Property not available',
                        status_code=404
                    )
            
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
    permission_classes = [IsAuthenticated, IsOwner]
    
    def post(self, request):
        serializer = PropertyCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            property_obj = serializer.save(owner=request.user)
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
    permission_classes = [IsAuthenticated, IsPropertyOwnerOrAdmin]
    
    def patch(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk)
            self.check_object_permissions(request, property_obj)
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
    permission_classes = [IsAuthenticated, IsPropertyOwnerOrAdmin]
    
    def delete(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk)
            self.check_object_permissions(request, property_obj)
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
            

class ActivateProperty(APIView):
    permission_classes = [IsAuthenticated, IsPropertyOwnerOrAdmin]
    
    def post(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk)
            self.check_object_permissions(request, property_obj)
            property_obj.is_active = True
            property_obj.save()
            return success_response(
                message='Property activated successfully'
            )
        except Property.DoesNotExist:
            return error_response(
                message='Property not found',
                status_code=404
            )


class DeactivateProperty(APIView):
    permission_classes = [IsAuthenticated, IsPropertyOwnerOrAdmin]
    
    def post(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk)
            self.check_object_permissions(request, property_obj)
            property_obj.is_active = False
            property_obj.save()
            return success_response(
                message='Property deactivated successfully'
            )
        except Property.DoesNotExist:
            return error_response(
                message='Property not found',
                status_code=404
            )


class AddToFavoriteView(APIView):
    permission_classes = [IsAuthenticated, IsRenter]

    def post(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk, status="ACTIVE")

            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                property=property_obj
            )

            if not created:
                return success_response(message="Already in favorites")

            return success_response(message="Added to favorites")

        except Property.DoesNotExist:
            return error_response(
                message="Property not found",
                status_code=404
            )

class RemoveFromFavoriteView(APIView):
    permission_classes = [IsAuthenticated, IsRenter]

    def post(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk)

            favorite = Favorite.objects.filter(
                user=request.user,
                property=property_obj
            ).first()

            if not favorite:
                return error_response(
                    message="Not in favorites",
                    status_code=404
                )

            favorite.delete()
            return success_response(message="Removed from favorites")

        except Property.DoesNotExist:
            return error_response(
                message="Property not found",
                status_code=404
            )
            
            
class ActivatePropertyView(APIView):
    permission_classes = [IsAuthenticated, IsPropertyOwnerOrAdmin]
    
    def post(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk)
            self.check_object_permissions(request, property_obj)
            property_obj.is_active = True
            property_obj.save()
            return success_response(
                message='Property activated successfully'
            )
        except Property.DoesNotExist:
            return error_response(
                message='Property not found',
                status_code=404
            )
            
            
class DeactivatePropertyView(APIView):
    permission_classes = [IsAuthenticated, IsPropertyOwnerOrAdmin]
    
    def post(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk)
            self.check_object_permissions(request, property_obj)
            property_obj.is_active = False
            property_obj.save()
            return success_response(
                message='Property deactivated successfully'
            )
        except Property.DoesNotExist:
            return error_response(
                message='Property not found',
                status_code=404
            )