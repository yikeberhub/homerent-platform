from django.db import models

class Location(models.Model):
    REGIONS = [
        ('addis_ababa', 'Addis Ababa'),
        ('oromia', 'Oromia'),
        ('amhara', 'Amhara'),
        ('snnpr', 'Southern Nations, Nationalities, and Peoples Region'),
        ('tigray', 'Tigray'),
        ('afar', 'Afar'),
        ('somali', 'Somali'),
        ('benishangul', 'Benishangul-Gumuz'),
        ('gambella', 'Gambella'),
        ('harari', 'Harari'),
        ('sidama', 'Sidama'),
        ('south_west', 'South West Ethiopia Peoples'),
    ]
    
    city = models.CharField(max_length=100, help_text="City or Town name")
    village = models.CharField(max_length=100, blank=True, help_text="Village or neighborhood name within city (optional)")
    region = models.CharField(max_length=50, choices=REGIONS)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    def __str__(self):
        if self.village:
            return f"{self.village}, {self.city}, {self.get_region_display()}"
        return f"{self.city}, {self.get_region_display()}"
    
    @property
    def full_address(self):
        if self.village:
            return f"{self.village}, {self.city}"
        return self.city
    
    class Meta:
        unique_together = ['city', 'village', 'region']
        ordering = ['city', 'village']