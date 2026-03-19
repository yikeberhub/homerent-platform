from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models.location import Location
from .models.property import Property,PropertyImage
from .serializers.location_serializers import LocationCreateUpdateSerializer


class PropertyService:
    @staticmethod
    def handle_location_data(location_data):
        
        if isinstance(location_data, dict):
            try:
                location = Location.objects.get(
                    city=location_data.get('city'),
                    village=location_data.get('village'),
                    region=location_data.get('region'),
                    latitude=location_data.get('latitude'),
                    longitude=location_data.get('longitude')
                    
                )
                return location 
            except Location.DoesNotExist:
                location_serializer = LocationCreateUpdateSerializer(data=location_data)
                if location_serializer.is_valid():
                    return location_serializer.save()
                else:
                    raise ValidationError({
                        'location': location_serializer.errors
                    })
        elif isinstance(location_data, int):
            try:
                return Location.objects.get(pk=location_data)
            except Location.DoesNotExist:
                raise ValidationError({
                    'location': f'Location with id {location_data} does not exist.'
                })
        else:
            raise ValidationError({
                'location': 'Location data must be either an object or an integer ID.'
            })
            
    

    @staticmethod
    @transaction.atomic
    def create_property(validated_data, location_data,images_data=None):
        location = PropertyService.handle_location_data(location_data)
        validated_data['location'] = location
        property_instance = Property.objects.create(**validated_data)
        if images_data:
            PropertyService._hanle_property_images(property_instance,images_data)
            
        return property_instance
    
    

    @staticmethod
    @transaction.atomic
    def update_property(property_instance, validated_data, location_data=None,images_data=None):
        if location_data is not None:
            location = PropertyService.handle_location_data(location_data)
            validated_data['location'] = location
            
        for attr, value in validated_data.items():
            setattr(property_instance, attr, value)
        property_instance.save()
        
        if images_data is not None:
            PropertyService._handle_property_images(property_instance,images_data)
        return property_instance
    
    
    @staticmethod
    def _handle_property_images(property_instance,images_data):
        
        if not isinstance(images_data,list):
            raise ValidationError({
                'images':'Images data must be a list'
            })
        
        image_instances = []
        for image_data in images_data:
            if not isinstance(image_data,dict):
                raise ValidationError({
                    'images':'Each image must be an object'
                })
            image_data['property']=property_instance.id
            image_instances.append(PropertyImage(**image_data))
        if image_instances:
            PropertyImage.objects.bulk_create(image_instances)
        
