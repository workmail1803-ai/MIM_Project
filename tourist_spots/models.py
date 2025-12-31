from django.db import models
from django.contrib.auth.models import User

class TouristSpot(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='tourist_spots/')
    highlights = models.TextField(blank=True)
    travel_info = models.TextField(blank=True)
    best_time = models.TextField(blank=True)
    safety_info = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']