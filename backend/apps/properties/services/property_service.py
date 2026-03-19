from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from apps.properties.models.location import Location
from apps.properties.models.property import Property,PropertyImage
from apps.properties.serializers.location_serializers import LocationCreateUpdateSerializer


class PropertyService:
    
    @staticmethod
    def get_base_queryset():
        return Property.objects.filter(
            is_active=True,
            is_available=True
        ).select_related('location','category').prefetch_related('images')
        
    @staticmethod
    def apply_filters(queryset,params):
        city = params.get('city')
        category = params.get('category')
        min_price = params.get('min_price')
        max_price = params.get('max_price')
        region = params.get('region')
        village = params.get('village')
        
        if city:
            queryset = queryset.filter(location__city__iexact=city)
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if region:
            queryset = queryset.filter(location__region__iexact=region)
        if village:
            queryset = queryset.filter(location__village__iexact=village)
        
        return queryset
    
    @staticmethod
    def apply_geo_filter(queryset, params):
        lat = params.get('lat')
        lng = params.get('lng')
        radius = params.get('radius')
        
        if lat and lng and radius:
            from django.db.models import F, FloatField, ExpressionWrapper
            from django.db.models.functions import ACos, Cos, Sin, Radians
            
            try:
                lat = float(lat)
                lng = float(lng)
                radius = float(radius)
            except (TypeError,ValueError):
                raise ValidationError('Invalid geo parameters')
            
            queryset = queryset.annotate(
                distance=ExpressionWrapper(6371 * ACos(  
                    Cos(Radians(lat)) *
                    Cos(Radians(F('location__latitude'))) *
                    Cos(Radians(F('location__longitude')) - Radians(lng)) +
                    Sin(Radians(lat)) *
                    Sin(Radians(F('location__latitude')))
                ),
                output_field=FloatField()
                )
            ).filter(distance__lte=radius).order_by('distance')

        
        return queryset
        
    
    @staticmethod
    def filter_properties(params):
        queryset = PropertyService.get_base_queryset()
        queryset = PropertyService.apply_filters(queryset,params)
        queryset = PropertyService.apply_geo_filter(queryset,params)
        
        return queryset
    
    @staticmethod
    def search_properties(q):
        queryset = PropertyService.get_base_queryset()
        queryset = queryset.filter(
            Q(title__icontains=q) | 
            Q(description__icontains=q)|
            Q(category__name__icontains=q)|
            Q(location__city__icontains=q)|
            Q(location__village__icontains=q)|
            Q(location__region__icontains=q)
            
            
            
        )
        return queryset
            
        
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
        
