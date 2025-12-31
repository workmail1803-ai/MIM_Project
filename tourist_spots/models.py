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


class TourPackage(models.Model):
    CATEGORY_CHOICES = [
        ('study_tour', 'Study Tour'),
        ('cycling', 'Cycling'),
        ('university_program', 'University Program'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='tour_packages/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100)
    destination = models.CharField(max_length=200)
    highlights = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='study_tour')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_category_display_name(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
    
    class Meta:
        ordering = ['-created_at']


class PackageBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='package_bookings')
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='bookings')
    student_name = models.CharField(max_length=200)
    student_id = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    emergency_contact = models.CharField(max_length=20, blank=True)
    num_persons = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    student_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student_name} - {self.package.name}"
    
    class Meta:
        ordering = ['-created_at']


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    booking = models.ForeignKey(PackageBooking, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    bkash_last_4 = models.CharField(max_length=4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment for {self.booking.student_name} - ৳{self.amount_paid}"
    
    class Meta:
        ordering = ['-created_at']
