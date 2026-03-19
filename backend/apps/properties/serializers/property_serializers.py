from rest_framework import serializers
from apps.properties.models.property import Property, PropertyImage
from apps.properties.models.location import Location
from apps.properties.services import PropertyService
from .location_serializers import LocationSerializer,FlexibleLocationField


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    location_details = LocationSerializer(source='location', read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Property
        fields = '__all__'


class PropertyCreateUpdateSerializer(serializers.ModelSerializer):
    location = FlexibleLocationField(required=False)
    class Meta:
        model = Property
        fields = '__all__'
        
    
        
    def create(self, validated_data):
        location_data = self.initial_data.get('location')
        return PropertyService.create_property(validated_data, location_data)

    def update(self, instance, validated_data):
        location_data = self.initial_data.get('location')
        return PropertyService.update_property(instance, validated_data, location_data)


class PropertyImageCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'
