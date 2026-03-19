from django.db import models
from apps.users.models.user import User 
from apps.categories.models import Category
from .location import Location

class Property(models.Model):
    LISTING_TYPES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='properties')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    area_sqm = models.PositiveIntegerField(help_text="Area in square meters")
    year_built = models.PositiveIntegerField(null=True, blank=True)
    
    price = models.DecimalField(max_digits=15, decimal_places=2, help_text="Price in ETB")
    maintenance_fee = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Monthly fee in ETB")
    
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES)
    
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    phone_contact = models.CharField(max_length=20,null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.location.full_address}"
    
    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = ['Properties']

class PropertyImage(models.Model):
    
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.property.title}"
    
    class Meta:
        ordering = ['created_at']