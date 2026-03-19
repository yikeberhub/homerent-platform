
from rest_framework import serializers
from apps.properties.models.location import Location

    
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        

class FlexibleLocationField(serializers.Field):    
    def to_representation(self, value):
        return LocationSerializer(value).data
    
    def to_internal_value(self, data):
        return data


class LocationCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'