
from django.contrib import admin
from .models.property import Property, PropertyImage
from .models.location import Location


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
        list_display = ('city', 'village', 'region')
        search_fields = ('city', 'village', 'region')
        list_filter = ('region',)
        ordering = ('city', 'village')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('title', 'category', 'location', 'price', 'listing_type', 'is_active', 'is_available', 'is_featured')
    list_filter = ('category', 'location__region', 'listing_type', 'is_active', 'is_available', 'is_featured')
    search_fields = ('title', 'description', 'location__city', 'location__village')
    ordering = ('-created_at',)

