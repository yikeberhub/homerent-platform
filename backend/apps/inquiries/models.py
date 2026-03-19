from django.db import models
from apps.users.models.user import User 
from apps.properties.models.property import Property 
# Create your models here.
class Inquiry(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("RESPONDED", "Responded"),
        ("CLOSED", "Closed"),
    ]

    renter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="inquiries"
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="inquiries"
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)